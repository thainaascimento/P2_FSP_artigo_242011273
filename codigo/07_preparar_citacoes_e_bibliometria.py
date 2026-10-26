#!/usr/bin/env python3
"""Gera a lista de referências citáveis e o painel bibliométrico para o artigo.
Fonte bibliográfica: artigos_verificados_doi.csv; as contagens bibliométricas são geradas em R/bibliometrix.
"""
from pathlib import Path
import csv, json, collections
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artigo'
LIT=ART/'literatura'
BIO=LIT/'bibliometria'
FIG=ART/'figuras'; FIG.mkdir(parents=True,exist_ok=True)
with open(LIT/'artigos_verificados_doi.csv',encoding='utf-8-sig',newline='') as f:
    papers=list(csv.DictReader(f))
if len(papers)<80 or len({p['doi'].lower() for p in papers}) != len(papers):
    raise SystemExit('Falha: corpus inferior a 80 ou DOI duplicado.')

# Reference list with literal-safe Typst strings and DOI hyperlinks.
def tq(s): return json.dumps(str(s),ensure_ascii=False)
lines=[]
supplemental_start=len(papers)+1
for p in papers:
    i=int(p['reference_id'])
    authors=p['authors'].replace(';', ', ')
    lines.append(f'#text({tq(f"[{i}] {authors} ({p['year']}). {p['title']}. {p['journal']}. ")}) #link({tq('https://doi.org/'+p['doi'])})[DOI: {p['doi']}]')
    lines.append('#parbreak()')
# Methodological and official sources follow the verified topical corpus.
lines += [
 f'#text("[{supplemental_start}] Baker, A. C., Larcker, D. F., & Wang, C. C. Y. (2022). How much should we trust staggered difference-in-differences estimates? Journal of Financial Economics, 144(2), 370–395. ") #link("https://doi.org/10.1016/j.jfineco.2022.01.004")[DOI: 10.1016/j.jfineco.2022.01.004]',
 '#parbreak()',
 f'#text("[{supplemental_start+1}] Ferreira, L. O. G. (2021). Constitutional tax transfer in Brazilian municipalities: the fiscal illusion and the flypaper effect. Tese de doutorado, Universidade de Brasília. ") #link("https://repositorio.unb.br/bitstream/10482/42292/1/2021_LucasOliveiraGomesFerreira.pdf")[PDF da tese]',
 '#parbreak()',
 f'#text("[{supplemental_start+2}] Secretaria do Tesouro Nacional. Siconfi — API de dados abertos, Declaração de Contas Anuais (DCA), anexos I-C e I-E. Acesso em 22 out. 2026. ") #link("https://apidatalake.tesouro.gov.br/docs/siconfi/")[Documentação da API] #text("; ") #link("https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/dca")[Endpoint DCA]',
 '#parbreak()',
 f'#text("[{supplemental_start+3}] IBGE. SIDRA, tabela 6579, estimativas da população residente; relação populacional publicada ao TCU em 2023, baseada no Censo 2022; tabela 5938, Produto Interno Bruto dos Municípios. Acesso em 22 out. 2026. ") #link("https://sidra.ibge.gov.br/tabela/6579")[Estimativas] #text("; ") #link("https://www.ibge.gov.br/estatisticas/sociais/populacao/37734-relacao-da-populacao-dos-municipios-para-publicacao-no-tcu.html")[IBGE ao TCU 2023] #text("; ") #link("https://sidra.ibge.gov.br/tabela/5938")[PIB municipal]',
 '#parbreak()',
 f'#text("[{supplemental_start+4}] Banco Central do Brasil. Sistema Gerenciador de Séries Temporais, IPCA, série 433. Acesso em 22 out. 2026. ") #link("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json")[API SGS 433]',
 '#parbreak()',
 f'#text("[{supplemental_start+5}] Ministry of Finance of the People’s Republic of China. Relatórios de execução do orçamento central e local, 2014–2025; endereços por ano e observação em dados/fontes_brutas/china_financas_mof_2014_2025.csv. Acesso em 22 out. 2026. ") #link("https://www.mof.gov.cn/zhengwuxinxi/caizhengxinwen/202603/t20260316_3985331.htm")[Relatório 2025]',
 '#parbreak()',
 f'#text("[{supplemental_start+6}] Ministry of Finance of the People’s Republic of China. Contas finais centrais de 2022, publicada em 4 jul. 2023. ") #link("https://www.mof.gov.cn/zhengwuxinxi/caizhengxinwen/202307/t20230704_3894361.htm")[Prestação final 2022]',
 '#parbreak()',
 f'#text("[{supplemental_start+7}] World Bank. World Development Indicators: PIB corrente, PIB per capita constante de 2015 (NY.GDP.PCAP.KD), população, CPI e câmbio médio da China, consulta 2014–2025. Acesso em 22 out. 2026. ") #link("https://api.worldbank.org/v2/country/CHN/indicator/NY.GDP.PCAP.KD?date=2014:2025&format=json")[API de PIB per capita constante] #text("; ") #link("https://api.worldbank.org/v2/country/CHN/indicator/NY.GDP.MKTP.CD?date=2014:2025&format=json")[API de PIB nominal]',
 '#parbreak()',
 f'#text("[{supplemental_start+8}] National Bureau of Statistics of China. Statistical Communiqué of the People’s Republic of China on the 2025 National Economic and Social Development. Publicado em 2026. ") #link("https://www.stats.gov.cn/english/PressRelease/202602/t20260228_1962661.html")[Comunicado estatístico 2025]',
 '#parbreak()',
 f'#text("[{supplemental_start+9}] Repositório de partida indicado pelo aluno. P1-Prova-Financas, matrícula 232037730. ") #link("https://github.com/vz8pypzpxs-creator/P1-Prova-Financas---P1-Gabriel-Rodrigues-232037730")[Repositório anterior]',
 '#parbreak()',
 f'#text("[{supplemental_start+10}] Aria, M., & Cuccurullo, C. (2017). bibliometrix: An R-tool for comprehensive science mapping analysis. Journal of Informetrics, 11(4), 959–975. ") #link("https://doi.org/10.1016/j.joi.2017.08.007")[DOI: 10.1016/j.joi.2017.08.007]'
]
ref_blocks=[f'#block(breakable: true, below: 1.2pt)[{line}]' for line in lines if line != '#parbreak()']
(ART/'referencias.typ').write_text('\n'.join(ref_blocks)+'\n',encoding='utf-8')

labels={
 'flypaper_classic':'Teoria clássica e mecanismos do efeito flypaper',
 'flypaper_reviews':'Revisões, heterogeneidade e identificação do efeito',
 'fiscal_illusion':'Ilusão fiscal, grants e percepção do eleitor',
 'fiscal_federalism':'Federalismo fiscal e instituições intergovernamentais',
 'brazil_flypaper':'Evidência brasileira sobre efeito flypaper',
 'brazil_tax_effort':'Receita própria, autonomia e esforço fiscal no Brasil',
 'china_transfers':'Transferências fiscais entre níveis na China',
 'china_local_finance':'Finanças locais, orçamento e financiamento na China',
 'china_institutions':'Instituições e incentivos fiscais locais chineses',
 'local_tax_effort':'Tributação local e esforço arrecadatório',
 'transfers_growth':'Transferências e atividade econômica/crescimento',
 'comparative_grants':'Resposta fiscal a grants em outras federações',
 'comparative_flypaper':'Comparações internacionais, desenho de grants e identificação'
}
groups=collections.defaultdict(list)
for p in papers: groups[p['origin_file']].append(int(p['reference_id']))
rows=[]
for source,ids in sorted(groups.items()):
    rows.append({'source_id':source,'eixo':labels.get(source,source),'n':len(ids),'reference_ids':';'.join(map(str,sorted(ids)))})
pd.DataFrame(rows).to_csv(LIT/'grupos_citacao_por_eixo.csv',index=False,encoding='utf-8-sig')

# One-page bibliometric dashboard (all frequencies from the R/bibliometrix outputs).
def load(name): return pd.read_csv(BIO/name,encoding='utf-8-sig')
annual=load('producao_por_ano.csv')
journals=load('periodicos_mais_relevantes.csv').head(7).sort_values('count')
authors=load('autores_mais_relevantes.csv').head(7).sort_values('count')
countries=load('paises_contexto_estudo.csv')
review_file=LIT/'dois_para_revisao_manual.csv'
review_count=len(pd.read_csv(review_file,encoding='utf-8-sig')) if review_file.exists() else 0
unspecified=countries.loc[countries.item=='Não especificado','count']
unspecified_count=int(unspecified.iloc[0]) if len(unspecified) else 0
countries=countries[countries.item!='Não especificado'].head(7).sort_values('count')
network_matrix=pd.read_csv(BIO/'matriz_coocorrencia_palavras_chave.csv',index_col=0,encoding='utf-8-sig')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.titlesize':9,'axes.labelsize':7})
fig=plt.figure(figsize=(12,8.3),constrained_layout=False)
gs=GridSpec(3,2,figure=fig,height_ratios=[0.83,1.1,1.1],left=.12,right=.985,top=.91,bottom=.17,hspace=.52,wspace=.34)
ax0=fig.add_subplot(gs[0,:])
all_years=np.arange(int(annual.year.min()),int(annual.year.max())+1)
counts=annual.set_index('year').articles.reindex(all_years,fill_value=0)
ax0.bar(all_years,counts,color='#3976A8',width=.85)
ax0.set_title(f'Produção anual do corpus (n={len(papers)})');ax0.set_ylabel('Artigos');ax0.set_xlim(all_years.min()-1,all_years.max()+1);ax0.grid(axis='y',alpha=.2)
ax0.set_xticks([1981,1990,2000,2010,2020,2026])
ax1=fig.add_subplot(gs[1,0]);ax1.barh(journals.item,journals['count'],color='#176B55');ax1.set_title('Periódicos mais recorrentes');ax1.set_xlabel('Artigos');ax1.grid(axis='x',alpha=.2);ax1.tick_params(axis='y',labelsize=7)
ax2=fig.add_subplot(gs[1,1]);ax2.barh(authors.item,authors['count'],color='#B35C34');ax2.set_title('Autores com maior frequência');ax2.set_xlabel('Artigos');ax2.grid(axis='x',alpha=.2);ax2.tick_params(axis='y',labelsize=7)
ax3=fig.add_subplot(gs[2,0]);ax3.barh(countries.item,countries['count'],color='#6750A4');ax3.set_title('Países mais mencionados');ax3.set_xlabel('Menções em artigos');ax3.grid(axis='x',alpha=.2);ax3.tick_params(axis='y',labelsize=7)
ax4=fig.add_subplot(gs[2,1]);ax4.set_title('Rede de coocorrência — matriz biblioNetwork')
nodes=list(network_matrix.index);n=len(nodes);angles=np.linspace(0,2*np.pi,n,endpoint=False);pos={node:(np.cos(a),np.sin(a)) for node,a in zip(nodes,angles)}
upper=[]
for i,u in enumerate(nodes):
    for j in range(i+1,n):
        v=nodes[j];w=float(network_matrix.loc[u,v])
        if w>0: upper.append((u,v,w))
cut=sorted([e[2] for e in upper],reverse=True)[min(24,max(0,len(upper)-1))] if upper else 1
for u,v,w in upper:
    if w<cut: continue
    x1,y1=pos[u];x2,y2=pos[v]
    ax4.plot([x1,x2],[y1,y2],color='#89939D',alpha=.22+.55*w/max(e[2] for e in upper),lw=.35+.75*w/max(e[2] for e in upper),zorder=1)
strength=network_matrix.sum(axis=0).astype(float)-np.diag(network_matrix.to_numpy(dtype=float))
for node in nodes:
    x,y=pos[node];s=float(strength[node]);ax4.scatter([x],[y],s=40+3*s,color='#3976A8',edgecolor='white',linewidth=.5,zorder=2)
    label=node.replace('transferências intergovernamentais','transferências\nintergovernamentais').replace('federalismo e descentralização fiscal','federalismo e\ndescentralização').replace('atividade econômica e desenvolvimento','atividade econômica\ne desenvolvimento').replace('receita própria e esforço fiscal','receita própria e\nesforço fiscal').replace('identificação e métodos causais','identificação e\nmétodos causais')
    ax4.text(x*1.18,y*1.18,label,ha='center',va='center',fontsize=6.2,color='#1F2933',zorder=3)
ax4.set_xlim(-1.55,1.55);ax4.set_ylim(-1.45,1.45);ax4.axis('off')
fig.suptitle('Estudo bibliométrico — fluxo executado em bibliometrix 5.5.0',fontsize=12,y=.98)
fig.text(.015,.025,f'Nota: corpus temático = {len(papers)} artigos com DOI, título compatível e tipo journal-article no Crossref; {review_count} registros ficaram fora após revisão. Países são menções codificadas de título/resumo/achado, não afiliações; um artigo pode mencionar vários países e {unspecified_count} não tiveram país identificável. Termos harmonizados não são palavras-chave autorais. Frequências não medem qualidade ou impacto.',fontsize=6.5,wrap=True,va='bottom')
fig.savefig(FIG/'figura_06_painel_bibliometrico.png',dpi=220,bbox_inches='tight')
plt.close(fig)

# Compact source-level citation manifest for audit and discussion.
ids={int(p['reference_id']) for p in papers}
assert ids==set(range(1,len(papers)+1))
print(f'OK: {len(papers)} DOI únicos, {len(groups)} eixos, {len(rows)} grupos e painel bibliométrico.')
