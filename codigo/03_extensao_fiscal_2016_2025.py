#!/usr/bin/env python3
"""Extensão fiscal de 10 exercícios completos, 2016–2025.

O painel sincronizado com PIB municipal permanece em 2014–2023. Este script cria
uma extensão fiscal separada no período mais recente com DCA e contas chinesas
publicadas (2016–2025), sem extrapolar PIB municipal inexistente em 2024–2025.
Valores reais: IPCA Brasil e CPI WDI China, média anual, ano-base 2025.
Conversão em USD: câmbio médio de mercado WDI de 2025 (não PPC).
Execute: python3 codigo/03_extensao_fiscal_2016_2025.py
"""
from pathlib import Path
from datetime import date, datetime
import importlib.util, json, math, time
import numpy as np
import pandas as pd
import requests
import openpyxl
from openpyxl import load_workbook
from openpyxl.comments import Comment
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "dados" / "fontes_brutas"
DCA = RAW / "siconfi_dca"
TREATED = ROOT / "dados" / "tratados"
OUT = ROOT / "resultados"
for p in (RAW, DCA, TREATED, OUT): p.mkdir(parents=True, exist_ok=True)
YEARS = list(range(2016, 2026))
CITIES = {4104808: "Cascavel/PR", 4113700: "Londrina/PR"}
TODAY = date.today().isoformat()

# Reutiliza a regra explícita de contas já validada no painel-base.
spec = importlib.util.spec_from_file_location("transform", ROOT / "codigo" / "02_transformacao_analise.py")
transform = importlib.util.module_from_spec(spec)
spec.loader.exec_module(transform)
account_value = transform.account_value


def save_json(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def collect_sidra_population():
    path = RAW / "ibge_pop_sidra_2014_2025.json"
    url = "https://apisidra.ibge.gov.br/values/t/6579/n6/4104808,4113700/v/9324/p/2014-2025"
    if not path.exists():
        r = requests.get(url, timeout=90); r.raise_for_status()
        save_json(path, {"url": url, "access_date": TODAY, "data": r.json()})
    d = json.loads(path.read_text(encoding="utf-8"))
    vals = {(int(r["D1C"]), int(r["D3C"])): float(r["V"]) for r in d["data"][1:] if r.get("D3C") and r.get("V") not in (None, "", "-")}
    # SIDRA não publica estimativa anual para 2022/2023 nesta tabela após o Censo.
    # Adota-se a população censitária de 2022 para esses dois anos, explicitamente marcada.
    census = {4104808: 348051.0, 4113700: 555965.0}
    pop, status = {}, {}
    for city in CITIES:
        for y in YEARS:
            if (city, y) in vals:
                pop[(city, y)] = vals[(city, y)]
                status[(city, y)] = "IBGE/SIDRA 6579 variável 9324; estimativa anual"
            elif y in (2022, 2023):
                pop[(city, y)] = census[city]
                status[(city, y)] = "Censo Demográfico 2022; proxy censitária documentada para 2023"
            else:
                raise ValueError(f"População ausente para {city}/{y}; sem imputação não documentada")
    return pop, status


def collect_ipca():
    path = RAW / "ipca_sgs_433_2014_2025.json"
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados"
    if not path.exists():
        r = requests.get(url, params={"formato":"json", "dataInicial":"01/01/2014", "dataFinal":"31/12/2025"}, timeout=90)
        r.raise_for_status()
        save_json(path, {"url":r.url, "source":"Banco Central do Brasil, SGS 433", "access_date":TODAY, "data":r.json()})
    rows = json.loads(path.read_text(encoding="utf-8"))["data"]
    rows.sort(key=lambda r: datetime.strptime(r["data"], "%d/%m/%Y"))
    level, annual, count = 100.0, {}, {}
    for r in rows:
        dt = datetime.strptime(r["data"], "%d/%m/%Y")
        level *= 1 + float(r["valor"].replace(",", "."))/100
        annual[dt.year] = annual.get(dt.year, 0.0) + level
        count[dt.year] = count.get(dt.year, 0) + 1
    annual = {y: annual[y]/count[y] for y in annual}
    if any(count.get(y) != 12 for y in YEARS): raise ValueError(f"IPCA mensal incompleto: {count}")
    return annual


def collect_wdi():
    codes = ["NY.GDP.MKTP.CD", "NY.GDP.PCAP.KD", "SP.POP.TOTL", "FP.CPI.TOTL", "PA.NUS.FCRF"]
    path = RAW / "worldbank_china_macro_2014_2025.json"
    url_base = "https://api.worldbank.org/v2/country/CHN/indicator/{code}?date=2014:2025&format=json&per_page=100"
    obj = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    changed = False
    for code in codes:
        if code not in obj:
            url = url_base.format(code=code)
            r=requests.get(url, timeout=90); r.raise_for_status(); payload=r.json()
            obj[code] = {"url":url, "source":"World Bank WDI", "access_date":TODAY, "data":payload[1] if len(payload)>1 else []}
            changed = True
    if changed or not path.exists(): save_json(path,obj)
    d=obj
    out={}
    for code,meta in d.items():
        out[code]={int(r["date"]):float(r["value"]) for r in meta["data"] if r.get("date") and r.get("value") is not None}
    for code in codes:
        if 2025 not in out.get(code,{}): raise ValueError(f"WDI {code} não tem valor de 2025")
    return out, d


def make_china_source():
    # Fluxos locais são recebimentos reportados no relatório anual central-local.
    # Os valores finais de despesa central com transferências ficam em coluna separada.
    old = pd.read_csv(RAW / "china_financas_mof_2014_2023.csv")
    rows = old.to_dict(orient="records")
    rows += [
      {"ano":2024,"receita_local_propria_100m_cny":119266.41,"transferencias_centro_para_local_100m_cny":100397.16,"receita_orcamento_geral_local_100m_cny":219663.57,"despesa_orcamento_geral_local_100m_cny":243892.07,"unidade":"亿元 (100 milhões de CNY)","source_url":"https://www.mof.gov.cn/zhengwuxinxi/caizhengxinwen/202503/t20250306_3959380.htm","observacao":"Execução do orçamento público geral local 2024; recebimento reportado = receita própria + transferências do governo central.","transferencia_central_final_100m_cny":np.nan,"url_revisao_final_transferencias":""},
      {"ano":2025,"receita_local_propria_100m_cny":122082.26,"transferencias_centro_para_local_100m_cny":101925.14,"receita_orcamento_geral_local_100m_cny":224007.40,"despesa_orcamento_geral_local_100m_cny":244361.18,"unidade":"亿元 (100 milhões de CNY)","source_url":"https://www.mof.gov.cn/zhengwuxinxi/caizhengxinwen/202603/t20260316_3985331.htm","observacao":"Execução reportada em mar/2026; transferência recebida localmente (101925.14) mantida distinta da despesa central final (101835.49), publicada em jul/2026.","transferencia_central_final_100m_cny":101835.49,"url_revisao_final_transferencias":"http://yss.mof.gov.cn/2025zyjs/202607/t20260715_3993596.htm"}
    ]
    # Harmoniza o esquema bruto preservando as observações e URLs históricas.
    cols=list(dict.fromkeys([*old.columns, "transferencia_central_final_100m_cny", "url_revisao_final_transferencias"]))
    d=pd.DataFrame(rows)
    for c in cols:
        if c not in d: d[c]=np.nan if c.endswith("_100m_cny") else ""
    # Copia a URL final de 2022 para a coluna harmonizada sem apagar o campo legado.
    for i,r in d.iterrows():
        if int(r["ano"])==2022:
            d.at[i,"transferencia_central_final_100m_cny"]=96941.82
            d.at[i,"url_revisao_final_transferencias"]="https://www.mof.gov.cn/zhengwuxinxi/caizhengxinwen/202307/t20230704_3894361.htm"
    d=d[cols].sort_values("ano")
    d.to_csv(RAW/"china_financas_mof_2014_2025.csv",index=False,encoding="utf-8-sig")
    return d


def build_panel():
    pop,pop_status=collect_sidra_population()
    ipca=collect_ipca()
    wdi,wdi_raw=collect_wdi()
    china_raw=make_china_source()
    china=china_raw[china_raw.ano.isin(YEARS)].copy()
    # taxa de mercado WDI, taxas reais ao câmbio anual médio de 2025
    fx_bra_url="https://api.worldbank.org/v2/country/BRA/indicator/PA.NUS.FCRF?date=2025&format=json"
    resp=requests.get(fx_bra_url,timeout=60);resp.raise_for_status();p=resp.json()
    fx_bra_2025=float(p[1][0]["value"])
    fx_china_2025=wdi["PA.NUS.FCRF"][2025]
    rows=[]
    for city,name in CITIES.items():
      for year in YEARS:
        rev=json.loads((DCA/f"{city}_{year}_DCA-Anexo_I-C.json").read_text(encoding="utf-8"))["items"]
        exp=json.loads((DCA/f"{city}_{year}_DCA-Anexo_I-E.json").read_text(encoding="utf-8"))["items"]
        tax=account_value(rev,prefix="RO1.1.0.0.00")
        total=account_value(rev,exact_code="ReceitasExcetoIntraOrcamentarias")
        if not np.isfinite(total):
            cur=account_value(rev,prefix="RO1.0.0.0.00"); cap=account_value(rev,prefix="RO2.0.0.0.00")
            total=cur+cap if np.isfinite(cur) and np.isfinite(cap) else np.nan
        trc=account_value(rev,prefix="RO1.7.0.0.00"); trk=account_value(rev,prefix="RO2.4.0.0.00")
        tr=trc+trk if np.isfinite(trc) and np.isfinite(trk) else np.nan
        expenditure=next((float(x["valor"]) for x in exp if x.get("coluna")=="Despesas Empenhadas" and x.get("conta") in {"Despesas Exceto Intraorçamentárias","Despesas (Exceto Intraorçamentárias)"}),np.nan)
        health=next((float(x["valor"]) for x in exp if x.get("coluna")=="Despesas Empenhadas" and x.get("conta")=="10 - Saúde"),np.nan)
        education=next((float(x["valor"]) for x in exp if x.get("coluna")=="Despesas Empenhadas" and x.get("conta")=="12 - Educação"),np.nan)
        popval=pop[(city,year)]; factor=ipca[2025]/ipca[year]
        meta_rev=json.loads((DCA/f"{city}_{year}_DCA-Anexo_I-C.json").read_text(encoding="utf-8"))["_metadata"]
        meta_exp=json.loads((DCA/f"{city}_{year}_DCA-Anexo_I-E.json").read_text(encoding="utf-8"))["_metadata"]
        r={"pais":"Brasil","unidade":name,"codigo_ibge":city,"ano":year,"populacao":popval,"status_populacao":pop_status[(city,year)],
           "receita_total_nominal_brl":total,"receita_tributaria_nominal_brl":tax,"transferencias_correntes_nominal_brl":trc,"transferencias_capital_nominal_brl":trk,"transferencias_correntes_mais_capital_nominal_brl":tr,
           "despesa_empenhada_nominal_brl":expenditure,"despesa_saude_empenhada_nominal_brl":health,"despesa_educacao_empenhada_nominal_brl":education,
           "deflator_ipca_base_2025":factor,"ipca_indice_medio_anual_encadeado":ipca[year],"url_dca_receita":meta_rev["source_url"],"url_dca_despesa":meta_exp["source_url"],
           "cambio_brl_por_usd_anual_2025":fx_bra_2025}
        for f in ["receita_total","receita_tributaria","transferencias_correntes_mais_capital","despesa_empenhada","despesa_saude_empenhada","despesa_educacao_empenhada"]:
          nom=r[f+"_nominal_brl"]; r[f+"_real_2025_brl"]=nom*factor if np.isfinite(nom) else np.nan
          r[f+"_real_2025_brl_pc"]=r[f+"_real_2025_brl"]/popval if np.isfinite(r[f+"_real_2025_brl"]) else np.nan
        r["transferencias_pct_receita_total"]=100*tr/total if np.isfinite(tr) and np.isfinite(total) and total else np.nan
        r["tributos_pct_receita_total"]=100*tax/total if np.isfinite(tax) and np.isfinite(total) and total else np.nan
        r["transferencias_pct_despesa"]=100*tr/expenditure if np.isfinite(tr) and np.isfinite(expenditure) and expenditure else np.nan
        r["transferencias_real_2025_usd_mercado"]=r["transferencias_correntes_mais_capital_real_2025_brl"]/fx_bra_2025
        r["transferencias_real_2025_usd_mercado_pc"]=r["transferencias_real_2025_usd_mercado"]/popval
        r["receita_tributaria_real_2025_usd_mercado"]=r["receita_tributaria_real_2025_brl"]/fx_bra_2025
        r["despesa_real_2025_usd_mercado"]=r["despesa_empenhada_real_2025_brl"]/fx_bra_2025
        rows.append(r)
    br=pd.DataFrame(rows)
    cn_rows=[]
    cpi=wdi["FP.CPI.TOTL"]; years_gdp=wdi["NY.GDP.MKTP.CD"]; gdp_pc_constant=wdi["NY.GDP.PCAP.KD"]; pops=wdi["SP.POP.TOTL"]; fxs=wdi["PA.NUS.FCRF"]
    for _,m in china.iterrows():
        y=int(m.ano); f=cpi[2025]/cpi[y]; popval=pops[y]
        own=float(m.receita_local_propria_100m_cny)*1e8; tr=float(m.transferencias_centro_para_local_100m_cny)*1e8
        local=float(m.receita_orcamento_geral_local_100m_cny)*1e8; expense=float(m.despesa_orcamento_geral_local_100m_cny)*1e8
        gdp_usd=years_gdp.get(y,np.nan); fx=fxs.get(y,np.nan); gdp_cny=gdp_usd*fx if np.isfinite(gdp_usd) and np.isfinite(fx) else np.nan
        d={"pais":"China","unidade":"Agregado de governos locais","ano":y,"populacao":popval,"status_populacao":"World Bank WDI, população anual nacional",
           "receita_local_propria_nominal_cny":own,"transferencias_centro_para_local_nominal_cny":tr,"receita_orcamento_geral_local_nominal_cny":local,"despesa_orcamento_geral_local_nominal_cny":expense,
           "transferencia_central_final_reportada_100m_cny":float(m.transferencia_central_final_100m_cny) if pd.notna(m.transferencia_central_final_100m_cny) else np.nan,
           "pib_nacional_nominal_cny":gdp_cny,"pib_nacional_nominal_usd":gdp_usd,"pib_nacional_per_capita_constante_2015_usd":gdp_pc_constant.get(y,np.nan),"pib_nacional_total_constante_2015_usd":gdp_pc_constant.get(y,np.nan)*popval,"cambio_cny_por_usd_anual":fx,"cpi_indice_anual_wdi_2010_100":cpi[y],"deflator_cpi_base_2025":f,
           "url_fonte_financas":m.source_url,"url_revisao_final_transferencias":m.url_revisao_final_transferencias if pd.notna(m.url_revisao_final_transferencias) else "",
           "observacao_contabil":m.observacao}
        for f0 in ["receita_local_propria","transferencias_centro_para_local","receita_orcamento_geral_local","despesa_orcamento_geral_local"]:
          nominal=d[f0+"_nominal_cny"]; real=nominal*f
          d[f0+"_real_2025_cny"]=real; d[f0+"_real_2025_cny_pc"]=real/popval
          d[f0+"_real_2025_usd_mercado"]=real/fx_china_2025; d[f0+"_real_2025_usd_mercado_pc"]=real/fx_china_2025/popval
        d["pib_nacional_corrente_cpi_deflacionado_2025_cny"]=gdp_cny*f if np.isfinite(gdp_cny) else np.nan
        d["transferencias_pct_receita_local"]=100*tr/local if local else np.nan
        d["receita_propria_pct_receita_local"]=100*own/local if local else np.nan
        d["transferencias_pct_despesa_local"]=100*tr/expense if expense else np.nan
        d["transferencias_pct_pib_nacional"]=100*tr/gdp_cny if np.isfinite(gdp_cny) and gdp_cny else np.nan
        d["transferencias_real_2025_usd_mercado"]=d["transferencias_centro_para_local_real_2025_usd_mercado"]
        d["transferencias_real_2025_usd_mercado_pc"]=d["transferencias_centro_para_local_real_2025_usd_mercado_pc"]
        cn_rows.append(d)
    cn=pd.DataFrame(cn_rows)
    panel=pd.concat([br,cn],ignore_index=True,sort=False).sort_values(["pais","unidade","ano"])
    if len(br)!=20 or len(cn)!=10: raise ValueError(f"Cobertura inesperada: Brasil={len(br)}, China={len(cn)}")
    key_b=["receita_total_nominal_brl","receita_tributaria_nominal_brl","transferencias_correntes_mais_capital_nominal_brl","despesa_empenhada_nominal_brl","populacao"]
    if br[key_b].isna().any().any(): raise ValueError("Campos fiscais ou populacionais essenciais ausentes no Brasil")
    key_c=["receita_local_propria_nominal_cny","transferencias_centro_para_local_nominal_cny","receita_orcamento_geral_local_nominal_cny","despesa_orcamento_geral_local_nominal_cny","populacao"]
    if cn[key_c].isna().any().any(): raise ValueError("Campos fiscais ou populacionais essenciais ausentes na China")
    return br,cn,panel,china_raw,ipca,wdi,fx_bra_2025,fx_china_2025


def summary(br,cn):
    rows=[]
    for _,d in br.groupby("unidade"):
      d=d.sort_values("ano"); a=d.iloc[0]; b=d.iloc[-1]
      for label,col,unit in [("Transferências reais per capita","transferencias_real_2025_usd_mercado_pc","USD 2025 mercado/pessoa"),("Transferências / receita total","transferencias_pct_receita_total","%"),("Tributos / receita total","tributos_pct_receita_total","%"),("Despesa empenhada real per capita","despesa_empenhada_real_2025_brl_pc","BRL 2025/pessoa")]:
        x,y=float(a[col]),float(b[col]); rows.append({"pais":"Brasil","unidade":a.unidade,"indicador":label,"2016":x,"2025":y,"variacao_real_%":(y/x-1)*100 if x else np.nan,"unidade_medida":unit})
    d=cn.sort_values("ano");a,b=d.iloc[0],d.iloc[-1]
    for label,col,unit in [("Transferências centrais reais per capita","transferencias_real_2025_usd_mercado_pc","USD 2025 mercado/pessoa"),("Transferências / receita local","transferencias_pct_receita_local","%"),("Receita própria / receita local","receita_propria_pct_receita_local","%"),("Transferências / despesa local","transferencias_pct_despesa_local","%"),("Transferências / PIB nacional","transferencias_pct_pib_nacional","%")]:
      x,y=float(a[col]),float(b[col]);rows.append({"pais":"China","unidade":"Agregado de governos locais","indicador":label,"2016":x,"2025":y,"variacao_real_%":(y/x-1)*100 if x and label=="Transferências centrais reais per capita" else (y-x if x else np.nan),"unidade_medida":unit})
    return pd.DataFrame(rows)


def apply_simple_styles(path):
    wb=load_workbook(path)
    for ws in wb.worksheets:
      ws.freeze_panes="A2"; ws.auto_filter.ref=ws.dimensions
      ws.row_dimensions[1].height=36
      for c in ws[1]: c.font=Font(name="Aptos",bold=True,color="FFFFFF");c.fill=PatternFill("solid",fgColor="16324F");c.alignment=Alignment(wrap_text=True,vertical="center")
      for col in ws.columns:
        letter=get_column_letter(col[0].column); vals=[len(str(c.value)) for c in col[:100] if c.value is not None]
        ws.column_dimensions[letter].width=min(max(12,max(vals,default=12)+2),42)
      for row in ws.iter_rows(min_row=2):
        for c in row:
          if isinstance(c.value,(int,float)) and c.value is not None: c.number_format='#,##0.00;[Red]-#,##0.00;–'
          if c.column==1:c.alignment=Alignment(vertical="top")
    wb.save(path)


def main():
    br,cn,panel,china_raw,ipca,wdi,fxbr,fxcn=build_panel()
    sm=summary(br,cn)
    br.to_csv(TREATED/"painel_brasil_2016_2025.csv",index=False,encoding="utf-8-sig",float_format="%.6f")
    cn.to_csv(TREATED/"painel_china_2016_2025.csv",index=False,encoding="utf-8-sig",float_format="%.6f")
    panel.to_csv(TREATED/"painel_fiscal_comparado_2016_2025.csv",index=False,encoding="utf-8-sig",float_format="%.6f")
    sm.to_csv(OUT/"resumo_fiscal_2016_2025.csv",index=False,encoding="utf-8-sig",float_format="%.4f")
    # Workbook final: preserva integralmente as abas 2014–2023 e agrega extensão de dez anos.
    book=ROOT/"dados"/"base_atualizada_232037730.xlsx"
    if not book.exists(): raise FileNotFoundError(book)
    wb=load_workbook(book)
    for name in ["Fiscal_10A_Painel","Fiscal_10A_Resumo","China_MOF_2014_2025"]:
      if name in wb.sheetnames: del wb[name]
    for name,df in [("Fiscal_10A_Painel",panel),("Fiscal_10A_Resumo",sm),("China_MOF_2014_2025",china_raw)]:
      ws=wb.create_sheet(name)
      ws.append(list(df.columns))
      for r in df.itertuples(index=False,name=None): ws.append([None if pd.isna(v) else (float(v) if isinstance(v,(np.floating,)) else int(v) if isinstance(v,(np.integer,)) else v) for v in r])
    # Comentários de proveniência na primeira linha de variáveis monetárias/fontes 2025.
    ws=wb["Fiscal_10A_Painel"]
    for row in range(2,ws.max_row+1):
      p=ws.cell(row,1).value; year=ws.cell(row,4).value if p=="Brasil" else ws.cell(row,3).value
      for cell in ws[row]:
        if cell.value is None: continue
        if cell.column==1: continue
        source="Siconfi DCA I-C/I-E; contas anuais executadas" if p=="Brasil" else "Ministry of Finance PRC; execução do orçamento público geral local"
        cell.comment=Comment(f"Fonte: {source}; exercício {year}. URLs de origem e definição/unidade na mesma linha da planilha e no dicionário/nota do repositório. Coleta: {TODAY}.","Manus")
    apply_simple_styles(book); wb.save(book)
    print(f"10-year extension: Brazil {len(br)} city-years; China {len(cn)} national-years; combined {len(panel)} records")
    print(f"IPCA 2025 base: {ipca[2025]:.6f}; WDI FX 2025 BRL/USD={fxbr:.6f}, CNY/USD={fxcn:.6f}")
    print("Workbook updated without replacing the 2014–2023 source-aligned panel.")
    print(sm.to_string(index=False))

if __name__=="__main__": main()
