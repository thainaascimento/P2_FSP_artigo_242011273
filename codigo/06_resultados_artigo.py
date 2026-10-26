#!/usr/bin/env python3
"""Estatísticas descritivas e figuras do artigo; sem inferência causal.
Todas as linhas são lidas dos painéis tratados gerados em 03_extensao_fiscal_2016_2025.py.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "dados" / "tratados"
OUT = ROOT / "resultados"
ART = ROOT / "artigo"
OUT.mkdir(exist_ok=True)
(ART / "figuras").mkdir(exist_ok=True)
B = pd.read_csv(DATA / "painel_brasil_2016_2025.csv")
C = pd.read_csv(DATA / "painel_china_2016_2025.csv")
BH = pd.read_csv(DATA / "painel_municipal_2014_2023.csv")
CH = pd.read_csv(DATA / "painel_china_2014_2023.csv")

# USD is a market-exchange-rate conversion, not PPP. Constant 2025 annual-average FX.
BRL_PER_USD_2025 = 5.587286
CNY_PER_USD_2025 = 7.189847

B["despesa_pc_usd_2025"] = B["despesa_empenhada_real_2025_brl_pc"] / BRL_PER_USD_2025
C["despesa_pc_usd_2025"] = C["despesa_orcamento_geral_local_real_2025_cny_pc"] / CNY_PER_USD_2025
B["transfer_pc_usd_2025"] = B["transferencias_real_2025_usd_mercado_pc"]
C["transfer_pc_usd_2025"] = C["transferencias_centro_para_local_real_2025_usd_mercado_pc"]

rows = []
series = []
for _, g in B.groupby("unidade"):
    g = g.sort_values("ano")
    unit = g["unidade"].iloc[0]
    series.append((unit, g, "Brazil"))
for unit, g, country in [("China — agregado local", C.sort_values("ano"), "China")]:
    series.append((unit, g, country))

specs = {
    "transferências reais per capita (USD de mercado, base 2025)": "transfer_pc_usd_2025",
    "transferências/receita local (%)": "transferencias_pct_receita_total",
    "tributos/receita total (%) — Brasil; definição não equivalente na China": "tributos_pct_receita_total",
    "despesa real per capita (USD de mercado, base 2025)": "despesa_pc_usd_2025",
}
for label, col in specs.items():
    for unit, g, country in series:
        if col not in g.columns:
            if country == "China" and col == "transferencias_pct_receita_total":
                col_actual = "transferencias_pct_receita_local"
            elif country == "China" and col == "tributos_pct_receita_total":
                col_actual = "receita_propria_pct_receita_local"
            else:
                continue
        else:
            col_actual = col
        d = g.dropna(subset=[col_actual]).sort_values("ano")
        if d.empty: continue
        a, z = d.iloc[0], d.iloc[-1]
        start, end = float(a[col_actual]), float(z[col_actual])
        rows.append({"unidade": unit, "variavel": label, "ano_inicial": int(a["ano"]), "valor_inicial": start,
                     "ano_final": int(z["ano"]), "valor_final": end,
                     "variacao_relativa_pct": (end/start-1)*100 if start else np.nan,
                     "variacao_pp": end-start if "(%)" in label else np.nan,
                     "n_observacoes": len(d)})
summary = pd.DataFrame(rows)
summary.to_csv(OUT / "resultados_descritivos_artigo_2016_2025.csv", index=False, encoding="utf-8-sig")
summary.to_csv(ART / "resultados_descritivos_2016_2025.csv", index=False, encoding="utf-8-sig")

assoc = []
for unit, g, country in series:
    g = g.sort_values("ano").copy()
    # Keep same units/base-year within each series; conversions are constant FX.
    pairs = [("níveis anuais", "transfer_pc_usd_2025", "despesa_pc_usd_2025")]
    if country == "Brazil":
        own = "receita_tributaria_real_2025_brl_pc"
        if own in g: g["own_pc_real"] = g[own]
    else:
        own = "receita_local_propria_real_2025_cny_pc"
        if own in g: g["own_pc_real"] = g[own]
    if "own_pc_real" in g:
        pairs.append(("níveis anuais", "transfer_pc_usd_2025", "own_pc_real"))
    for label, x, y in pairs:
        z = g[[x, y]].dropna()
        r = z[x].corr(z[y]) if len(z) >= 3 else np.nan
        assoc.append({"unidade":unit,"associacao":label,"variavel_x":x,"variavel_y":y,"pearson_r_descritivo":r,"n":len(z),
                      "aviso":"Exploratória; séries anuais curtas e tendências comuns; não é teste causal nem significância inferencial."})
    # First differences reduce common deterministic trends but do not establish exogeneity.
    for x,y in [("transfer_pc_usd_2025","despesa_pc_usd_2025")]:
        z = g[["ano",x,y]].dropna().sort_values("ano").copy()
        z[x+"_d"] = z[x].diff(); z[y+"_d"] = z[y].diff(); z = z.dropna()
        assoc.append({"unidade":unit,"associacao":"primeiras diferenças anuais", "variavel_x":x+"_d", "variavel_y":y+"_d",
                      "pearson_r_descritivo":z[x+"_d"].corr(z[y+"_d"]) if len(z)>=3 else np.nan,"n":len(z),
                      "aviso":"Exploratória, n pequeno; diferenças não eliminam endogeneidade nem identificam causalidade."})
pd.DataFrame(assoc).to_csv(OUT / "associacoes_exploratorias_artigo.csv", index=False, encoding="utf-8-sig")
pd.DataFrame(assoc).to_csv(ART / "associacoes_exploratorias.csv", index=False, encoding="utf-8-sig")

# Main four-panel fiscal figure.
plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":9, "axes.titlesize":10, "axes.labelsize":8})
fig, axes = plt.subplots(2, 2, figsize=(11.4, 7.4), constrained_layout=False)
colors = {"Cascavel/PR":"#176B55", "Londrina/PR":"#3976A8", "China — agregado local":"#B35C34"}
for unit,g,country in series:
    color=colors[unit]
    axes[0,0].plot(g.ano,g.transfer_pc_usd_2025,marker='o',lw=1.8,label=unit,color=color)
    axes[0,1].plot(g.ano,g.despesa_pc_usd_2025,marker='o',lw=1.8,label=unit,color=color)
    share = "transferencias_pct_receita_total" if country=="Brazil" else "transferencias_pct_receita_local"
    own = "tributos_pct_receita_total" if country=="Brazil" else "receita_propria_pct_receita_local"
    axes[1,0].plot(g.ano,g[share],marker='o',lw=1.8,label=unit,color=color)
    axes[1,1].plot(g.ano,g[own],marker='o',lw=1.8,label=unit,color=color)
axes[0,0].set_title("Transferências reais por habitante")
axes[0,0].set_ylabel("USD de mercado, preços de 2025")
axes[0,1].set_title("Despesa orçamentária real por habitante")
axes[0,1].set_ylabel("USD de mercado, preços de 2025")
axes[1,0].set_title("Transferências como proporção da receita reportada")
axes[1,0].set_ylabel("%")
axes[1,1].set_title("Receita própria como proporção da receita local")
axes[1,1].set_ylabel("%")
for ax in axes.flat:
    ax.grid(axis='y',alpha=.25); ax.set_xlabel("Ano fiscal"); ax.legend(frameon=False,fontsize=7)
fig.suptitle("Cascavel, Londrina e agregado de governos locais da China — 2016–2025",fontsize=12)
fig.subplots_adjust(left=.08,right=.985,bottom=.18,top=.89,hspace=.38,wspace=.22)
fig.text(.01,.025,"Nota: conversão cambial a taxas médias de mercado de 2025; não é PPC. No Brasil, transferências DCA correntes+capital e tributos próprios; na China, transferências centrais e receita própria do orçamento público geral. As categorias não são institucionalmente idênticas.",fontsize=6.5,wrap=True,va='bottom')
fig.savefig(ART/"figuras"/"figura_04_paineis_fiscais_2016_2025.png",dpi=220,bbox_inches="tight")
plt.close(fig)

# Activity data: only matched years in official municipal GDP (IBGE) and national WDI GDP.
BH["pib_pc_real_2023"] = BH["pib_municipal_real_2023_brl"] / BH["populacao"]
CH["pib_pc_constante_2015_usd"] = CH["pib_nacional_per_capita_constante_2015_usd"]
fig,ax=plt.subplots(figsize=(8.6,4.6),constrained_layout=False)
for unit,g in BH[ BH["ano"].between(2016,2023)].groupby("unidade"):
    g=g.sort_values("ano"); base=float(g.iloc[0].pib_pc_real_2023)
    ax.plot(g.ano,g.pib_pc_real_2023/base*100,marker='o',lw=1.8,label=f"{unit} — PIB municipal")
g=CH[CH["ano"].between(2016,2023)].sort_values("ano");base=float(g.iloc[0].pib_pc_constante_2015_usd)
ax.plot(g.ano,g.pib_pc_constante_2015_usd/base*100,marker='o',lw=1.8,linestyle='--',label="China — PIB nacional")
ax.set_title("Atividade econômica real per capita (índice 2016 = 100)")
ax.set_xlabel("Ano");ax.set_ylabel("Índice (base própria 2016 = 100)");ax.grid(alpha=.25);ax.legend(frameon=False,fontsize=8)
fig.subplots_adjust(left=.10,right=.985,bottom=.20,top=.88)
fig.text(.01,.025,"Nota: municípios = PIB IBGE deflacionado pelo IPCA a preços de 2023; China = PIB per capita WDI a preços constantes de 2015 (NY.GDP.PCAP.KD). PIB municipal disponível até 2023. Índices de bases monetárias próprias; não comparar níveis nem unidades administrativas.",fontsize=6.5,wrap=True,va='bottom')
fig.savefig(ART/"figuras"/"figura_05_pib_pc_indice_2016_2023.png",dpi=220,bbox_inches="tight")
plt.close(fig)

# Exploratory correlations of transfers with real local GDP per capita, matched to 2016–2023 only.
gdp_corr=[]
for unit,g in BH[BH.ano.between(2016,2023)].groupby("unidade"):
    z=g.merge(B[B.unidade.eq(unit)][["ano","transfer_pc_usd_2025"]],on="ano",how="inner").dropna(subset=["transfer_pc_usd_2025","pib_pc_real_2023"])
    gdp_corr.append({"unidade":unit,"periodo":"2016–2023","associacao":"níveis anuais", "r_pearson_descritivo":z.transfer_pc_usd_2025.corr(z.pib_pc_real_2023),"n":len(z),"aviso":"N pequeno; GDP municipal só até 2023; descritivo, sem identificação causal."})
CH_B=CH[CH.ano.between(2016,2023)].merge(C[C.ano.between(2016,2023)][["ano","transfer_pc_usd_2025"]],on="ano",how="inner").dropna(subset=["transfer_pc_usd_2025","pib_pc_constante_2015_usd"])
gdp_corr.append({"unidade":"China — agregado local e PIB nacional","periodo":"2016–2023","associacao":"níveis anuais","r_pearson_descritivo":CH_B.transfer_pc_usd_2025.corr(CH_B.pib_pc_constante_2015_usd),"n":len(CH_B),"aviso":"N pequeno; mistura agregado local com PIB nacional; WDI em USD constantes de 2015; descritivo, sem identificação causal."})
pd.DataFrame(gdp_corr).to_csv(OUT/"associacoes_pib_artigo.csv",index=False,encoding="utf-8-sig")
pd.DataFrame(gdp_corr).to_csv(ART/"associacoes_pib.csv",index=False,encoding="utf-8-sig")

qa={"access_date":"2026-10-22","fiscal_years":[2016,2025],"brazil_rows":int(len(B)),"china_rows":int(len(C)),"brazil_municipal_gdp_through":int(BH.ano.max()),"china_national_gdp_through":int(CH.ano.max()),"fx_brl_per_usd_2025":BRL_PER_USD_2025,"fx_cny_per_usd_2025":CNY_PER_USD_2025,"causal_claims":False,"outputs":["resultados_descritivos_artigo_2016_2025.csv","associacoes_exploratorias_artigo.csv","associacoes_pib_artigo.csv","artigo/figuras/figura_04_paineis_fiscais_2016_2025.png","artigo/figuras/figura_05_pib_pc_indice_2016_2023.png"]}
(OUT/"qa_resultados_artigo.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK",len(summary),"endpoint rows;",len(assoc),"exploratory correlations; GDP observations matched 2016-2023",[x["n"] for x in gdp_corr])
