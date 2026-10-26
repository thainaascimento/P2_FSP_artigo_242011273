#!/usr/bin/env python3
"""Tratamento reprodutível das séries fiscais de Cascavel, Londrina e China (2014–2023).

O script não substitui valores ausentes por zero. Deflaciona fluxos anuais pela razão
entre o CPI médio/índice anual de 2023 e o do ano da observação. Salva dados tratados,
XLSX com abas editáveis, tabelas-síntese e gráficos. Execução: python3 codigo/02_transformacao_analise.py
"""
from __future__ import annotations
from pathlib import Path
from datetime import date, datetime
import json, math, re
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "dados" / "fontes_brutas"
DCA = RAW / "siconfi_dca"
TREATED = ROOT / "dados" / "tratados"
OUTPUT = ROOT / "resultados"
TREATED.mkdir(parents=True, exist_ok=True)
OUTPUT.mkdir(parents=True, exist_ok=True)
YEARS = list(range(2014, 2024))
CITIES = {4104808: "Cascavel/PR", 4113700: "Londrina/PR"}
ACCESS_DATE = "2026-10-22"


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def fetch_brazil_fx():
    """Baixa e arquiva a série WDI de câmbio anual médio BRL por USD."""
    path = RAW / "worldbank_brazil_fx_2014_2023.json"
    if not path.exists():
        url = "https://api.worldbank.org/v2/country/BRA/indicator/PA.NUS.FCRF?date=2014:2023&format=json&per_page=100"
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        payload = r.json()
        out = {"url": url, "source": "World Bank WDI", "access_date": ACCESS_DATE, "data": payload[1] if len(payload) > 1 else []}
        path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return load_json(path)


def wdi_series(obj, indicator):
    out = {}
    for row in obj.get(indicator, {}).get("data", []):
        if row.get("date") and row.get("value") is not None:
            out[int(row["date"])] = float(row["value"])
    return out


def ipca_annual_mean_index():
    """Índice mensal encadeado a partir da variação do IPCA (SGS 433); média anual."""
    obj = load_json(RAW / "ipca_sgs_433.json")
    rows = obj["data"]
    rows = sorted(rows, key=lambda x: datetime.strptime(x["data"], "%d/%m/%Y"))
    level = 100.0
    annual = {}
    counts = {}
    for row in rows:
        dt = datetime.strptime(row["data"], "%d/%m/%Y")
        level *= 1.0 + float(row["valor"].replace(",", ".")) / 100.0
        annual[dt.year] = annual.get(dt.year, 0.0) + level
        counts[dt.year] = counts.get(dt.year, 0) + 1
    annual = {y: annual[y] / counts[y] for y in annual}
    if any(counts.get(y) != 12 for y in YEARS):
        raise ValueError(f"IPCA incompleto: meses por ano = {counts}")
    return annual


def get_ibge_population():
    """Estimativa anual SIDRA até 2021; 2022/23 usam contagem censitária 2022, marcada como proxy."""
    obj = load_json(RAW / "ibge_pop_sidra.json")
    vals = {}
    for row in obj["data"][1:]:
        city = int(row["D1C"])
        year = int(row["D3C"])
        if city in CITIES and year <= 2021:
            vals[(city, year)] = float(row["V"])
    # Relação oficial enviada pelo IBGE ao TCU em 2023; população residente do Censo 2022.
    census_2022 = {4104808: 348051.0, 4113700: 555965.0}
    statuses = {}
    for city in CITIES:
        for year in YEARS:
            if year <= 2021:
                if (city, year) not in vals:
                    raise ValueError(f"População ausente no SIDRA para {city}/{year}; nenhum zero/imputação permitido")
                statuses[(city, year)] = "Estimativa anual IBGE (SIDRA 6579; var. 9324)"
            else:
                vals[(city, year)] = census_2022[city]
                statuses[(city, year)] = "Censo 2022; referência censitária usada em 2022 e como proxy de 2023 (malha TCU 2023)"
    return vals, statuses


def get_pib():
    obj = load_json(RAW / "ibge_pib_sidra.json")
    rows = obj.get("data", [])
    # O cabeçalho é a primeira linha da resposta SIDRA.
    out = {}
    for r in rows[1:]:
        city = int(r["D1C"])
        year = int(r["D3C"])
        if city in CITIES and year in YEARS and r.get("V") not in (None, "", "-"):
            out[(city, year)] = float(r["V"]) * 1000.0  # SIDRA em mil reais -> BRL
    return out


def account_value(items, prefix=None, exact_code=None, column="Receitas Brutas Realizadas"):
    hits = []
    for x in items:
        if x.get("coluna") != column:
            continue
        code = str(x.get("cod_conta", ""))
        if exact_code is not None and code == exact_code:
            hits.append(x)
        elif prefix is not None and code.startswith(prefix):
            hits.append(x)
    if not hits:
        return np.nan
    # Prefixos usados aqui designam a conta-pai, não os filhos; se mais de um tiver
    # correspondência, prefira o rótulo mais curto, evitando somar pais e subcontas.
    hits.sort(key=lambda x: (len(str(x.get("cod_conta", ""))), len(str(x.get("conta", "")))))
    return float(hits[0]["valor"])


def city_panel():
    pop, pop_status = get_ibge_population()
    pib = get_pib()
    ipca = ipca_annual_mean_index()
    rows = []
    for city, name in CITIES.items():
        for year in YEARS:
            rev_path = DCA / f"{city}_{year}_DCA-Anexo_I-C.json"
            exp_path = DCA / f"{city}_{year}_DCA-Anexo_I-E.json"
            rev = load_json(rev_path)["items"]
            exp = load_json(exp_path)["items"]
            tax = account_value(rev, prefix="RO1.1.0.0.00")
            current = account_value(rev, prefix="RO1.0.0.0.00")
            capital = account_value(rev, prefix="RO2.0.0.0.00")
            total_exp = next((float(x["valor"]) for x in exp if x.get("coluna") == "Despesas Empenhadas" and x.get("conta") in {"Despesas Exceto Intraorçamentárias", "Despesas (Exceto Intraorçamentárias)"}), np.nan)
            health = next((float(x["valor"]) for x in exp if x.get("coluna") == "Despesas Empenhadas" and x.get("conta") == "10 - Saúde"), np.nan)
            education = next((float(x["valor"]) for x in exp if x.get("coluna") == "Despesas Empenhadas" and x.get("conta") == "12 - Educação"), np.nan)
            total_all = account_value(rev, exact_code="ReceitasExcetoIntraOrcamentarias")
            if not np.isfinite(total_all):
                total_all = current + capital if np.isfinite(current) and np.isfinite(capital) else np.nan
            tr_current = account_value(rev, prefix="RO1.7.0.0.00")
            tr_capital = account_value(rev, prefix="RO2.4.0.0.00")
            # Use apenas os totais das contas-pai 1.7.0 e 2.4.0. As subcontas são
            # mantidas no JSON bruto, não somadas aqui, para não duplicar agregados.
            factor = ipca[2023] / ipca[year]
            row = {
                "pais": "Brasil", "unidade": name, "codigo_ibge": city, "ano": year,
                "populacao": pop.get((city, year), np.nan), "status_populacao": pop_status.get((city, year), "ausente"),
                "receita_total_nominal_brl": total_all,
                "receita_tributaria_nominal_brl": tax,
                "transferencias_correntes_nominal_brl": tr_current,
                "transferencias_capital_nominal_brl": tr_capital,
                "transferencias_correntes_mais_capital_nominal_brl": tr_current + tr_capital if np.isfinite(tr_current) and np.isfinite(tr_capital) else np.nan,
                "despesa_empenhada_nominal_brl": total_exp,
                "despesa_saude_empenhada_nominal_brl": health,
                "despesa_educacao_empenhada_nominal_brl": education,
                "pib_municipal_nominal_brl": pib.get((city, year), np.nan),
                "deflator_ipca_base_2023": factor,
                "ipca_indice_medio_anual_encadeado": ipca[year],
                "url_dca_receita": load_json(rev_path).get("_metadata", {}).get("source_url", ""),
                "url_dca_despesa": load_json(exp_path).get("_metadata", {}).get("source_url", ""),
            }
            for field in ["receita_total", "receita_tributaria", "transferencias_correntes", "transferencias_capital", "transferencias_correntes_mais_capital", "despesa_empenhada", "despesa_saude_empenhada", "despesa_educacao_empenhada", "pib_municipal"]:
                n = field + "_nominal_brl"
                if n in row:
                    row[field + "_real_2023_brl"] = row[n] * factor if np.isfinite(row[n]) else np.nan
            if np.isfinite(row["populacao"]) and row["populacao"] > 0:
                for field in ["receita_total", "receita_tributaria", "transferencias_correntes_mais_capital", "despesa_empenhada", "despesa_saude_empenhada", "despesa_educacao_empenhada", "pib_municipal"]:
                    key = field + "_real_2023_brl"
                    row[field + "_real_2023_brl_pc"] = row.get(key, np.nan) / row["populacao"] if np.isfinite(row.get(key, np.nan)) else np.nan
            else:
                for field in ["receita_total", "receita_tributaria", "transferencias_correntes_mais_capital", "despesa_empenhada", "despesa_saude_empenhada", "despesa_educacao_empenhada", "pib_municipal"]:
                    row[field + "_real_2023_brl_pc"] = np.nan
            row["transferencias_pct_receita_total"] = 100 * row["transferencias_correntes_mais_capital_nominal_brl"] / total_all if np.isfinite(total_all) and total_all else np.nan
            row["tributos_pct_receita_total"] = 100 * tax / total_all if np.isfinite(total_all) and total_all else np.nan
            row["transferencias_pct_pib"] = 100 * row["transferencias_correntes_mais_capital_nominal_brl"] / row["pib_municipal_nominal_brl"] if np.isfinite(row["pib_municipal_nominal_brl"]) and row["pib_municipal_nominal_brl"] else np.nan
            row["transferencias_pct_despesa"] = 100 * row["transferencias_correntes_mais_capital_nominal_brl"] / total_exp if np.isfinite(total_exp) and total_exp else np.nan
            rows.append(row)
    df = pd.DataFrame(rows)
    return df, ipca


def china_panel():
    mof = pd.read_csv(RAW / "china_financas_mof_2014_2023.csv")
    wdi_path = RAW / "worldbank_china_macro_2014_2023.json"
    wdi = load_json(wdi_path)
    code = "NY.GDP.PCAP.KD"
    if code not in wdi:
        url = f"https://api.worldbank.org/v2/country/CHN/indicator/{code}?date=2014:2023&format=json&per_page=100"
        r = requests.get(url, timeout=90); r.raise_for_status(); payload = r.json()
        wdi[code] = {"url": url, "source": "World Bank WDI", "access_date": ACCESS_DATE, "data": payload[1] if len(payload) > 1 else []}
        wdi_path.write_text(json.dumps(wdi, ensure_ascii=False, indent=2), encoding="utf-8")
    fx_obj = fetch_brazil_fx()
    fx_br = {}
    for r in fx_obj.get("data", []):
        if r.get("date") and r.get("value") is not None:
            fx_br[int(r["date"])] = float(r["value"])
    cpi = wdi_series(wdi, "FP.CPI.TOTL")
    fx_cn = wdi_series(wdi, "PA.NUS.FCRF")
    gdp_usd = wdi_series(wdi, "NY.GDP.MKTP.CD")
    gdp_pc_constant = wdi_series(wdi, "NY.GDP.PCAP.KD")
    pop_cn = wdi_series(wdi, "SP.POP.TOTL")
    rows = []
    for _, m in mof.iterrows():
        y = int(m["ano"])
        f = cpi[2023] / cpi[y]
        own = float(m["receita_local_propria_100m_cny"]) * 1e8
        tr = float(m["transferencias_centro_para_local_100m_cny"]) * 1e8
        localrev = float(m["receita_orcamento_geral_local_100m_cny"]) * 1e8
        expense = float(m["despesa_orcamento_geral_local_100m_cny"]) * 1e8
        fx = fx_cn[y]
        gdp_local = gdp_usd[y] * fx
        row = {
            "pais": "China", "unidade": "Agregado de governos locais", "ano": y,
            "populacao": pop_cn.get(y, np.nan), "status_populacao": "World Bank WDI, população anual nacional",
            "receita_local_propria_nominal_cny": own,
            "transferencias_centro_para_local_nominal_cny": tr,
            "receita_orcamento_geral_local_nominal_cny": localrev,
            "despesa_orcamento_geral_local_nominal_cny": expense,
            "pib_nacional_nominal_usd": gdp_usd[y], "cambio_cny_por_usd_anual": fx,
            "pib_nacional_per_capita_constante_2015_usd": gdp_pc_constant.get(y, np.nan),
            "pib_nacional_total_constante_2015_usd": gdp_pc_constant.get(y, np.nan) * pop_cn.get(y, np.nan),
            "pib_nacional_nominal_cny": gdp_local,
            "cpi_indice_anual_wdi_2010_100": cpi[y], "deflator_cpi_base_2023": f,
            "url_fonte_financas": m["source_url"], "unidade_fonte_financas": m["unidade"],
            "revisao_2022": ("Recebimento local de março/2023: 97.144,75 亿元; despesa central final de julho/2023: 96.941,82 亿元. Diferença de fechamento; conceitos mantidos separados." if y == 2022 else ""),
            "url_revisao_transferencia_2022_final": (str(m.get("url_revisao_final_2022", "")) if y == 2022 else ""),
        }
        row["pib_nacional_corrente_cpi_deflacionado_2023_cny"] = gdp_local * f
        for field in ["receita_local_propria", "transferencias_centro_para_local", "receita_orcamento_geral_local", "despesa_orcamento_geral_local"]:
            nom = field + "_nominal_cny"
            real_key = field + "_real_2023_cny"
            row[real_key] = row[nom] * f
        if row["populacao"] and row["populacao"] > 0:
            for field in ["receita_local_propria", "transferencias_centro_para_local", "receita_orcamento_geral_local", "despesa_orcamento_geral_local"]:
                key = field + "_real_2023_cny"
                row[field + "_real_2023_cny_pc"] = row[key] / row["populacao"] if key in row else np.nan
        else:
            for field in ["receita_local_propria", "transferencias_centro_para_local", "receita_orcamento_geral_local", "despesa_orcamento_geral_local"]:
                row[field + "_real_2023_cny_pc"] = np.nan
        row["transferencias_pct_receita_local"] = 100 * tr / localrev if localrev else np.nan
        row["receita_propria_pct_receita_local"] = 100 * own / localrev if localrev else np.nan
        row["transferencias_pct_despesa_local"] = 100 * tr / expense if expense else np.nan
        row["transferencias_pct_pib_nacional"] = 100 * tr / gdp_local if gdp_local else np.nan
        row["despesa_local_pct_pib_nacional"] = 100 * expense / gdp_local if gdp_local else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def summary_metrics(br, cn, fx_br_2023):
    records = []
    for _, d in br.groupby("unidade"):
        d = d.sort_values("ano"); a, b = d.iloc[0], d.iloc[-1]
        for label, col, unit in [
            ("Transferências correntes + capital reais per capita", "transferencias_correntes_mais_capital_real_2023_brl_pc", "BRL 2023/pessoa"),
            ("Transferências correntes + capital per capita (USD de 2023)", "transferencias_real_2023_usd_mercado_pc", "USD 2023/pessoa"),
            ("Transferências / receita total", "transferencias_pct_receita_total", "%"),
            ("Tributos / receita total", "tributos_pct_receita_total", "%"),
            ("Transferências / PIB municipal", "transferencias_pct_pib", "%"),
            ("Despesas empenhadas reais per capita", "despesa_empenhada_real_2023_brl_pc", "BRL 2023/pessoa"),
        ]:
            x0, x1 = a[col], b[col]
            records.append({"país": "Brasil", "unidade": a["unidade"], "indicador": label, "2014": x0, "2023": x1, "variação_%": (x1 / x0 - 1) * 100 if pd.notna(x0) and x0 else np.nan, "unidade_medida": unit})
        for label, col, unit in [("Receita tributária real total", "receita_tributaria_real_2023_brl", "BRL 2023"), ("Transferências correntes + capital reais totais", "transferencias_correntes_mais_capital_real_2023_brl", "BRL 2023"), ("Transferências correntes + capital totais (USD de 2023)", "transferencias_real_2023_usd_mercado", "USD 2023"), ("PIB municipal real", "pib_municipal_real_2023_brl", "BRL 2023")]:
            x0, x1 = a[col], b[col]
            records.append({"país": "Brasil", "unidade": a["unidade"], "indicador": label, "2014": x0, "2023": x1, "variação_%": (x1 / x0 - 1) * 100 if pd.notna(x0) and x0 else np.nan, "unidade_medida": unit})
    d = cn.sort_values("ano"); a, b = d.iloc[0], d.iloc[-1]
    for label, col, unit in [
        ("Transferências centrais reais per capita", "transferencias_centro_para_local_real_2023_cny_pc", "CNY 2023/pessoa"),
        ("Transferências centrais per capita (USD de 2023)", "transferencias_real_2023_usd_mercado_pc", "USD 2023/pessoa"),
        ("Transferências / receita local", "transferencias_pct_receita_local", "%"),
        ("Receita própria / receita local", "receita_propria_pct_receita_local", "%"),
        ("Transferências / despesa local", "transferencias_pct_despesa_local", "%"),
        ("Transferências / PIB nacional", "transferencias_pct_pib_nacional", "%"),
        ("Despesa local / PIB nacional", "despesa_local_pct_pib_nacional", "%"),
    ]:
        x0, x1 = a[col], b[col]
        records.append({"país": "China", "unidade": "Agregado de governos locais", "indicador": label, "2014": x0, "2023": x1, "variação_%": (x1 / x0 - 1) * 100 if pd.notna(x0) and x0 else np.nan, "unidade_medida": unit})
    for label, col, unit in [("Receita local própria real", "receita_local_propria_real_2023_cny", "CNY 2023"), ("Transferências centrais reais", "transferencias_centro_para_local_real_2023_cny", "CNY 2023"), ("Transferências centrais totais (USD de 2023)", "transferencias_real_2023_usd_mercado", "USD 2023"), ("Despesa local real", "despesa_orcamento_geral_local_real_2023_cny", "CNY 2023")]:
        x0, x1 = a[col], b[col]
        records.append({"país": "China", "unidade": "Agregado de governos locais", "indicador": label, "2014": x0, "2023": x1, "variação_%": (x1 / x0 - 1) * 100 if pd.notna(x0) and x0 else np.nan, "unidade_medida": unit})
    return pd.DataFrame(records)


def var_dictionary():
    rows = [
        ("receita_total_nominal_brl", "Receitas municipais realizadas, exceto intraorçamentárias; quando o agregado total não é fornecido no DCA antigo, soma receitas correntes e de capital", "BRL corrente", "Siconfi/Finbra DCA Anexo I-C; conta total ou agregados 1.0 e 2.0", "2014–2023; dois municípios"),
        ("receita_tributaria_nominal_brl", "Receita tributária própria municipal agregada, rubrica 1.1.0.0", "BRL corrente", "Siconfi/Finbra DCA I-C; 1.1.0.0 Receita Tributária/Impostos, Taxas e Contribuições de Melhoria", "2014–2023; dois municípios"),
        ("transferencias_correntes_mais_capital_nominal_brl", "Soma das contas-pai de transferências correntes (1.7.0) e de capital (2.4.0); categoria ampla, não equivale exclusivamente a transferências intergovernamentais", "BRL corrente", "Siconfi/Finbra DCA I-C; os arquivos brutos preservam as subcontas e origens", "2014–2023; dois municípios"),
        ("despesa_empenhada_nominal_brl", "Despesa total empenhada, exceto intraorçamentária, todas as funções", "BRL corrente", "Siconfi/Finbra DCA Anexo I-E; Despesas Empenhadas", "2014–2023; dois municípios"),
        ("despesa_saude_empenhada_nominal_brl", "Despesa empenhada na função 10 Saúde", "BRL corrente", "Siconfi/Finbra DCA I-E, função 10", "2014–2023; dois municípios"),
        ("despesa_educacao_empenhada_nominal_brl", "Despesa empenhada na função 12 Educação", "BRL corrente", "Siconfi/Finbra DCA I-E, função 12", "2014–2023; dois municípios"),
        ("pib_municipal_nominal_brl", "Produto interno bruto municipal a preços correntes (SIDRA em mil reais, convertido a reais)", "BRL corrente", "IBGE/SIDRA tabela 5938, variável 37", "2014–2023; dois municípios; série base 2010"),
        ("populacao", "Estimativa residente anual 2014–2021; Censo 2022 para 2022 e população censitária em malha TCU 2023 como proxy para 2023", "pessoas", "IBGE/SIDRA 6579 variável 9324; Censo 2022/arquivo TCU", "2014–2023; referência censitária/proxy 2022–23"),
        ("*_real_2023_brl", "Fluxo nominal multiplicado por média do índice mensal IPCA encadeado em 2023 dividida pela média do ano t", "BRL a preço médio de 2023", "BCB SGS 433, IPCA mensal", "2014–2023"),
        ("*_real_2023_brl_pc", "Fluxo em BRL de 2023 dividido pela população do mesmo ano (proxy explicitado em 2023)", "BRL 2023/pessoa", "Derivado; IBGE + BCB", "2014–2023"),
        ("transferencias_real_2023_usd_mercado", "Transferências reais a preços de 2023 convertidas pela taxa média anual de câmbio de 2023; não é paridade de poder de compra", "USD 2023", "WDI PA.NUS.FCRF; 4,99438 BRL/USD e 7,083998 CNY/USD em 2023", "2014–2023; totais fiscais"),
        ("transferencias_real_2023_usd_mercado_pc", "Transferências reais em USD de 2023 divididas pela população da unidade; 2023 municipal usa proxy censitária 2022", "USD 2023/pessoa", "Derivado; BCB/IBGE/WDI", "2014–2023"),
        ("receita_local_propria_nominal_cny", "Receita própria do orçamento público geral local chinês (本级收入), inclui componentes fiscais e não fiscais", "CNY corrente", "Ministry of Finance; relatório de execução anual central-local", "2014–2023; agregado nacional local"),
        ("transferencias_centro_para_local_nominal_cny", "Transferências centrais reportadas como receita local no orçamento público geral (tax rebates e pagamentos de transferência)", "CNY corrente", "Ministry of Finance; relatórios anuais central-local", "2014–2023; agregado nacional local; revisão 2022 documentada"),
        ("receita_orcamento_geral_local_nominal_cny", "Receita local do orçamento público geral conforme reportada pelo MOF", "CNY corrente", "Ministry of Finance; 亿元 × 100 milhões", "2014–2023"),
        ("despesa_orcamento_geral_local_nominal_cny", "Despesa local do orçamento público geral", "CNY corrente", "Ministry of Finance; 亿元 × 100 milhões", "2014–2023"),
        ("pib_nacional_nominal_usd", "PIB nominal corrente nacional da China", "USD corrente", "World Bank WDI NY.GDP.MKTP.CD", "2014–2023"),
        ("pib_nacional_per_capita_constante_2015_usd", "PIB nacional per capita em volume, série oficial a preços constantes de 2015", "USD constantes de 2015/pessoa", "World Bank WDI NY.GDP.PCAP.KD", "2014–2023; atividade econômica China"),
        ("pib_nacional_total_constante_2015_usd", "PIB nacional em volume, calculado como PIB per capita constante × população WDI", "USD constantes de 2015", "Derivado; WDI NY.GDP.PCAP.KD × SP.POP.TOTL", "2014–2023"),
        ("pib_nacional_corrente_cpi_deflacionado_2023_cny", "PIB corrente convertido a CNY pela taxa anual e ajustado pelo CPI; proxy de valor corrente, não medida de volume do PIB", "CNY de 2023 ajustado pelo CPI", "WDI NY.GDP.MKTP.CD × PA.NUS.FCRF; deflator FP.CPI.TOTL", "2014–2023; não usar como PIB real"),
        ("cpi_indice_anual_wdi_2010_100", "Índice anual de preços ao consumidor; CPI 2010=100, série WDI baseada em fonte oficial", "Índice", "World Bank WDI FP.CPI.TOTL", "2014–2023; razão CPI_2023/CPI_t"),
        ("cambio_cny_por_usd_anual", "Taxa média anual oficial de CNY por USD", "CNY/USD", "World Bank WDI PA.NUS.FCRF", "2014–2023"),
        ("transferencias_pct_pib_nacional", "Transferências centrais para locais divididas pelo PIB nominal do país", "% PIB", "Derivado de MOF/WDI; a escala nacional não equivale ao PIB municipal", "2014–2023"),
    ]
    return pd.DataFrame(rows, columns=["variável", "definição", "unidade", "fonte/transformação", "período/cobertura"])


def style_workbook(path: Path):
    wb = load_workbook(path)
    for ws in wb.worksheets:
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
        ws.row_dimensions[1].height = 32
        for cell in ws[1]:
            cell.font = Font(name="Aptos", bold=True, color="FFFFFF", size=10)
            cell.fill = PatternFill("solid", fgColor="16324F")
            cell.alignment = Alignment(wrap_text=True, vertical="center")
        for col in ws.columns:
            letter = get_column_letter(col[0].column)
            vals = [len(str(c.value)) for c in col[:100] if c.value is not None]
            ws.column_dimensions[letter].width = min(max(12, max(vals, default=12) + 2), 42)
        for row in ws.iter_rows(min_row=2):
            for c in row:
                if isinstance(c.value, (float, int)) and c.value is not None:
                    c.number_format = '#,##0.00;[Red]-#,##0.00;–'
                if c.column == 1:
                    c.alignment = Alignment(vertical="top")
    wb.save(path)


def make_figures(br, cn):
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.titlesize": 13, "axes.labelsize": 10})
    # Transferências como proporção das receitas, comparação de escala relativa.
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    for name, g in br.groupby("unidade"):
        ax.plot(g["ano"], g["transferencias_pct_receita_total"], marker="o", linewidth=2, label=name)
    ax.plot(cn["ano"], cn["transferencias_pct_receita_local"], marker="s", linewidth=2, label="China — governos locais")
    ax.set(title="Transferências como proporção da receita orçamentária reportada", xlabel="Ano", ylabel="% da receita", xticks=YEARS)
    ax.legend(frameon=False); fig.tight_layout(); fig.savefig(OUTPUT / "figura_01_transferencias_participacao.png", dpi=220); plt.close(fig)
    # Índice real 2014=100, séries em moeda local; sem comparar níveis nominais entre moedas.
    fig, ax = plt.subplots(figsize=(10, 5.8))
    colors = {"Cascavel/PR": "#2563eb", "Londrina/PR": "#ea580c"}
    for name, g in br.groupby("unidade"):
        g=g.sort_values("ano")
        for col, ls in [("transferencias_correntes_mais_capital_real_2023_brl", "-"), ("receita_tributaria_real_2023_brl", "--"), ("despesa_empenhada_real_2023_brl", ":")]:
            ax.plot(g["ano"], 100*g[col]/g[col].iloc[0], color=colors[name], linestyle=ls, marker="o")
    for col, ls in [("transferencias_centro_para_local_real_2023_cny", "-"), ("receita_local_propria_real_2023_cny", "--"), ("despesa_orcamento_geral_local_real_2023_cny", ":")]:
        ax.plot(cn["ano"], 100*cn[col]/cn[col].iloc[0], color="#15803d", linestyle=ls, marker="s")
    ax.set(title="Evolução real dos fluxos fiscais — índice 2014 = 100", xlabel="Ano", ylabel="Índice", xticks=YEARS)
    unit_handles = [Line2D([0], [0], color=c, linewidth=2.5, label=lab) for lab, c in [("Cascavel/PR", colors["Cascavel/PR"]), ("Londrina/PR", colors["Londrina/PR"]), ("China — governos locais", "#15803d")]]
    flow_handles = [Line2D([0], [0], color="#505050", linewidth=2, linestyle=ls, label=lab) for lab, ls in [("Transferências", "-"), ("Tributos / receita própria", "--"), ("Despesas", ":")]]
    unit_legend = ax.legend(handles=unit_handles, loc="upper center", bbox_to_anchor=(0.5, 1.23), ncol=3, fontsize=8, frameon=False)
    ax.add_artist(unit_legend)
    ax.legend(handles=flow_handles, loc="upper center", bbox_to_anchor=(0.5, 1.12), ncol=3, fontsize=8, frameon=False)
    fig.tight_layout(rect=[0, 0, 1, 0.86]); fig.savefig(OUTPUT / "figura_02_indices_reais.png", dpi=220); plt.close(fig)
    # Per capita em moeda local constante, painéis separados por moeda.
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.8))
    for name, g in br.groupby("unidade"):
        axes[0].plot(g["ano"], g["transferencias_correntes_mais_capital_real_2023_brl_pc"], marker="o", label=name)
    axes[0].set(title="Brasil: transferência por habitante", ylabel="BRL médios de 2023/pessoa", xlabel="Ano", xticks=YEARS)
    axes[0].legend(frameon=False)
    axes[1].plot(cn["ano"], cn["transferencias_centro_para_local_real_2023_cny_pc"], color="#15803d", marker="s", label="China — governos locais")
    axes[1].set(title="China: transferência por habitante", ylabel="CNY médios de 2023/pessoa", xlabel="Ano", xticks=YEARS)
    axes[1].legend(frameon=False)
    fig.suptitle("Valores per capita em moeda local real — escalas não são diretamente comparáveis", y=1.03, fontsize=12)
    fig.tight_layout(); fig.savefig(OUTPUT / "figura_03_transferencias_pc.png", dpi=220, bbox_inches="tight"); plt.close(fig)


def main():
    br, ipca = city_panel()
    cn = china_panel()
    br_fx_obj = fetch_brazil_fx()
    fx_br = {int(r["date"]): float(r["value"]) for r in br_fx_obj.get("data", []) if r.get("date") and r.get("value") is not None}[2023]
    # Converte moedas apenas pelo câmbio anual de mercado do ano-base 2023; mantém moedas locais.
    br["transferencias_real_2023_usd_mercado"] = br["transferencias_correntes_mais_capital_real_2023_brl"] / fx_br
    br["transferencias_real_2023_usd_mercado_pc"] = br["transferencias_real_2023_usd_mercado"] / br["populacao"]
    br["receita_tributaria_real_2023_usd_mercado"] = br["receita_tributaria_real_2023_brl"] / fx_br
    br["despesa_empenhada_real_2023_usd_mercado"] = br["despesa_empenhada_real_2023_brl"] / fx_br
    fx_cn_2023 = float(wdi_series(load_json(RAW / "worldbank_china_macro_2014_2023.json"), "PA.NUS.FCRF")[2023])
    cn["transferencias_real_2023_usd_mercado"] = cn["transferencias_centro_para_local_real_2023_cny"] / fx_cn_2023
    cn["transferencias_real_2023_usd_mercado_pc"] = cn["transferencias_real_2023_usd_mercado"] / cn["populacao"]
    cn["receita_local_propria_real_2023_usd_mercado"] = cn["receita_local_propria_real_2023_cny"] / fx_cn_2023
    cn["despesa_local_real_2023_usd_mercado"] = cn["despesa_orcamento_geral_local_real_2023_cny"] / fx_cn_2023
    summary = summary_metrics(br, cn, fx_br)
    dictionary = var_dictionary()
    br_path = TREATED / "painel_municipal_2014_2023.csv"
    cn_path = TREATED / "painel_china_2014_2023.csv"
    summary_path = OUTPUT / "tabela_resumo_2014_2023.csv"
    br.to_csv(br_path, index=False, encoding="utf-8-sig", float_format="%.4f")
    cn.to_csv(cn_path, index=False, encoding="utf-8-sig", float_format="%.4f")
    summary.to_csv(summary_path, index=False, encoding="utf-8-sig", float_format="%.4f")
    dictionary_path = TREATED / "dicionario_variaveis.csv"
    dictionary.to_csv(dictionary_path, index=False, encoding="utf-8-sig")
    book = ROOT / "dados" / "base_atualizada_232037730.xlsx"
    with pd.ExcelWriter(book, engine="openpyxl") as writer:
        br.to_excel(writer, index=False, sheet_name="Brasil_Municipios")
        cn.to_excel(writer, index=False, sheet_name="China_Governos_Locais")
        summary.to_excel(writer, index=False, sheet_name="Comparativo_Resumo")
        dictionary.to_excel(writer, index=False, sheet_name="Dicionario")
        pd.read_csv(RAW / "china_financas_mof_2014_2023.csv").to_excel(writer, index=False, sheet_name="China_Fontes_MOF")
    style_workbook(book)
    make_figures(br, cn)
    # QA: 20 município-ano observações por painel; core series não pode conter zero artificial.
    assert len(br) == 20 and br.groupby("unidade")["ano"].nunique().eq(10).all()
    assert len(cn) == 10 and cn["ano"].nunique() == 10
    core_br = ["receita_total_nominal_brl", "receita_tributaria_nominal_brl", "transferencias_correntes_mais_capital_nominal_brl", "despesa_empenhada_nominal_brl", "pib_municipal_nominal_brl"]
    if br[core_br].isna().any().any():
        raise ValueError("Há ausências em séries fiscais/PIB centrais; verificar em vez de preencher com zero")
    if cn[["receita_local_propria_nominal_cny", "transferencias_centro_para_local_nominal_cny", "receita_orcamento_geral_local_nominal_cny", "despesa_orcamento_geral_local_nominal_cny"]].isna().any().any():
        raise ValueError("Há ausências em séries fiscais chinesas; verificar em vez de preencher com zero")
    qa = {
        "access_date": ACCESS_DATE,
        "years": YEARS,
        "brazil_rows": int(len(br)), "china_rows": int(len(cn)),
        "brazil_missing_core": int(br[core_br].isna().sum().sum()),
        "china_missing_core": int(cn[["receita_local_propria_nominal_cny", "transferencias_centro_para_local_nominal_cny", "receita_orcamento_geral_local_nominal_cny", "despesa_orcamento_geral_local_nominal_cny"]].isna().sum().sum()),
        "cpi_base_year": 2023, "brazil_fx_2023_brl_per_usd": fx_br,
        "china_fx_2023_cny_per_usd": fx_cn_2023,
        "population_2023_note": "IBGE Censo 2022 / lista TCU 2023; valor não é estimativa populacional anual de 2023.",
        "outputs": [str(br_path), str(cn_path), str(summary_path), str(book)],
    }
    (OUTPUT / "qa_tratamento.json").write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding="utf-8")
    make_readme = OUTPUT / "resumo_numerico_tratamento.txt"
    make_readme.write_text("\n".join([
        "Painel fiscal Brasil–China, 2014–2023 — QA",
        f"Acesso: {ACCESS_DATE}; deflatores em preços médios de 2023.",
        f"Cascavel/Londrina: {len(br)} observações; China: {len(cn)} observações; faltantes fiscais centrais=0.",
        f"Câmbio 2023: BRL/USD={fx_br:.6f}; CNY/USD={fx_cn_2023:.6f}. Conversões em USD de mercado, não PPC.",
        "2023 população municipal usa população censitária 2022 publicada na relação TCU 2023, explicitamente proxy.",
        "Comparação é descritiva: rubricas brasileiras 1.7+2.4 são transferências correntes/de capital amplas, não exclusivamente intergovernamentais; China é agregado nacional de transferências centrais para governos locais. Definições e níveis não são plenamente harmonizados.",
        "Não estima efeito causal nem regressão: dez observações anuais por série não sustentam identificação do efeito flypaper.",
        f"Arquivos: {br_path.name}; {cn_path.name}; {book.name}; figuras em {OUTPUT}."
    ]) + "\n", encoding="utf-8")
    print(json.dumps(qa, ensure_ascii=False, indent=2))
    print("\nResumo 2014–2023:")
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
