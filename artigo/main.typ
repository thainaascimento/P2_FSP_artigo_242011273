#set document(title: "Transferências intergovernamentais, receitas próprias e atividade econômica", author: "Thainá Cristine Martins do Nascimento")
#set page(paper: "a4", margin: (top: 2.2cm, bottom: 2.2cm, left: 2.5cm, right: 2.5cm))
#set text(font: "Libertinus Serif", size: 10pt, lang: "pt", region: "BR")
#set par(leading: 0.65em, spacing: 0.55em, justify: true)
#set heading(numbering: "1.")
#show heading.where(level: 1): set text(size: 14pt, weight: "bold")
#show heading.where(level: 2): set text(size: 11pt, weight: "bold")
#align(center)[
  #text(size: 17pt, weight: "bold")[Transferências intergovernamentais, receitas próprias e atividade econômica: evidência descritiva de Cascavel, Londrina e do agregado local da China, 2016–2025]
  #v(12pt)
  #text(size: 10pt)[Thainá Cristine Martins do Nascimento — Matrícula 242011273 — Finanças do Setor Público]
]
#v(12pt)
#v(4pt)
= 1 Introdução
#par(justify: true)[Transferências entre níveis de governo financiam serviços locais, reduzem desigualdades de capacidade fiscal e podem alterar incentivos à arrecadação e ao gasto. A literatura, contudo, não prevê uma resposta única. O gasto pode reagir mais a um repasse do que a uma elevação equivalente da renda dos residentes — o efeito flypaper (EF) —, mas o padrão também pode decorrer da regra de distribuição, da composição do grant, do processo orçamentário, da capacidade tributária ou de problemas de mensuração. Uma correlação entre transferências e despesas, por si só, não distingue esses mecanismos. A pergunta verificável deste artigo é: entre 2016 e 2025, como variaram as transferências reportadas, a receita tributária própria, a despesa pública e as medidas disponíveis de atividade econômica em Cascavel/PR e Londrina/ PR, e em que medida essas trajetórias se aproximam ou diferem das observadas no agregado de governos locais da China? O objetivo é descrever níveis reais, valores per capita, participações fiscais e associações temporais, sem inferir efeitos causais. As unidades são dois municípios brasileiros e um agregado nacional local chinês; portanto, a comparação identifica contrastes de trajetória, não equivalência de jurisdição ou de sistema fiscal. A escolha de Cascavel e Londrina segue o material anterior associado à matrícula, preservado sem sobrescrita e identificado no repositório indicado pelo aluno \[107\]. O trabalho anterior e seus arquivos Finbra serviram para reconhecer o escopo e as variáveis a reconstruir, mas não foram tratados como fonte atual suficiente. A nova extração utiliza os anexos anuais da Declaração de Contas Anuais (DCA) do Siconfi e inclui os dez exercícios fiscais completos mais recentes encontrados para a análise, 2016–2025 \[100\]. O PIB municipal do IBGE está disponível somente até 2023; por isso, a atividade econômica local é comparada até esse ano, sem extrapolação \[101\]. A China é examinada por meio dos valores nacionais do orçamento público geral local publicados pelo Ministry of Finance, e não por uma amostra de cidades. Esse agregado registra receita própria local, transferências centrais recebidas e despesa orçamentária, mas não abrange todos os fundos, a receita de uso da terra ou o financiamento extraorçamentário. A atividade chinesa é medida pelo PIB per capita real do WDI \[103\] \[105\]. A unidade adminis- trativa, a abrangência orçamentária e as categorias de receita não são equivalentes às brasileiras. A comparação usa moeda local real, proporções e, apenas para facilitar a visualização, valores por habitante em dólares ao câmbio de mercado de 2025; não usa paridade do poder de compra (PPC). A contribuição empírica é uma atualização auditável de dez anos, com dados brutos, painéis tratados, dicionário, código e registro de mudanças. A contribuição analítica é mais modesta: documenta quais padrões descritivos são compatíveis — e quais não podem ser chamados — de evidência de resposta flypaper. Da tese de Ferreira \[99\] reapro- veitam-se o enquadramento sobre transferências constitucionais e autonomia tributária, a atenção à endogeneidade e a organização de despesa, receita e atividade econômica. Não se reutilizam seus dados, estimativas, instrumentos ou índices. A estrutura da primeira página — título, identificação, resumo, palavras-chave e códigos JEL — e a abertura da introdução na página seguinte seguem a organização editorial observada nas páginas iniciais de Baker, Larcker e Wang \[98\], sem reproduzir texto, resultados ou estratégia de estimação.]
= 2 Referencial teórico
== 2.1 Efeito flypaper: mecanismo, heterogeneidade e identificação
#par(justify: true)[Oates \[19\] situa essas respostas no problema mais amplo de distribuir responsabilidades, receitas e instrumentos entre níveis de governo; Rodden \[23\] mostra que dependência persistente de grants pode acompanhar desempenho fiscal subnacional frágil. O contraste entre a previsão do eleitor mediano e a resposta observada do orçamento local é o núcleo do debate. Hamilton \[2\] mostra que substituições na produção de serviços públicos podem gerar respostas distintas à renda privada e a grants; Hamilton \[4\] associa a diferença ao custo marginal crescente da tributação. A hipótese burocrática de Wyckoff \[6\] explica melhor algumas despesas de capital do que as operacionais, enquanto Schneider e Ji \[5\] não encontram que a competição local limite o fenômeno de forma consistente. Turnbull \[9\] desloca a explicação para incerteza e informação imperfeita. A síntese de Hines e Thaler \[12\] documenta a discrepância entre previsões teóricas modestas e respostas empíricas maiores, mas Bailey e Connolly \[17\] ressaltam que a própria existência e explicação do efeito permanecem contestadas.]
#v(4pt)
#par(justify: true)[A identificação importa tanto quanto o sinal. Brennan e Pincus \[13\] demonstram que a origem da variação dos repasses pode produzir efeitos aparentes; Becker \[14\] mostra como especificações funcionais inadequadas podem gerar um flypaper espúrio. Wyckoff \[8\] não confirma quatro explicações em seus dados, e Worthington e Dollery]
#par(justify: true)[\[20\] encontram sensibilidade à forma funcional no contexto australiano. Já regras de elegibilidade descontínuas]
#par(justify: true)[permitem desenhos mais informativos sobre respostas de gasto e tributos, como em Dahlberg et al. \[34\]. A evidência também varia por tipo de transferência, por despesa e por aumento ou redução do repasse: Mehiriz e Marceau \[48\] relatam assimetria no Quebec, Kjaergaard \[53\] encontra assimetria na Dinamarca e Rios, Hortas-Rico e Pascual \[79\] relacionam a intensidade do efeito à força política local e à eficiência arrecadatória. Lundqvist \[49\] estima resposta positiva e imediata do gasto local a grants, com efeito menor sobre impostos de renda e sem evidência de reversão dinâmica. Assim, uma série curta de despesas e transferências agregadas, sem variação exógena, não identifica o parâmetro estrutural do efeito.]
== 2.2 Ilusão fiscal, autonomia e regras de equalização
#par(justify: true)[A ilusão fiscal (IF) propõe que a origem, a visibilidade e a percepção do custo dos recursos alteram a demanda por gasto. Hewitt \[3\] e Grossman \[7\] encontram respostas compatíveis com a separação entre quem financia e quem decide o gasto. Oulasvirta \[15\] mostra que transferências vinculadas e com contrapartida podem produzir respostas diferentes das transferências gerais; Turnbull \[18\] modela como informação incompleta sobre custos e benefícios afeta o orçamento. Mitias e Turnbull \[21\] tratam ilusão sobre grants e sobre tributos como mecanismos interdependentes. Em contraste, Maher e Johnson \[33\] acham pouca evidência sistemática em survey de governos locais, e o estudo de Worthington e Dollery \[20\] evidencia dependência de especificação. Esses resultados recomendam não inferir ilusão fiscal apenas da participação elevada de transferências. A relação entre grants e arrecadação própria tampouco é necessariamente de substituição. Longo \[1\] associa depen- dência de transferências a menor exploração da base tributária municipal, e Araujo e Siqueira \[55\] mostram que estrutura tributária e percepção de preço fiscal ajudam a explicar a demanda local por gasto no Brasil. Caldeira e Rota-Graziosi \[47\] encontram crowding-in da receita própria no Benim, mais forte acima de um limiar de riqueza e em municípios sem alinhamento político com o presidente. Mas Gadenne \[57\] encontra que reforçar a capacidade tributária municipal melhora a provisão de infraestrutura educacional, enquanto transferências discricionárias comparáveis não produzem o mesmo resultado. Evidências sobre spillovers \[74\], capital e despesas correntes \[78\], incentivos ligados a regras de gasto mínimo \[71\], despesas administrativas \[90\] e indicadores socioeconômicos da capacidade fiscal \[95\] ampliam o conjunto de mecanismos, sem tornar receita tributária um substituto perfeito de toda receita própria. Equalização pode reduzir disparidades e, simultaneamente, alterar incentivos. Baretti, Huber e Lichtblau \[22\] encon- tram efeitos de substituição associados a menor receita tributária nos estados alemães; Buettner \[31\] e Ferede \[59\] mostram que regras marginais de equalização também podem alterar alíquotas. Miyazaki \[70\] e Buettner e Krause]
#par(justify: true)[\[72\] apontam respostas tributárias estratégicas em sistemas japonês e alemão. Já Masaki \[64\] registra aumento da]
#par(justify: true)[mobilização de receita própria após transferências na Tanzânia, em especial em distritos rurais; Mogues e Benin]
#par(justify: true)[\[39\] encontram resultado agregado em sentido oposto para governos distritais ganeses. Shani et al. \[83\] mostram]
#par(justify: true)[assimetria entre cortes e aumentos de grants em Israel, e Le e Young \[85\] destacam que a composição da receita própria — tributos, multas e tarifas — tem implicações distributivas. Essas divergências tornam indispensável explicitar a rubrica contábil antes de interpretar “esforço fiscal”.]
== 2.3 Evidência brasileira e efeitos sobre serviços e atividade
#par(justify: true)[A evidência brasileira não é uniforme, o que torna inadequado tratar uma única estimativa como fato geral. Mattos, Rocha e Arvate \[36\] encontram efeito de transferências incondicionais sobre gastos municipais usando instrumentos baseados em regras constitucionais; Ferreira, Serrano e Revelli \[66\] também reportam flypaper e heterogeneidade por alinhamento político e autonomia tributária. Em contraste, Costa e Castelar \[52\] não confirmam o efeito em sua especificação com VAR em painel e regressões quantílicas. Pansani, Serrano e Ferreira \[69\] encontram evidência de flypaper e parcialmente de ilusão fiscal em painel estadual, não equivalente a um painel de municípios. Luz et al. \[78\] separam despesas de capital das correntes; Lima Filho et al. \[84\] medem eficiência arrecadatória associada]
#v(4pt)
#par(justify: true)[a transferências voluntárias, não a elasticidade clássica do gasto. Bernardelli et al. \[96\] reportam efeitos do FPM sobre despesas e receita própria em municípios paulistas. A diferença entre fonte, amostra, desfecho e estratégia de identificação é parte da explicação para resultados divergentes. Transferências também podem afetar provisão de serviços, renda e estrutura produtiva por canais que não se resumem ao gasto total. Litschig e Morrison \[43\] usam uma descontinuidade para avaliar educação e pobreza, enquanto Carvalho Filho e Litschig \[76\] acompanham a persistência de efeitos de longo prazo. O programa Bolsa Família aparece ligado a crescimento local e mudança estrutural em Rougier, Combarnous e Fauré \[65\]. Corbi, Papaioannou e Surico \[67\] estimam multiplicadores regionais brasileiros com uma variação de regra de repasse; a análise de spillovers de Castro e Mattos \[74\] destaca interdependência municipal. Cruz e Silva \[71\] mostram que pisos educacionais condicionam a resposta do gasto. Esses desenhos identificam mecanismos que os dados agregados anuais deste artigo não conseguem isolar.]
== 2.4 China: instituições, orçamento e financiamento local
#par(justify: true)[O caso chinês combina descentralização de responsabilidades, incentivos ao crescimento local e coordenação central. Oi \[10\] e Montinola, Qian e Weingast \[11\] descrevem como reformas e competição entre governos locais moldaram os incentivos econômicos; Jin, Qian e Weingast \[29\] examinam incentivos fiscais do modelo chinês. Zhang e Zou \[16\] encontram associação negativa entre descentralização de despesa e crescimento provincial em determinado período, enquanto Zhang \[30\] e Brehm \[41\] mostram como bases tributárias, incentivos e produtividade alteram os resultados. Niu \[40\] distingue graus de descentralização entre níveis administrativos, e Liu e Hung \[80\] vinculam a reforma fiscal de 1994 a incentivos ambientais. Tsui \[28\] questiona a redução sustentada das disparidades após a reforma. O conjunto não autoriza projetar um único “efeito chinês” para o agregado nacional recente. As contas e os canais de receita também importam. Liu e Zhao \[37\] identificam relação entre transferências e esforço tributário provincial; Huang e Chen \[38\] avaliam componentes equalizadores. Zhang \[44\] distingue devoluções tributárias, transferências de capacidade fiscal e repasses específicos; Wu et al. \[61\] relacionam a composição das transferências à eficiência fiscal. Huang et al. \[63\] mostram que muitos subsídios educacionais podem substituir recursos locais, ao passo que Tu et al. \[94\] relatam associação entre transferências, reorganização do gasto e serviços de saúde. Lü \[51\], avaliando um programa antipobreza, não encontra aumento sistemático de gasto educacional ou redução do analfabetismo. Tan e Tan \[87\] ressaltam que equalização central e provincial não elimina desigualdades intrarregionais. O orçamento público geral não esgota o financiamento subnacional chinês. Eckaus \[25\] e Zhan \[42\] estudam receitas extraorçamentárias; Ding, Niu e Lichtenberg \[46\] analisam receitas da terra e a composição do gasto urbano. Jia, Guo e Zhang \[45\] mostram que a descentralização da despesa pode mudar a composição entre capital, educação e administração. Gyourko et al. \[75\] sintetizam o papel da land finance, e Guo e Liang \[91\] evidenciam como regras de carryover podem alterar o momento do gasto. Yan e Reschovsky \[81\] mostram que equalização reduz, mas não elimina, disparidades em Zhejiang; Liu e Hu \[92\] encontram que a equalização pode favorecer crescimento em condados menos desenvolvidos sem elevar necessariamente a eficiência agregada. Esses canais delimitam a série MOF usada aqui: ela descreve o orçamento público geral local, não o conjunto dos recursos ou passivos de governos locais.]
== 2.5 Evidência comparada e expectativas
#par(justify: true)[Resultados fora dos dois países ajudam a separar mecanismos sem presumir transferibilidade institucional. Faguet]
#par(justify: true)[\[26\] associa descentralização boliviana a maior correspondência entre investimento e necessidades; Reinikka e]
#par(justify: true)[Svensson \[27\] mostram risco de captura de grants em Uganda. Arulampalam et al. \[35\] identificam distribuição política de transferências na Índia. Em desenhos e contextos diversos, Amusa et al. \[32\] e Mogues e Benin \[39\] estudam ilusão e receita; Kis-Katos e Sjahrir \[58\] discutem investimento local e descentralização na Indonésia; Sacchi e Salotti \[60\] ligam volatilidade das receitas à do gasto. Vincent e Kwadwo \[77\] documentam difusão espacial de grants e spillovers entre governos locais no Benin, reforçando que unidades vizinhas podem não ser independentes. O objetivo desta síntese é contrastar mecanismos e não supor que coeficientes de países, níveis de governo ou regras fiscais distintas sejam diretamente comparáveis.]
#v(4pt)
#par(justify: true)[As comparações adicionais reforçam que o desenho do grant e a métrica do resultado são decisivos. Tovmo e Falch]
#par(justify: true)[\[24\] relacionam efeito flypaper e força política; Bracco et al. \[50\] estudam alinhamento e grants na Itália; Allers e]
#par(justify: true)[Vermeulen \[54\] mostram capitalização imobiliária de equalização nos Países Baixos; Baekgaard e Kjaergaard \[56\] não encontram que a fonte do recurso domine a ideologia em experimento com políticos dinamarqueses. Canare]
#par(justify: true)[\[68\] estima resposta de despesa a repartição de receita nas Filipinas. Danisewicz e Ongena \[88\] associam grants e]
#par(justify: true)[empreendedorismo na Polônia, e Dick-Sagoe et al. \[93\] reportam flypaper e incentivos arrecadatórios em Gana. Em resultados de desenvolvimento, Dawid et al. \[62\] analisam crescimento regional; Henkel et al. \[73\], efeitos espaciais; Ajefu e Ogebe \[82\], bem-estar na Nigéria; Tang et al. \[86\], renda e pobreza nas Filipinas; e Sánchez-Aragón et al. \[97\], vendas locais no Equador. A revisão de Lago, Lago-Peñas e Martinez-Vazquez \[89\] sintetiza a heterogeneidade e a lacuna de identificação. Dessa literatura decorrem expectativas descritivas, não hipóteses causais testadas aqui. Espera-se que transferências relevantes acompanhem a escala da despesa; a hipótese flypaper, porém, exigiria estimar a resposta marginal do gasto a grants relativamente à resposta a renda própria dos residentes, o que não é possível com estas variáveis agregadas. Para a receita própria, admite-se tanto crowding-out quanto crowding-in, condicionado por desenho e capacidade de arrecadação. Para atividade econômica, espera-se associação temporal positiva em alguns contextos, mas reconhece- -se que crescimento pode simultaneamente ampliar receitas, alterar transferências e elevar gastos. O estudo testa somente se as trajetórias observadas são consistentes com essas expectativas descritivas.]
= 3 Metodologia
== 3.1 Delineamento, unidades e período
#par(justify: true)[O estudo é quantitativo, longitudinal e descritivo. O painel principal contém duas unidades municipais brasileiras — Cascavel e Londrina — e uma unidade agregada, “governos locais da China”, observadas anualmente em 2016–2025. Não se trata de um painel de 3 unidades homogêneas: o agregado chinês soma governos subnacionais sob orçamento público geral, enquanto cada observação brasileira corresponde a um único município. O recorte cobre dez exercícios completos nas fontes fiscais disponíveis na data de acesso, 22 de outubro de 2026. A série de atividade econômica municipal tem cobertura menor, 2014–2023; por isso, as análises de PIB usam a janela comum 2016–2023.]
== 3.2 Fontes e construção das variáveis
#par(justify: true)[No Brasil, receitas são extraídas do anexo I-C da DCA-Siconfi e despesas empenhadas por função do anexo I-E. Receita total exclui intraorçamentárias; para versões em que o total não é publicado como conta única, é reconstruída pela soma das receitas correntes e de capital. Receita tributária própria corresponde à conta-pai 1.1.0.0. Transferências são a soma das contas-pai 1.7.0, correntes, e 2.4.0, de capital. É uma categoria ampla de transferências reportadas e pode conter itens além de transferências intergovernamentais estritas. Não se somam as contas-pai às subcontas. A despesa total é a empenhada, excluídas intraorçamentárias; saúde e educação são mantidas em colunas próprias para extensão futura \[100\]. Para a China, os relatórios anuais do Ministry of Finance informam receita própria do orçamento público geral local, transferências centrais recebidas, receita local total e despesa local. O registro original está em 亿元, isto é, 100 milhões de yuans, e é convertido a CNY pela multiplicação por 100 milhões. Receita própria local inclui componentes tributários e não tributários; não equivale a receita tributária municipal brasileira. O escopo exclui fundos públicos de uso da terra, previdência social e outras fontes extraorçamentárias. A própria execução local publicada é usada para manter a identidade contábil entre receita própria, transferências recebidas e receita local total \[103\]. Valores nominais são deflacionados em cada país para preços médios de 2025. No Brasil, encadeia-se a série mensal do IPCA do Banco Central (SGS 433), calcula-se a média dos índices de cada ano e multiplica-se o fluxo pelo quociente entre o índice médio de 2025 e o do ano observado \[102\]. Na China, usa-se a razão entre o CPI anual do WDI em 2025 e o do ano observado \[105\]. O WDI é usado também para população, câmbio médio CNY/USD e PIB nacional real per capita a preços constantes de 2015. O indicador de atividade é NY.GDP.PCAP.KD, não PIB corrente ajustado]
#v(4pt)
#par(justify: true)[pelo CPI: este último permanece apenas como variável identificada como proxy nominal e não entra nas figuras ou correlações. O comunicado estatístico do NBS para 2025 serve como conferência externa da disponibilidade recente de população e preços; para manter continuidade temporal e metadados comparáveis, as séries quantitativas do painel chinês permanecem baseadas no WDI \[106\]. As observações per capita dividem fluxos reais pela população da unidade no mesmo ano. Para Cascavel e Londrina, usam-se as estimativas IBGE/SIDRA da tabela 6579 nos anos em que a série anual está disponível (2016–2021); para 2022 e 2023, usa-se a população do Censo Demográfico de 2022, com 2023 explicitamente marcado como proxy estática, também reproduzida na relação populacional do IBGE ao TCU de 2023 \[101\]. Não se interpola crescimento. Para a China, usa-se população anual WDI. Para facilitar a leitura da escala, os fluxos brasileiros em BRL de 2025 e os chineses em CNY de 2025 são convertidos para USD usando as taxas médias de mercado de 2025: BRL 5,587286/USD e CNY 7,189847/USD \[101\] \[105\]. Essa conversão fixa um câmbio comum dentro de cada série e não é uma medida de paridade de poder de compra. O PIB municipal é obtido na tabela SIDRA 5938, variável 37, em valores correntes e com série de referência-base 2010; os valores são deflacionados pelo IPCA para reais médios de 2023 e divididos pela população. O PIB per capita chinês é a série WDI em dólares constantes de 2015. Para visualizar a trajetória, cada série é indexada a 2016=100. Os níveis não são comparados entre países, e não se atribui equivalência entre PIB municipal e PIB nacional \[101\] \[105\].]
== 3.3 Indicadores e análise
#par(justify: true)[Para cada unidade e ano, calcula-se a participação das transferências na receita local: sT\_it = 100 × T\_it / R\_it; para o Brasil, a participação da receita tributária própria é sTax\_it = 100 × Tax\_it / R\_it. Na China, a medida correspondente é receita própria local, tributária e não tributária, dividida pela receita local. A medida per capita é pc\_it = Xreal\_it / Pop\_it. A diferença é mantida explícita no texto e no dicionário. As taxas de variação comparam 2016 e 2025 em termos reais. Tabelas e gráficos usam valores não arredondados internamente; os números apresentados são arredondados para facilitar a leitura. As associações são coeficientes de correlação de Pearson calculados em níveis anuais para transferências per capita e despesas per capita, e para transferências per capita e a medida de receita própria; também são calculadas correlações entre variações anuais e PIB per capita na janela disponível. O tamanho amostral é n=10 para a série fiscal, n=9 para primeiras diferenças e n=8 para PIB. Não se estima regressão, não se reportam valores-p e não se fazem testes de raiz unitária, autocorrelação ou heterocedasticidade: com apenas dez anos por unidade, tais procedimentos não sustentariam inferência confiável. Em particular, correlações em níveis podem refletir tendências comuns. As primeiras diferenças são um diagnóstico exploratório, não removem endogeneidade nem constituem desenho causal. O corpus bibliométrico reúne artigos sobre teoria flypaper, ilusão fiscal, transferências no Brasil e na China, equali- zação, arrecadação própria e efeitos sobre atividade econômica. Foram consolidados 101 candidatos distintos por DOI; 97 artigos tiveram DOI acessível, título editorial compatível e tipo Crossref “journal-article”, além de periódico e endereço editorial verificáveis. Quatro registros ficaram em revisão manual e foram excluídos da contagem. O corpus cobre 1981–2026, 53 periódicos e 176 autores. As frequências e a rede de coocorrência foram calculadas em R com bibliometrix 5.5.0 \[108\]. Como as referências citadas pelos artigos não foram coletadas de forma sistemática, a visualização em rede usa termos harmonizados de títulos, resumos e descrições temáticas, não co-citação nem palavras-chave autorais. A codificação de países indica cenário empírico, não afiliação; 31 artigos não tiveram país identificado.]
= 4 Resultados
== 4.1 Estudo bibliométrico
#par(justify: true)[A produção do corpus começa em 1981 e se estende até 2026, com crescimento recente: seis artigos em 2023, cinco em 2024, cinco em 2025 e dois em 2026 até a data da coleta. Journal of Public Economics é o periódico mais recorrente (n=9), seguido por China Economic Review (7), World Development (6) e Public Choice (5). Geoffrey]
#v(4pt)
#par(justify: true)[K. Turnbull aparece em três artigos; os demais autores de maior frequência têm dois cada. Esses números descrevem o corpus selecionado e não medem qualidade ou influência de citação. Na codificação dos contextos empíricos, China (25 menções), Estados Unidos (18) e Brasil (15) são os mais frequentes. Os termos harmonizados mais recorrentes são transferências intergovernamentais (72), despesa pública local (54), receita própria e esforço fiscal (39), efeito flypaper (31) e atividade econômica e desenvolvimento (27). A rede abaixo representa coocorrência entre termos extraídos e harmonizados. Como 31 artigos não tiveram contexto nacional identificável e um artigo pode mencionar mais de um país, essas frequências não devem ser lidas como participação de afiliações ou como distribuição exaustiva da produção mundial.]
#align(center)[#text(size: 9pt, style: "italic")[Figura 1: Painel bibliométrico do corpus de 97 artigos, processado com bibliometrix 5.5.0.]]
#align(center)[
  #image("figures/figure-000.jpg", width: 95%)
  #v(4pt)
  #image("figures/figure-001.jpg", width: 95%)
  #v(4pt)
  #image("figures/figure-002.jpg", width: 95%)
  #v(4pt)
]
#v(4pt)
== 4.2 Trajetórias fiscais, 2016–2025
#par(justify: true)[A Tabela 1 resume as mudanças entre os pontos inicial e final. Em valores reais per capita convertidos a USD de mercado a preços de 2025, as transferências aumentaram 33,4% em Cascavel, 33,6% em Londrina e 49,4% no agregado local chinês. A participação das transferências na receita local caiu 4,83 pontos percentuais em Cascavel e 3,24 pontos em Londrina, enquanto subiu 4,95 pontos no agregado chinês. A participação tributária própria brasileira avançou 5,18 pontos em Cascavel e 10,96 pontos em Londrina. A participação de receita própria chinesa recuou na mesma magnitude da participação das transferências porque o denominador local soma essas duas rubricas; a categoria própria chinesa inclui receitas não tributárias.]
#table(columns: (2fr, 1fr, 1fr, 1fr, 1fr), inset: 4pt, align: left, [*Indicador*], [*Unidade*], [*2016*], [*2025*], [*Variação*],
  [Transferências reais per capita], [Cascavel], [398,22], [531,29], [+33,4%],
  [Transferências reais per capita], [Londrina], [413,58], [552,56], [+33,6%],
  [Transferências reais per capita], [China local], [674,38], [1.007,85], [+49,4%],
  [Transferências / receita local], [Cascavel], [53,60%], [48,77%], [−4,83 p.p.],
  [Transferências / receita local], [Londrina], [48,81%], [45,58%], [−3,24 p.p.],
  [Transferências / receita local], [China local], [40,55%], [45,50%], [+4,95 p.p.],
  [Tributos próprios / receita], [Cascavel], [25,34%], [30,52%], [+5,18 p.p.],
  [Tributos próprios / receita], [Londrina], [28,36%], [39,32%], [+10,96 p.p.],
  [Receita própria / receita local], [China local], [59,45%], [54,50%], [−4,95 p.p.],
  [Despesa real per capita], [Cascavel], [687,18], [954,52], [+38,9%],
  [Despesa real per capita], [Londrina], [813,56], [1.117,96], [+37,4%],
  [Despesa real per capita], [China local], [1.818,82], [2.416,28], [+32,8%],
)
#align(center)[#text(size: 9pt, style: "italic")[Tabela 1: Indicadores fiscais selecionados, base de preços 2025. Valores per capita em USD de mercado; participações]]
#par(justify: true)[em percentuais da receita reportada. Nota: transferências brasileiras somam contas DCA correntes e de capital; na China são recebimentos centrais no orçamento público geral. “Tributos próprios” é a receita tributária municipal brasileira; “receita própria” chinesa inclui componentes tributários e não tributários. As categorias não são equivalentes. Fonte: Siconfi, Ministry of Finance, IBGE, BCB e WDI \[100\] \[101\] \[102\] \[103\] \[105\]. O aumento dos fluxos por habitante não implica dependência crescente em todas as unidades. As participações brasileiras caíram mesmo com o crescimento real das transferências, porque as receitas locais e, especialmente em Londrina, a parcela tributária também avançaram. Na China, transferências centrais cresceram mais rapidamente do que a receita própria local no agregado do orçamento público geral e sua participação aumentou. O contraste é compatível com diferenças de desenho e de base fiscal; não é evidência de maior ou menor esforço tributário comparável. A despesa empenhada real por habitante aumentou 38,9% em Cascavel e 37,4% em Londrina. A despesa do orçamento geral local chinês aumentou 32,8% per capita em USD de mercado. Embora esses aumentos sejam todos positivos, os estágios e conceitos contábeis diferem: empenho municipal brasileiro não é idêntico à execução orçamentária local chinesa. Os níveis em dólares não são uma medida de bem-estar nem de volume homogêneo de serviços. O uso principal da conversão é ilustrar escala; as comparações mais robustas dentro de cada unidade são as variações reais e as participações fiscais.]
#v(4pt)
#align(center)[#text(size: 9pt, style: "italic")[Figura 2: Transferências, despesas e composição das receitas, em séries reais per capita e participações fiscais.]]
== 4.3 Transferências, despesas e receitas próprias
#par(justify: true)[A correlação entre transferências reais per capita e despesa real per capita em níveis é positiva nas três séries: r=0,940 em Cascavel, r=0,915 em Londrina e r=0,956 no agregado chinês (n=10 em cada caso). Entretanto, quando se correlacionam as primeiras diferenças anuais, os coeficientes caem para 0,140, 0,067 e 0,366 (n=9). A queda sinaliza que boa parte da associação em níveis pode refletir tendência comum, expansão nominal corrigida por preços ou outros fatores temporais. Não há interpretação causal ou inferencial desses coeficientes. A correlação em níveis entre transferências e receita tributária própria brasileira é 0,921 em Cascavel e 0,876 em Londrina. Na China, a correlação com receita própria local é 0,856; essa variável incorpora itens não tributários. Os sinais positivos não permitem escolher entre crowding-in e crowding-out: a receita própria pode crescer junto com transferências por expansão econômica, regras de repartição, mudanças de base ou simultaneidade. O resultado é consistente com a literatura que encontra ambos os sinais sob diferentes regras e capacidades fiscais, mas não estima a resposta de receita a um choque exógeno de transferências. O rótulo flypaper também não pode ser atribuído a essas correlações. O teste clássico compara a resposta marginal do gasto a um grant com a resposta marginal a um aumento equivalente da renda privada dos residentes. A base não contém renda domiciliar comparável para os dois municípios e para o agregado chinês, nem uma fonte exógena de variação nos repasses. Além disso, a rubrica brasileira agrega transferências correntes e de capital de diversas origens. Assim, os dados mostram co-movimento fiscal, mas não comprovam ilusão fiscal, baixa arrecadação causada por transferências ou efeito flypaper.]
== 4.4 Atividade econômica
#par(justify: true)[A Figura 3 indexa em 2016=100 o PIB municipal real per capita do IBGE em Cascavel e Londrina e o PIB nacional per capita chinês em volume. A cobertura municipal termina em 2023, enquanto a série chinesa segue até 2025; a comparação desenhada limita-se a 2016–2023. A correlação em níveis entre transferências reais per capita e PIB per capita nessa janela é 0,958 em Cascavel, 0,580 em Londrina e 0,955 entre o agregado local chinês e o PIB nacional (n=8). Para a China, a correlação mistura dois níveis territoriais diferentes. Os valores elevados em Cascavel e China são especialmente vulneráveis a tendências comuns e amostra curta; não devem ser interpretados como multiplicadores.]
#align(center)[
  #image("figures/figure-003.jpg", width: 95%)
  #v(4pt)
  #image("figures/figure-004.jpg", width: 95%)
  #v(4pt)
]
#v(4pt)
#align(center)[#text(size: 9pt, style: "italic")[Figura 3: Trajetórias de atividade econômica real per capita indexadas a 2016=100; municípios até 2023.]]
#par(justify: true)[O PIB municipal de 2022 e 2023 segue a série de referência 2010 do IBGE disponível na data de coleta, sujeita a revisão futura das Contas Nacionais. A população de 2023 é proxy censitária explicitamente identificada, não uma estimativa demográfica anual. A série chinesa emprega WDI NY.GDP.PCAP.KD, em USD constantes de 2015; uma versão anterior do trabalho havia ajustado PIB corrente pelo CPI, o que não mede volume real. O campo antigo foi renomeado para proxy e retirado das figuras e correlações de atividade. Nenhum dado de PIB municipal foi extrapolado para 2024–2025.]
== 4.5 Revisões, lacunas e mudança frente ao trabalho anterior
#par(justify: true)[A base anterior fornecida pelo repositório do aluno foi preservada na pasta dados/originais, e seus hashes estão registrados. Ela continha arquivos Finbra com cobertura até 2022 e planilhas de despesas; a série nova reextrai os exercícios DCA de 2014–2025 para as duas cidades, mas a janela comparativa principal utiliza 2016–2025. A atualização amplia a cobertura fiscal em três anos além de 2022 e separa um painel histórico municipal com PIB até 2023. O novo tratamento documenta mudanças de rótulos contábeis da receita tributária, harmonizadas pelo código estrutural 1.1.0.0, e evita somar contas-pai às suas subcontas. Também mantém transferências correntes e de capital explícitas e nomeia a variável como categoria ampla, em vez de assumir equivalência perfeita com transferências intergovernamentais. Na China, a série foi transcrita das execuções anuais oficiais do orçamento público geral local. Para 2022, o recebi- mento reportado localmente é 97.144,75 unidades de 100 milhões de CNY; a prestação central final reporta despesa de transferência de 96.941,82, diferença de 202,93 (0,209% do valor local). Para 2025, os valores correspondentes são 101.925,14 e 101.835,49, diferença de 89,65 (0,088%). Os dois conceitos — receita local recebida e despesa central executada — são preservados em colunas distintas e não conciliados por substituição silenciosa \[104\] \[103\]. A sensibilidade não altera a decisão de usar os recebimentos locais para fechar a identidade da receita local; não se afirma igualdade contábil entre os registros. A cobertura populacional municipal depois do Censo também exige cautela: mantém-se a população censitária como proxy de 2023 e não há interpolação. Para todas as fontes, dados ausentes não são substituídos por zero. Os fluxos fiscais essenciais do painel 2016–2025 estão completos para as três unidades; a limitação é de conceito e cobertura de algumas variáveis complementares, em especial PIB municipal. Revisões estatísticas futuras, mudanças de classi- ficação e diferenças de estágio da despesa podem alterar comparações de nível.]
= 5 Conclusão
#par(justify: true)[A resposta à pergunta de pesquisa é descritiva. Entre 2016 e 2025, transferências reais per capita aumentaram nas duas cidades brasileiras e no agregado local chinês; a participação delas na receita caiu em Cascavel e Londrina e]
#align(center)[
  #image("figures/figure-005.jpg", width: 95%)
  #v(4pt)
]
#v(4pt)
#par(justify: true)[aumentou na China. A participação dos tributos próprios na receita municipal brasileira também cresceu, enquanto a medida chinesa de receita própria — mais ampla e não equivalente — diminuiu. As despesas reais por habitante aumentaram nas três séries, mas suas definições contábeis não são idênticas. As correlações em níveis entre transferências e despesas são positivas, mas diminuem fortemente nas primeiras diferenças. Esse padrão é compatível com trajetórias fiscais que crescem ao longo do tempo e não demonstra que transferências causem despesas, reduzam arrecadação própria ou produzam ilusão fiscal. O efeito flypaper permanece não testado: faltam uma medida comparável de renda privada, variação exógena dos repasses e unidades institucionais homogêneas. Tampouco se deve interpretar a associação entre PIB e transferências como multiplicador econômico. A principal contribuição é uma base atualizada, reprodutível e acompanhada de fontes, dicionário, código e registro de mudanças. O estudo reaproveita da tese de Ferreira o enquadramento de autonomia fiscal, transferências e endogeneidade, mas constrói novas séries e não replica as estimativas da tese. A comparação Brasil–China explicita diferenças de nível governamental e orçamento, em vez de ocultá-las em conversões cambiais. Pesquisas futuras podem combinar painéis municipais mais longos, contas harmonizadas, renda domiciliar, bases tributárias e regras exógenas de transferência; podem também separar transferências vinculadas e discricionárias, tributos e receitas não tributárias, despesa empenhada e paga, e recursos orçamentários e extraorçamentários na China. Com mais unidades e anos, torna-se possível investigar tendências, dependência temporal e identificação causal com desenhos apropriados. Até lá, a conclusão prudente é que os padrões observados motivam testes mais fortes, não substituem esses testes.]
= 6 Glossário
#par(justify: true)[DCA – Declaração de Contas Anuais: Declaração contábil anual dos entes subnacionais publicada no Siconfi. 2 EF – efeito flypaper: Resposta do gasto público local a transferências relativamente maior do que a resposta a um aumento equivalente da renda privada local; sua identificação requer comparação estrutural apropriada. 2 IF – ilusão fiscal: Mecanismos de informação, percepção e atribuição de custos que podem alterar como eleitores ou governos avaliam o preço dos bens públicos e a origem dos recursos. 3 PPC – paridade do poder de compra: Conversão que ajusta diferenças de nível de preços entre países; não é utilizada na conversão cambial deste artigo. 2]
#v(4pt)
= 7 Referências
#par(justify: true)[\[1\] Carlos A. Longo (1981). A Note On Local Tax Revenues: the Case of Brazilian Municipalities. Public Finance Quarterly. DOI:]
#par(justify: true)[10.1177/109114218100900306]
#par(justify: true)[\[2\] Bruce W. Hamilton (1983). The flypaper effect and other anomalies. Journal of Public Economics. DOI: 10.1016/0047-2727(83)90040-3]
#par(justify: true)[\[3\] Daniel Hewitt (1986). Fiscal Illusion from Grants and the Level of State and Federal Expenditures. National Tax Journal. DOI: 10.1086/]
#par(justify: true)[ntj41788627]
#par(justify: true)[\[4\] Jonathan H. Hamilton (1986). The flypaper effect and the deadweight loss from taxation. Journal of Urban Economics. DOI:]
#par(justify: true)[10.1016/0094-1190(86)90036-7]
#par(justify: true)[\[5\] Mark Schneider, Byung Moon Ji (1987). The flypaper effect and competition in the local market for public goods. Public Choice. DOI:]
#par(justify: true)[10.1007/bf00123803]
#par(justify: true)[\[6\] Paul Gary Wyckoff (1988). A bureaucratic theory of flypaper effects. Journal of Urban Economics. DOI: 10.1016/0094-1190(88)90009-5]
#par(justify: true)[\[7\] Philip J. Grossman (1990). The Impact of Federal and State Grants on Local Government Spending: a Test of the Fiscal Illusion Hypothesis.]
#par(justify: true)[Public Finance Quarterly. DOI: 10.1177/109114219001800304]
#par(justify: true)[\[8\] Paul Gary Wyckoff (1991). The elusive flypaper effect. Journal of Urban Economics. DOI: 10.1016/0094-1190(91)90052-9]
#par(justify: true)[\[9\] Geoffrey K. Turnbull (1992). Fiscal illusion, uncertainty, and the flypaper effect. Journal of Public Economics. DOI:]
#par(justify: true)[10.1016/0047-2727(92)90027-d]
#par(justify: true)[\[10\] Jean C. Oi (1992). Fiscal Reform and the Economic Foundations of Local State Corporatism in China. World Politics. DOI: 10.2307/2010520]
#par(justify: true)[\[11\] Gabriella Montinola, Yingyi Qian, Barry R. Weingast (1995). Federalism, Chinese Style: The Political Basis for Economic Success in China.]
#par(justify: true)[World Politics. DOI: 10.1353/wp.1995.0003]
#par(justify: true)[\[12\] James R. Hines Jr., Richard H. Thaler (1995). The Flypaper Effect. Journal of Economic Perspectives. DOI: 10.1257/jep.9.4.217]
#par(justify: true)[\[13\] Geoffrey Brennan, J. J. Pincus (1996). A minimalist model of federal grants and flypaper effects. Journal of Public Economics. DOI:]
#par(justify: true)[10.1016/0047-2727(95)01543-4]
#par(justify: true)[\[14\] Elizabeth Becker (1996). The illusion of fiscal illusion: Unsticking the flypaper effect. Public Choice. DOI: 10.1007/bf00114876]
#par(justify: true)[\[15\] Lasse Oulasvirta (1997). Real and perceived effects of changing the grant system from specific to general grants. Public Choice. DOI:]
#par(justify: true)[10.1023/a:1004987824891]
#par(justify: true)[\[16\] Tao Zhang, Heng-fu Zou (1998). Fiscal decentralization, public spending, and economic growth in China. Journal of Public Economics.]
#par(justify: true)[DOI: 10.1016/s0047-2727(97)00057-1]
#par(justify: true)[\[17\] Stephen J. Bailey, Stephen Connolly (1998). The flypaper effect: Identifying areas for further research. Public Choice. DOI: 10.1023/]
#par(justify: true)[a:1005053921709]
#par(justify: true)[\[18\] Geoffrey K. Turnbull (1998). The Overspending and Flypaper Effects of Fiscal Illusion: Theory and Empirical Evidence. Journal of Urban]
#par(justify: true)[Economics. DOI: 10.1006/juec.1997.2056]
#par(justify: true)[\[19\] Wallace E. Oates (1999). An Essay on Fiscal Federalism. Journal of Economic Literature. DOI: 10.1257/jel.37.3.1120]
#par(justify: true)[\[20\] Andrew C. Worthington, Brian E. Dollery (1999). Fiscal illusion and the Australian local government grants process: How sticky is the]
#par(justify: true)[flypaper effect?. Public Choice. DOI: 10.1023/a:1018329802757]
#par(justify: true)[\[21\] Peter M. Mitias, Geoffrey K. Turnbull (2001). Grant Illusion, Tax Illusion, and Local Government Spending. Public Finance Review.]
#par(justify: true)[DOI: 10.1177/109114210102900501]
#par(justify: true)[\[22\] Christian Baretti, Bernd Huber e Karl Lichtblau (2002). A Tax on Tax Revenue: The Incentive Effects of Equalizing Transfers: Evidence]
#par(justify: true)[from Germany. International Tax and Public Finance. DOI: 10.1023/a:1020925812428]
#par(justify: true)[\[23\] Jonathan Rodden (2002). The Dilemma of Fiscal Federalism: Grants and Fiscal Performance around the World. American Journal of Political]
#par(justify: true)[Science. DOI: 10.2307/3088407]
#par(justify: true)[\[24\] Per Tovmo, Torberg Falch (2002). The flypaper effect and political strength. Economics of Governance. DOI: 10.1007/s101010100036]
#par(justify: true)[\[25\] R. S. Eckaus (2003). Some consequences of fiscal reliance on extrabudgetary revenues in China. China Economic Review. DOI: 10.1016/]
#par(justify: true)[s1043-951x(03)00002-6]
#par(justify: true)[\[26\] Jean-Paul Faguet (2004). Does decentralization increase government responsiveness to local needs? Evidence from Bolivia. Journal of]
#par(justify: true)[Public Economics. DOI: 10.1016/s0047-2727(02)00185-8]
#par(justify: true)[\[27\] Ritva Reinikka, Jakob Svensson (2004). Local Capture: Evidence from a Central Government Transfer Program in Uganda. The Quarterly]
#par(justify: true)[Journal of Economics. DOI: 10.1162/0033553041382120]
#par(justify: true)[\[28\] Kai-yuen Tsui (2005). Local tax system, intergovernmental transfers and China's local fiscal disparities. Journal of Comparative Economics.]
#par(justify: true)[DOI: 10.1016/j.jce.2004.11.003]
#par(justify: true)[\[29\] Hehui Jin, Yingyi Qian, Barry R. Weingast (2005). Regional decentralization and fiscal incentives: Federalism, Chinese style. Journal of]
#par(justify: true)[Public Economics. DOI: 10.1016/j.jpubeco.2004.11.008]
#par(justify: true)[\[30\] Xiaobo Zhang (2006). Fiscal decentralization and political centralization in China: Implications for growth and inequality. Journal of]
#par(justify: true)[Comparative Economics. DOI: 10.1016/j.jce.2006.08.006]
#par(justify: true)[\[31\] Thiess Buettner (2006). The incentive effect of fiscal equalization transfers on tax policy. Journal of Public Economics. DOI: 10.1016/]
#par(justify: true)[j.jpubeco.2005.09.004]
#par(justify: true)[\[32\] Hammed Amusa, Robert Mabunda, Ramos Mabugu (2008). Fiscal Illusion at the Local Sphere: An Empirical Test of the Flypaper Effect]
#par(justify: true)[Using South African Municipal Data. South African Journal of Economics. DOI: 10.1111/j.1813-6982.2008.00205.x]
#par(justify: true)[\[33\] Craig S. Maher, Terri Johnson (2008). Testing for Fiscal Illusion in Wisconsin Towns. International Journal of Public Administration.]
#par(justify: true)[DOI: 10.1080/01900690701501048]
#par(justify: true)[\[34\] Matz Dahlberg, Eva Mörk, Jørn Rattsø, Hanna Ågren (2008). Using a discontinuous grant rule to identify the effect of grants on local]
#par(justify: true)[taxes and spending. Journal of Public Economics. DOI: 10.1016/j.jpubeco.2007.05.004]
#par(justify: true)[\[35\] Wiji Arulampalam, Sugato Dasgupta, Amrita Dhillon, Bhaskar Dutta (2009). Electoral goals and center-state transfers: A theoretical]
#par(justify: true)[model and empirical evidence from India. Journal of Development Economics. DOI: 10.1016/j.jdeveco.2008.01.001]
#par(justify: true)[\[36\] Enlinson Mattos, Fabiana Rocha, Paulo Arvate (2011). Flypaper effect revisited: evidence for tax collection efficiency in Brazilian]
#par(justify: true)[municipalities. Estudos Econômicos (São Paulo). DOI: 10.1590/s0101-41612011000200002]
#par(justify: true)[\[37\] Yongzheng Liu, Jianmei Zhao (2011). Intergovernmental fiscal transfers and local tax efforts: evidence from provinces in China. Journal]
#par(justify: true)[of Economic Policy Reform. DOI: 10.1080/17487870.2011.591175]
#par(justify: true)[\[38\] Bihong Huang e Kang Chen (2012). Are intergovernmental transfers in China equalizing?. China Economic Review. DOI: 10.1016/]
#par(justify: true)[j.chieco.2012.01.001]
#par(justify: true)[\[39\] Tewodaj Mogues, Samuel Benin (2012). Do External Grants to District Governments Discourage Own Revenue Generation? A Look at]
#par(justify: true)[Local Public Finance Dynamics in Ghana. World Development. DOI: 10.1016/j.worlddev.2011.12.001]
#par(justify: true)[\[40\] Meili Niu (2013). Fiscal Decentralization in China Revisited (中国财政分权政策再探). Australian Journal of Public Administration. DOI:]
#par(justify: true)[10.1111/1467-8500.12026]
#v(4pt)
#par(justify: true)[\[41\] Stefan Brehm (2013). Fiscal Incentives, Public Spending, and Productivity – County-Level Evidence from a Chinese Province. World]
#par(justify: true)[Development. DOI: 10.1016/j.worlddev.2013.01.029]
#par(justify: true)[\[42\] Jing Vivian Zhan (2013). Strategy for Fiscal Survival? Analysis of local extra-budgetary finance in China. Journal of Contemporary China.]
#par(justify: true)[DOI: 10.1080/10670564.2012.734077]
#par(justify: true)[\[43\] Stephan Litschig, Kevin M. Morrison (2013). The Impact of Intergovernmental Transfers on Education Outcomes and Poverty Reduction.]
#par(justify: true)[American Economic Journal: Applied Economics. DOI: 10.1257/app.5.4.206]
#par(justify: true)[\[44\] Guang Zhang (2013). The Impacts of Intergovernmental Transfers on Local Governments’ Fiscal Behavior in China: A Cross-County]
#par(justify: true)[Analysis. Australian Journal of Public Administration. DOI: 10.1111/1467-8500.12027]
#par(justify: true)[\[45\] Junxue Jia, Qingwang Guo e Jing Zhang (2014). Fiscal decentralization and local expenditure policy in China. China Economic Review.]
#par(justify: true)[DOI: 10.1016/j.chieco.2014.01.002]
#par(justify: true)[\[46\] Chengri Ding, Yi Niu e Erik Lichtenberg (2014). Spending preferences of local officials with off-budget land revenues of Chinese cities.]
#par(justify: true)[China Economic Review. DOI: 10.1016/j.chieco.2014.10.001]
#par(justify: true)[\[47\] Emilie Caldeira, Grégoire Rota-Graziosi (2014). The Crowding-in Effect of Simple Unconditional Central Grants on Local Own-Source]
#par(justify: true)[Revenue: The Case of Benin. Journal of African Economies. DOI: 10.1093/jae/eju003]
#par(justify: true)[\[48\] Kaddour Mehiriz, Richard Marceau (2014). The Flypaper and Asymmetric Effects of Intergovernmental Grants to Quebec Municipalities.]
#par(justify: true)[Public Budgeting & Finance. DOI: 10.1111/pbaf.12026]
#par(justify: true)[\[49\] Heléne Lundqvist (2015). Granting public or private consumption? Effects of grants on local public spending and income taxes. Interna-]
#par(justify: true)[tional Tax and Public Finance. DOI: 10.1007/s10797-013-9279-7]
#par(justify: true)[\[50\] Emanuele Bracco, Ben Lockwood, Francesco Porcelli, Michela Redoano (2015). Intergovernmental grants as signals and the alignment]
#par(justify: true)[effect: Theory and evidence. Journal of Public Economics. DOI: 10.1016/j.jpubeco.2014.11.007]
#par(justify: true)[\[51\] Xiaobo Lü (2015). Intergovernmental transfers and local education provision — Evaluating China's 8-7 National Plan for Poverty Reduction.]
#par(justify: true)[China Economic Review. DOI: 10.1016/j.chieco.2015.02.001]
#par(justify: true)[\[52\] Rodolfo Ferreira Ribeiro Costa, Luiz Ivan de Melo Castelar (2015). O impacto das transferências constitucionais sobre os gastos dos]
#par(justify: true)[municípios brasileiros. Análise Econômica. DOI: 10.22456/2176-5456.51004]
#par(justify: true)[\[53\] Marie Kjaergaard (2015). The Flypaper Effect: Do Political Institutions Affect Danish Local Governments’ Response to Intergovernmental]
#par(justify: true)[Grants?. Local Government Studies. DOI: 10.1080/03003930.2014.968708]
#par(justify: true)[\[54\] Maarten A. Allers, Wouter Vermeulen (2016). Capitalization of equalizing grants and the flypaper effect. Regional Science and Urban]
#par(justify: true)[Economics. DOI: 10.1016/j.regsciurbeco.2016.03.005]
#par(justify: true)[\[55\] Jevuks Matheus Araujo, Rozane Bezerra Siqueira (2016). Demanda por gastos públicos locais: evidências dos efeitos de ilusão fiscal no]
#par(justify: true)[Brasil. Estudos Econômicos (São Paulo). DOI: 10.1590/0101-416146116jar]
#par(justify: true)[\[56\] Martin Baekgaard, Marie Kjaergaard (2016). Intergovernmental Grants and Public Expenditures: Evidence from a Survey Experiment.]
#par(justify: true)[Local Government Studies. DOI: 10.1080/03003930.2015.1110521]
#par(justify: true)[\[57\] Lucie Gadenne (2017). Tax Me, but Spend Wisely? Sources of Public Finance and Government Accountability. American Economic Journal:]
#par(justify: true)[Applied Economics. DOI: 10.1257/app.20150509]
#par(justify: true)[\[58\] Krisztina Kis-Katos, Bambang Suharnoko Sjahrir (2017). The impact of fiscal and political decentralization on local public investment in]
#par(justify: true)[Indonesia. Journal of Comparative Economics. DOI: 10.1016/j.jce.2017.03.003]
#par(justify: true)[\[59\] Ergete Ferede (2017). The Incentive Effects of Equalization Grants on Tax Policy: Evidence from Canadian Provinces. Public Finance]
#par(justify: true)[Review. DOI: 10.1177/1091142116666316]
#par(justify: true)[\[60\] Agnese Sacchi, Simone Salotti (2017). The influence of decentralized taxes and intergovernmental grants on local spending volatility.]
#par(justify: true)[Regional Studies. DOI: 10.1080/00343404.2015.1111512]
#par(justify: true)[\[61\] Yongqiu Wu, Yi Huang, Jing Zhao, Yanping Pu (2017). Transfer payment structure and local government fiscal efficiency: evidence from]
#par(justify: true)[China. China Finance and Economic Review. DOI: 10.1186/s40589-017-0058-y]
#par(justify: true)[\[62\] Herbert Dawid, Peter Harting, Michael Neugart (2018). Fiscal transfers and regional economic growth. Review of International Economics.]
#par(justify: true)[DOI: 10.1111/roie.12317]
#par(justify: true)[\[63\] Bin Huang, Yunxia Dong, Jingjing Miao, Caiqun Xu (2018). Intergovernmental Fiscal Transfers and County-Level Education Expenditure]
#par(justify: true)[in China. ECNU Review of Education. DOI: 10.30926/ecnuroe2018010306]
#par(justify: true)[\[64\] Takaaki Masaki (2018). The impact of intergovernmental transfers on local revenue generation in Sub-Saharan Africa: Evidence from]
#par(justify: true)[Tanzania. World Development. DOI: 10.1016/j.worlddev.2018.01.026]
#par(justify: true)[\[65\] Eric Rougier, François Combarnous, Yves-André Fauré (2018). The “Local Economy” Effect of Social Transfers: An Empirical Assessment]
#par(justify: true)[of the Impact of the Bolsa Família Program on Local Productive Structure and Economic Growth. World Development. DOI: 10.1016/ j.worlddev.2017.09.019]
#par(justify: true)[\[66\] Lucas Oliveira Gomes Ferreira, André Luiz Marques Serrano, Federico Revelli (2019). Effects of federal constitutional grants in Brazilian]
#par(justify: true)[municipalities. Review of Urban & Regional Development Studies. DOI: 10.1111/rurd.12103]
#par(justify: true)[\[67\] Raphael Corbi, Elias Papaioannou, Paolo Surico (2019). Regional Transfer Multipliers. The Review of Economic Studies. DOI: 10.1093/]
#par(justify: true)[restud/rdy069]
#par(justify: true)[\[68\] Tristan Canare (2019). THE EFFECT OF REVENUE SHARES ON LOCAL GOVERNMENT SPENDING: EVIDENCE FROM PHILIPPINE]
#par(justify: true)[PROVINCES. The Singapore Economic Review. DOI: 10.1142/s0217590819500206]
#par(justify: true)[\[69\] Daniel Azevedo Pansani, André Luiz Marques Serrano, Lucas Oliveira Gomes Ferreira (2020). Análise de Evidências e Causas do Efeito]
#par(justify: true)[Flypaper e da Ilusão Fiscal nos Estados e Municípios Brasileiros. Administração Pública e Gestão Social. DOI: 10.21118/apgs.v12i3.8169]
#par(justify: true)[\[70\] Takeshi Miyazaki (2020). Intergovernmental fiscal transfers and tax efforts: Regression-discontinuity analysis for Japanese local govern-]
#par(justify: true)[ments. Regional Science and Urban Economics. DOI: 10.1016/j.regsciurbeco.2020.103554]
#par(justify: true)[\[71\] Tassia Cruz, Talita Silva (2020). Minimum Spending in Education and the Flypaper Effect. Economics of Education Review. DOI: 10.1016/]
#par(justify: true)[j.econedurev.2020.102012]
#par(justify: true)[\[72\] Thiess Buettner e Manuela Krause (2021). Fiscal equalization as a driver of tax increases: empirical evidence from Germany. International]
#par(justify: true)[Tax and Public Finance. DOI: 10.1007/s10797-020-09610-9]
#par(justify: true)[\[73\] Marcel Henkel, Tobias Seidel, Jens Suedekum (2021). Fiscal Transfers in the Spatial Economy. American Economic Journal: Economic]
#par(justify: true)[Policy. DOI: 10.1257/pol.20180294]
#par(justify: true)[\[74\] Marcelo Castro, Enlinson Mattos (2021). Measuring Fiscal Spillovers in Brazilian Municipalities. Public Finance Review. DOI:]
#par(justify: true)[10.1177/1091142121993522]
#par(justify: true)[\[75\] Joseph Gyourko, Yang Shen, Jing Wu e Rongjie Zhang (2022). Land finance in China: Analysis and review. China Economic Review. DOI:]
#par(justify: true)[10.1016/j.chieco.2022.101868]
#v(4pt)
#par(justify: true)[\[76\] Irineu de Carvalho Filho, Stephan Litschig (2022). Long-Run Impacts of Intergovernmental Transfers. Journal of Human Resources. DOI:]
#par(justify: true)[10.3368/jhr.57.3.0917-9064r2]
#par(justify: true)[\[77\] Rose Camille Vincent, Victor Osei Kwadwo (2022). Spatial interdependence and spillovers of fiscal grants in Benin: Static and dynamic]
#par(justify: true)[diffusions. World Development. DOI: 10.1016/j.worlddev.2022.106006]
#par(justify: true)[\[78\] Estela Oliveira da Luz, Silvania Neris Nossa, Danilo Soares Monte-mor, João Eudes Bezerra Filho (2022). Transferências Voluntárias e o]
#par(justify: true)[Efeito Flypaper. Administração Pública e Gestão Social. DOI: 10.21118/apgs.v14i3.12321]
#par(justify: true)[\[79\] Vicente Rios, Miriam Hortas-Rico, Pedro Pascual (2022). What shapes the flypaper effect? The role of the political environment in the]
#par(justify: true)[budget process. Local Government Studies. DOI: 10.1080/03003930.2020.1866555]
#par(justify: true)[\[80\] Yidan Liu, Juann H. Hung (2023). China’s 1994 fiscal reform and local governments’ efforts on fighting industrial pollution. International]
#par(justify: true)[Public Management Journal. DOI: 10.1080/10967494.2023.2174224]
#par(justify: true)[\[81\] Yan Yan e Andrew Reschovsky (2023). Fiscal disparities among local governments in Zhejiang Province, China. Journal of Urban Affairs.]
#par(justify: true)[DOI: 10.1080/07352166.2020.1851138]
#par(justify: true)[\[82\] Joseph B. Ajefu, Joseph O. Ogebe (2023). Impact of Intergovernmental Transfers on Household Multidimensional Well-Being. The Journal]
#par(justify: true)[of Development Studies. DOI: 10.1080/00220388.2022.2139604]
#par(justify: true)[\[83\] Ron Shani, Yaniv Reingewertz e Eran Vigoda-Gadot (2023). Intergovernmental grants and local public finance: An empirical examination]
#par(justify: true)[in Israel. European Journal of Political Economy. DOI: 10.1016/j.ejpoleco.2023.102420]
#par(justify: true)[\[84\] Saulo Silva Lima Filho, Sara Silva Lima Dal-Comuni, Fernanda Ferro Lima (2023). O Efeito Flypaper e a Preguiça Fiscal: Uma Análise da]
#par(justify: true)[Eficiência de Arrecadação Municipal em Relação às Transferências Voluntárias Recebidas. Revista Contabilidade, Gestão e Governança. DOI: 10.51341/cgg.v26i1.3018]
#par(justify: true)[\[85\] Thai V Le e Matthew M Young (2023). Regressive revenue sourcing by local governments. Urban Studies. DOI: 10.1177/00420980221124456]
#par(justify: true)[\[86\] Cheng-Tao Tang, Chun Yee Wong, Orelie Bathan Delas Alas (2024). Effect of intergovernmental transfers on income and poverty rates:]
#par(justify: true)[Evidence from the Philippines. World Development. DOI: 10.1016/j.worlddev.2023.106420]
#par(justify: true)[\[87\] Xiao Tan, Ying Tan (2024). Equalization through the People’s Republic of China’s Intergovernmental Fiscal System: The Effectiveness of]
#par(justify: true)[Central and Provincial Transfers. Asian Development Review. DOI: 10.1142/s011611052450001x]
#par(justify: true)[\[88\] Piotr Danisewicz, Steven Ongena (2024). Fiscal transfers, local government, and entrepreneurship. Journal of Policy Analysis and]
#par(justify: true)[Management. DOI: 10.1002/pam.22532]
#par(justify: true)[\[89\] Manuel E. Lago, Santiago Lago-Peñas e Jorge Martinez-Vazquez (2024). On the effects of intergovernmental grants: a survey. International]
#par(justify: true)[Tax and Public Finance. DOI: 10.1007/s10797-023-09816-7]
#par(justify: true)[\[90\] Pedro Jorge Holanda Figueiredo Alves, Jevuks Matheus Araujo (2024). The effects of intergovernmental transfers on the local fiscal]
#par(justify: true)[incentives of Brazilian municipalities. Journal of Government and Economics. DOI: 10.1016/j.jge.2024.100104]
#par(justify: true)[\[91\] Yuchen Guo e Pinghan Liang (2025). Budget rollover and year-end spending in China: evidence from public procurement contracts. China]
#par(justify: true)[Economic Review. DOI: 10.1016/j.chieco.2025.102522]
#par(justify: true)[\[92\] Feng Liu, Yangmu Hu (2025). Can fiscal transfers achieve both equity and efficiency: Evidence from Chinese counties. International]
#par(justify: true)[Review of Economics & Finance. DOI: 10.1016/j.iref.2025.104586]
#par(justify: true)[\[93\] Christopher Dick-Sagoe, Ernest Ngeh Tingum, Peter Asare-Nuamah, Denis N. Yuni, Nicholas Baidoo (2025). Central transfers and]
#par(justify: true)[incentives to collect local revenue among the Central Region of Ghana’s local government officials: analysing the flypaper effect. Humanities and Social Sciences Communications. DOI: 10.1057/s41599-025-05463-x]
#par(justify: true)[\[94\] Xunhua Tu, Jie Yan, Yueyi Wang, Jing Zheng (2025). Fiscal transfers and public health services in China: a macro–micro analysis.]
#par(justify: true)[Frontiers in Public Health. DOI: 10.3389/fpubh.2025.1577963]
#par(justify: true)[\[95\] Luis Alberto da Costa, Napiê Galvê Araújo Silva, Vilmar Antonio Gonçalves Tondolo, Lauro Nogueira (2025). Socioeconomic]
#par(justify: true)[indicators and municipal revenues: Explanatory factors of the fiscal capacity of Brazilian municipalities. Revista de Administração Pública. DOI: 10.1590/0034-761220240085x]
#par(justify: true)[\[96\] Luan Vinicius Bernardelli, Pietro André Telatin Paschoalino, Letícia Xander Russo, Michael Alexander Kortt (2026). Intergovernmental]
#par(justify: true)[transfers and fiscal performance: evidence from Brazil. Local Government Studies. DOI: 10.1080/03003930.2026.2655683]
#par(justify: true)[\[97\] Leonardo Sánchez-Aragón, Gonzalo E. Sánchez, Wladimir Zanoni (2026). Stimulating local economies through central transfers: A natural]
#par(justify: true)[experiment from Ecuador. Journal of Development Economics. DOI: 10.1016/j.jdeveco.2025.103664]
#par(justify: true)[\[98\] Baker, A. C., Larcker, D. F., & Wang, C. C. Y. (2022). How much should we trust staggered difference-in-differences estimates? Journal of]
#par(justify: true)[Financial Economics, 144(2), 370–395. DOI: 10.1016/j.jfineco.2022.01.004]
#par(justify: true)[\[99\] Ferreira, L. O. G. (2021). Constitutional tax transfer in Brazilian municipalities: the fiscal illusion and the flypaper effect. Tese de doutorado,]
#par(justify: true)[Universidade de Brasília. PDF da tese]
#par(justify: true)[\[100\] Secretaria do Tesouro Nacional. Siconfi — API de dados abertos, Declaração de Contas Anuais (DCA), anexos I-C e I-E. Acesso em 22]
#par(justify: true)[out. 2026. Documentação da API ; Endpoint DCA]
#par(justify: true)[\[101\] IBGE. SIDRA, tabela 6579, estimativas da população residente; relação populacional publicada ao TCU em 2023, baseada no Censo 2022;]
#par(justify: true)[tabela 5938, Produto Interno Bruto dos Municípios. Acesso em 22 out. 2026. Estimativas ; IBGE ao TCU 2023 ; PIB municipal]
#par(justify: true)[\[102\] Banco Central do Brasil. Sistema Gerenciador de Séries Temporais, IPCA, série 433. Acesso em 22 out. 2026. API SGS 433]
#par(justify: true)[\[103\] Ministry of Finance of the People’s Republic of China. Relatórios de execução do orçamento central e local, 2014–2025; endereços por]
#par(justify: true)[ano e observação em dados/fontes\_brutas/china\_financas\_mof\_2014\_2025.csv. Acesso em 22 out. 2026. Relatório 2025]
#par(justify: true)[\[104\] Ministry of Finance of the People’s Republic of China. Contas finais centrais de 2022, publicada em 4 jul. 2023. Prestação final 2022]
#par(justify: true)[\[105\] World Bank. World Development Indicators: PIB corrente, PIB per capita constante de 2015 (NY.GDP.PCAP.KD), população, CPI e câmbio]
#par(justify: true)[médio da China, consulta 2014–2025. Acesso em 22 out. 2026. API de PIB per capita constante ; API de PIB nominal]
#par(justify: true)[\[106\] National Bureau of Statistics of China. Statistical Communiqué of the People’s Republic of China on the 2025 National Economic and]
#par(justify: true)[Social Development. Publicado em 2026. Comunicado estatístico 2025]
#par(justify: true)[\[107\] Repositório de partida indicado pelo aluno. P1-Prova-Financas, matrícula 232037730. Repositório anterior]
#par(justify: true)[\[108\] Aria, M., & Cuccurullo, C. (2017). bibliometrix: An R-tool for comprehensive science mapping analysis. Journal of Informetrics, 11(4),]
#par(justify: true)[959–975. DOI: 10.1016/j.joi.2017.08.007]
#v(4pt)
