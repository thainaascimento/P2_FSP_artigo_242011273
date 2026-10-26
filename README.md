# Transferências intergovernamentais, receitas próprias e atividade econômica

**Matrícula:** 232037730  
**Cobertura fiscal principal:** 2016–2025  
**Unidades:** Cascavel/PR, Londrina/PR e agregado dos governos locais da China  
**Data de coleta documentada:** 22 de outubro de 2026

> **Transparência acadêmica:** este material foi preparado com assistência de IA e deve ser tratado como rascunho de pesquisa. O estudante deve revisar dados, texto e conclusões e declarar o uso de IA de acordo com as normas da disciplina antes de eventual submissão. A matrícula não constitui declaração de autoria individual.

## Pergunta e escopo

O artigo descreve como transferências intergovernamentais se relacionam com receitas próprias, despesas e atividade econômica em Cascavel e Londrina, e como essas trajetórias diferem das do agregado local chinês. A janela fiscal principal contém os dez exercícios mais recentes completos no momento da coleta (2016–2025). O painel histórico 2014–2023 é preservado para comparação com a série de PIB municipal: o último PIB municipal disponível na coleta era 2023.

A análise é descritiva. Correlações e trajetórias não demonstram causalidade nem identificam o efeito flypaper. A série chinesa é um agregado nacional de governos locais, não um município; os escopos contábeis e institucionais não são equivalentes aos brasileiros. Conversões para USD usam câmbio de mercado médio de 2025, não paridade do poder de compra.

## Arquivos principais

- [Artigo em PDF](artigo/main.pdf), identificado pela matrícula.
- [Base Excel atualizada](dados/base_atualizada_232037730.xlsx).
- [Painel fiscal comparado 2016–2025](dados/tratados/painel_fiscal_comparado_2016_2025.csv).
- [Dicionário de variáveis](dados/tratados/dicionario_variaveis.csv).
- [Registro de alterações](CHANGELOG.md).
- [Fontes consultadas](relatorios/fontes_consultadas.md) e [nota de fontes, decisões e limitações](relatorios/nota_de_fontes_e_limitacoes.md).
- [Scripts de coleta, tratamento, análise e bibliometria](codigo/).

## Estrutura

```text
artigo/                 PDF, fonte Typst, referências, corpus e saídas bibliométricas
codigo/                 Scripts Python e R reproduzíveis
dados/originais/        Planilha e arquivos Finbra recebidos do trabalho anterior
dados/fontes_brutas/    Respostas originais das APIs, arquivos oficiais e metadados
dados/tratados/         Painéis CSV e dicionário de variáveis
dados/                  Planilha XLSX integrada
resultados/              Estatísticas, gráficos e relatórios de QA
relatorios/              Fontes, decisões de mensuração, limitações e hashes
```

## Fontes e tratamento

As receitas e despesas municipais vêm da DCA do Siconfi/Tesouro Nacional, anexos I-C e I-E. População e PIB municipal vêm do IBGE/SIDRA; o deflator brasileiro é o IPCA mensal do Banco Central (SGS 433). A série fiscal chinesa usa relatórios anuais do Ministry of Finance; população, CPI, câmbio e PIB per capita real chinês vêm do World Development Indicators do Banco Mundial. O comunicado estatístico do NBS de 2025 é usado como verificação externa de cobertura recente.

Valores nominais são convertidos para preços médios de 2025 pelo IPCA no Brasil e pelo CPI do WDI na China. Valores per capita são calculados com a população observada. Para Cascavel e Londrina, o valor do Censo Demográfico 2022 é usado em 2022 e como proxy estática explicitamente marcada para 2023; não há interpolação de crescimento. PIB municipal não é extrapolado para 2024–2025. Dados ausentes permanecem ausentes e não são tratados como zero.

As contas brasileiras de transferências somam rubricas DCA correntes e de capital de escopo amplo. A receita própria chinesa inclui componentes tributários e não tributários; o orçamento público geral chinês não cobre todos os fundos, receitas da terra ou fontes extraorçamentárias locais. As distinções estão descritas no artigo e no dicionário.

## Reprodução

Requer Python 3, R e Typst, além de acesso à internet para consultas a fontes que não estejam em cache e para a validação Crossref. Na raiz do repositório:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
export R_LIBS_USER="${R_LIBS_USER:-$HOME/R/library}"
mkdir -p "$R_LIBS_USER"
Rscript -e 'install.packages("bibliometrix", repos="https://cloud.r-project.org")'
bash reproduzir.sh
```

O script executa, em ordem, a coleta Siconfi, os painéis históricos e atualizados, a validação do corpus DOI, a análise com `bibliometrix`, as estatísticas e figuras e a compilação Typst do PDF. O corpus bibliográfico arquivado inclui candidatos, registros em revisão, DOIs e o snapshot datado da auditoria Crossref; `FINANCAS_USE_ARCHIVED_CORPUS=1` reutiliza essa auditoria e mantém estáveis as referências, sem depender de pastas de pesquisa fora do repositório. Para revalidar exportações bibliográficas novas, indique-as com `FINANCAS_RESEARCH_SOURCE_DIR` e execute o script sem o modo arquivado.

Para explorar interativamente o corpus com Biblioshiny, execute em uma sessão R:

```r
library(bibliometrix)
biblioshiny()
```

O `biblioshiny()` abre uma aplicação local interativa; ele não é necessário para a rotina automatizada. Os resultados reproduzíveis do artigo são calculados pelo script `codigo/05_bibliometria.R` com bibliometrix 5.5.0.

Se você tiver exportações brutas adicionais das pesquisas bibliográficas, indique seu diretório antes de rodar `codigo/04_preparar_corpus_bibliometrix.py`:

```bash
FINANCAS_RESEARCH_SOURCE_DIR=/caminho/para/exportacoes python3 codigo/04_preparar_corpus_bibliometrix.py
```

O arquivo `dados/base_atualizada_232037730.xlsx` agrega os dados tratados e mantém abas históricas. CSVs separados são fornecidos para inspeção, leitura por máquina e verificação independente.

## Contato e proveniência

O repositório anterior indicado pelo estudante é citado no artigo e seus materiais editáveis preservados em `dados/originais/`; os hashes constam em `relatorios/SHA256_anteriores.txt`. Consulte `CHANGELOG.md` para o resumo das atualizações. A metodologia, a revisão bibliográfica e os limites comparativos estão no PDF e nos relatórios de fonte.
