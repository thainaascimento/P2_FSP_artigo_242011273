#!/usr/bin/env python3
"""Consolida estudos editoriais verificáveis e valida metadados DOI via Crossref.
O resultado audita o corpus selecionado para a análise com bibliometrix.
"""
from pathlib import Path
import csv
import json
import os
import re
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from difflib import SequenceMatcher
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artigo" / "literatura"
OUT.mkdir(parents=True, exist_ok=True)
RESEARCH_DIR = Path(os.environ.get("FINANCAS_RESEARCH_SOURCE_DIR", OUT / "pesquisas_brutas"))
SOURCES = [*sorted(RESEARCH_DIR.glob("**/output.txt")), *sorted(RESEARCH_DIR.glob("**/*.json"))]
ARCHIVE = OUT / "corpus_completo_cruzado.json"
AXIS_ALIASES = {
    0: "flypaper_classic", 1: "flypaper_reviews", 2: "fiscal_illusion", 3: "fiscal_federalism",
    4: "brazil_flypaper", 5: "brazil_tax_effort", 6: "china_transfers", 7: "china_local_finance",
    8: "china_institutions", 9: "local_tax_effort", 10: "transfers_growth",
}
SOURCE_ALIASES = {"transferencias_flypaper_artigos": "comparative_flypaper"}


def canonical_origin(value, fallback="archived_corpus"):
    """Keep thematic provenance without publishing local paths or job IDs."""
    value = str(value or fallback).replace("\\", "/")
    if "/" in value:
        path = Path(value)
        value = path.parent.name if path.name == "output.txt" else path.stem
    axis_match = re.fullmatch(r"[a-f0-9]{12}_a(\d+)", value)
    if axis_match:
        return AXIS_ALIASES.get(int(axis_match.group(1)), "research_axis")
    if re.fullmatch(r"job_[A-Za-z0-9]{6,}", value):
        return "comparative_grants"
    return SOURCE_ALIASES.get(value, value)


def tidy_doi(doi):
    if not doi:
        return ""
    doi = str(doi).strip()
    doi = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi, flags=re.I)
    return doi.rstrip(" .,;)").lower()


def normalize(raw, source):
    if isinstance(raw.get("autores"), list):
        authors = raw["autores"]
    elif isinstance(raw.get("authors"), list):
        authors = raw["authors"]
    elif isinstance(raw.get("authors"), str):
        authors = [author.strip() for author in raw["authors"].split(";") if author.strip()]
    else:
        authors = []
    return {
        "authors": authors,
        "year": int(raw.get("year", raw.get("ano"))),
        "title": str(raw.get("title", raw.get("titulo", ""))).strip(),
        "journal": str(raw.get("journal", raw.get("periodico", ""))).strip(),
        "doi": tidy_doi(raw.get("doi")),
        "editorial_url": raw.get("editorial_url", raw.get("verification_url", raw.get("url_editorial", raw.get("doi_url", "")))),
        "finding": str(raw.get("finding", raw.get("achado_confirmado_no_resumo_editorial", raw.get("achado", "")))).strip(),
        "relevance": str(raw.get("relevance", raw.get("tema", ""))).strip(),
        "origin_file": canonical_origin(raw.get("origin_file", source), source),
    }


def read_papers(path):
    obj = json.loads(path.read_text(encoding="utf-8"))
    docs = obj.get("papers", obj.get("artigos", []))
    if path.name == "corpus_completo_cruzado.json":
        docs = docs + obj.get("review_records", [])
    source_id = path.parent.name if path.name == "output.txt" else path.stem
    for paper in docs:
        yield normalize(paper, source_id)


def write_exports(verified, review):
    verified_fields = [
        "reference_id", "year", "authors", "title", "journal", "doi", "editorial_url", "finding", "relevance",
        "crossref_title", "crossref_year", "crossref_journal", "crossref_type", "title_similarity", "origin_file",
    ]
    with (OUT / "artigos_verificados_doi.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=verified_fields, extrasaction="ignore")
        writer.writeheader()
        for paper in verified:
            row = {**paper, "authors": "; ".join(paper.get("authors", [])) if isinstance(paper.get("authors"), list) else paper.get("authors", "")}
            writer.writerow(row)
    review_fields = ["doi", "title", "crossref_title", "journal", "editorial_url", "status", "crossref_type", "title_similarity", "origin_file"]
    with (OUT / "dois_para_revisao_manual.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=review_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(review)


def get_crossref(paper):
    url = "https://api.crossref.org/works/" + requests.utils.quote(paper["doi"], safe="/:;()")
    response = None
    last_error = ""
    for attempt in range(4):
        time.sleep(0.35)
        try:
            response = requests.get(url, headers={"User-Agent": "PublicFinanceArticleBot/1.0 (research metadata audit)"}, timeout=25)
            if response.status_code == 200:
                break
            last_error = str(response.status_code)
            if response.status_code not in (429, 500, 502, 503, 504) or attempt == 3:
                break
            retry_after = response.headers.get("Retry-After", "")
            delay = float(retry_after) if retry_after.isdigit() else 2 ** (attempt + 1)
            time.sleep(min(delay, 30))
        except Exception as exc:
            last_error = str(exc)
            if attempt == 3:
                break
            time.sleep(2 ** attempt)
    if response is None or response.status_code != 200:
        return {"ok": False, "status": last_error or "request_failed", "crossref_type": "", "crossref_title": "", "crossref_year": None, "crossref_journal": "", "crossref_authors": []}
    try:
        message = response.json()["message"]
        publication_type = message.get("type", "")
        title = (message.get("title") or [""])[0]
        journal = (message.get("container-title") or [""])[0]
        year = (message.get("published-print", message.get("published-online", message.get("issued", {}))).get("date-parts") or [[None]])[0][0]
        authors = [" ".join(value for value in (author.get("given"), author.get("family")) if value) for author in message.get("author", [])]
        return {"ok": True, "status": 200, "crossref_type": publication_type, "crossref_title": title, "crossref_year": year, "crossref_journal": journal, "crossref_authors": authors}
    except Exception as exc:
        return {"ok": False, "status": str(exc), "crossref_type": "", "crossref_title": "", "crossref_year": None, "crossref_journal": "", "crossref_authors": []}


def simplify(text):
    text = unicodedata.normalize("NFKD", str(text).casefold())
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def main():
    # The archived mode reuses the dated Crossref audit, keeping reference IDs stable.
    if os.environ.get("FINANCAS_USE_ARCHIVED_CORPUS") == "1" and ARCHIVE.exists():
        snapshot = json.loads(ARCHIVE.read_text(encoding="utf-8"))
        verified = snapshot.get("papers", [])
        review = snapshot.get("review_records", [])
        for paper in verified + review:
            paper["origin_file"] = canonical_origin(paper.get("origin_file"))
        verified.sort(key=lambda paper: (int(paper["year"]), str(paper["title"]).casefold()))
        for index, paper in enumerate(verified, 1):
            paper["reference_id"] = index
        snapshot["papers"] = verified
        snapshot["review_records"] = review
        snapshot["verified_count"] = len(verified)
        snapshot["excluded_or_review_count"] = len(review)
        snapshot["retrieval_sources"] = [Path(str(source)).name for source in snapshot.get("retrieval_sources", [ARCHIVE.name])]
        snapshot["audit_mode"] = "archived_crossref_snapshot"
        ARCHIVE.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
        write_exports(verified, review)
        print("Using archived Crossref audit:", len(verified), "verified;", len(review), "manual/excluded; date", snapshot.get("retrieval_date"))
        return

    papers = []
    for source in SOURCES:
        if source.exists():
            papers.extend(read_papers(source))
        else:
            print("missing source", source.name)
    by_doi = {}
    for paper in papers:
        if not paper["doi"] or not paper["title"] or not paper["journal"]:
            continue
        if paper["doi"] not in by_doi or len(paper["finding"] + paper["relevance"]) > len(by_doi[paper["doi"]]["finding"] + by_doi[paper["doi"]]["relevance"]):
            by_doi[paper["doi"]] = paper
    corpus = list(by_doi.values())
    print("unique DOI candidates", len(corpus), "from", len(papers), "records")
    checks = {}
    with ThreadPoolExecutor(max_workers=1) as executor:
        futures = {executor.submit(get_crossref, paper): paper["doi"] for paper in corpus}
        for future in as_completed(futures):
            checks[futures[future]] = future.result()
    for paper in corpus:
        result = checks[paper["doi"]]
        paper.update(result)
        paper["title_similarity"] = SequenceMatcher(None, simplify(paper["title"]), simplify(paper["crossref_title"])).ratio() if result["ok"] else 0.0
        paper["title_match"] = bool(result["ok"] and paper["title_similarity"] >= 0.72)
        paper["verified_for_corpus"] = bool(paper["title_match"] and paper["journal"] and paper["editorial_url"] and result["crossref_type"] == "journal-article")
    verified = [paper for paper in corpus if paper["verified_for_corpus"]]
    review = [paper for paper in corpus if not paper["verified_for_corpus"]]
    verified.sort(key=lambda paper: (paper["year"], paper["title"].casefold()))
    for index, paper in enumerate(verified, 1):
        paper["reference_id"] = index
    snapshot = {
        "retrieval_date": time.strftime("%Y-%m-%d"),
        "retrieval_sources": [source.name for source in SOURCES],
        "candidate_count": len(corpus),
        "verified_count": len(verified),
        "excluded_or_review_count": len(review),
        "audit_mode": "live_crossref_revalidation",
        "papers": verified,
        "review_records": review,
    }
    ARCHIVE.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    write_exports(verified, review)
    print("Crossref verified title matches:", len(verified), "manual/excluded:", len(review))
    for paper in review:
        print("REVIEW", paper["doi"], paper["title"], "=>", paper["crossref_title"], paper["status"], f'{paper["title_similarity"]:.2f}')


if __name__ == "__main__":
    main()
