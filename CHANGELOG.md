# Registro de alterações

## 2026-10-22 — versão de pesquisa 1.0

- Preservada a planilha editável do trabalho anterior e os dois arquivos Finbra originais em `dados/originais/`; hashes registrados em `relatorios/SHA256_anteriores.txt`.
- Reconstruídas e arquivadas declarações DCA do Siconfi para Cascavel e Londrina entre 2014 e 2025, com URLs e metadados por arquivo. A janela fiscal principal foi atualizada para 2016–2025, os dez exercícios mais recentes completos na data de coleta.
- Mantido um painel histórico separado para 2014–2023, que permite associar finanças ao PIB municipal do IBGE sem extrapolar atividade econômica municipal para 2024–2025.
- Atualizadas as séries chinesas de orçamento público geral local do Ministry of Finance até 2025. Os recebimentos locais que fecham a identidade contábil foram mantidos separados da despesa central final com transferências: a distinção está documentada para 2022 e 2025, sem substituição silenciosa.
- Aplicados IPCA mensal encadeado, média anual e ano-base 2025 para fluxos brasileiros; para a China, CPI do WDI com ano-base 2025. Conversões para USD usam câmbio médio de mercado de 2025 e não são PPC.
- Explicitada a cobertura populacional: estimativas IBGE/SIDRA nos anos disponíveis, Censo 2022 em 2022 e valor do Censo como proxy estática para 2023, também reproduzido na relação do IBGE ao TCU de 2023. Não foi interpolado crescimento.
- Corrigido o indicador de atividade econômica chinês: figuras e correlações usam PIB per capita WDI a preços constantes de 2015 (`NY.GDP.PCAP.KD`), não PIB corrente deflacionado por CPI. A variável CPI-deflacionada antiga permanece identificada como proxy e fora dos resultados centrais.
- Harmonizados rótulos históricos de contas DCA, sem somar contas-pai às subcontas. A rubrica brasileira de transferências é apresentada como agregação ampla de contas correntes e de capital, não como medida perfeitamente isolada de transferências intergovernamentais.
- Mantidas explícitas as diferenças entre tributos próprios municipais brasileiros e receita própria local chinesa (tributária e não tributária), bem como a exclusão de fundos de uso da terra e outras fontes extraorçamentárias no agregado fiscal chinês.
- Criados painéis CSV, dicionário de variáveis, aba XLSX atualizada, estatísticas, gráficos e verificações de qualidade. Valores ausentes não foram substituídos por zero; população de 2023 é marcada como proxy e PIB municipal não é extrapolado.
- Produzido artigo em português, identificado pela matrícula, com pergunta verificável, metodologia, resultados descritivos, limitações, glossário e referências. Após nova auditoria Crossref com retentativas, a literatura temática contém 97 artigos de periódico com DOI, título compatível e tipo editorial `journal-article`, todos citados e discutidos no texto; quatro registros permaneceram em revisão manual. Documentos oficiais e trabalhos metodológicos estão separados da contagem mínima.
- Executada análise bibliométrica em R com bibliometrix 5.5.0: produção anual, periódicos, autores, contextos nacionais e rede de coocorrência baseada em termos harmonizados. A visualização não é apresentada como rede de co-citação nem como palavras-chave autorais.
- Incluída nota de transparência sobre assistência de IA: o arquivo é um rascunho de pesquisa e não certifica autoria individual. Revisão e declaração conforme as normas da disciplina são necessárias antes de eventual submissão.

## Alterações em relação ao ponto de partida

O material anterior foi preservado, não sobrescrito. A atualização reconstrói os painéis a partir das fontes primárias, amplia a coleta fiscal a 2025, separa o painel de PIB municipal até 2023, documenta mudanças de classificação e de conceitos, incorpora fontes chinesas atualizadas, corrige a mensuração do PIB chinês e fornece rotinas para reproduzir tratamento, estatísticas, gráficos e artigo.
