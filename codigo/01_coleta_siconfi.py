#!/usr/bin/env python3
"""Download annual DCA revenue and function-expenditure annexes via STN Open Data API.
Retrieved 2026-10-22. The API documentation specifies one request per second.
"""
from pathlib import Path
from datetime import date
import json, time, requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "dados" / "fontes_brutas" / "siconfi_dca"
RAW.mkdir(parents=True, exist_ok=True)
BASE = "https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/dca"
ENTITIES = {4104808: "Cascavel-PR", 4113700: "Londrina-PR"}
YEARS = range(2014, 2026)
ANNEXES = ["DCA-Anexo I-C", "DCA-Anexo I-E"]
s = requests.Session()
for entity in ENTITIES:
    for year in YEARS:
        for annex in ANNEXES:
            f = RAW / f"{entity}_{year}_{annex.replace(' ', '_')}.json"
            if f.exists() and f.stat().st_size > 20:
                continue
            response = s.get(BASE, params={"an_exercicio": year, "id_ente": entity, "no_anexo": annex}, timeout=60)
            response.raise_for_status()
            payload = response.json()
            payload["_metadata"] = {
                "source_url": response.url,
                "access_date": date.today().isoformat(),
                "entity_ibge": entity,
                "year": year,
                "annex": annex,
            }
            f.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"{entity} {year} {annex}: {payload.get('count', len(payload.get('items', [])))} records", flush=True)
            # At least one second between STN API requests (official stated limit).
            time.sleep(1.05)
print("Collection complete.")
