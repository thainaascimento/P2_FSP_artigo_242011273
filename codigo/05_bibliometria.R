#!/usr/bin/env Rscript
# Bibliometria descritiva com bibliometrix 5.5.0.
# Entrada: CSV do corpus com DOI e títulos compatíveis com Crossref.
# Países = contexto empírico codificado a partir do resumo/relevância; não país de afiliação dos autores.
# Palavras-chave = vocabulário temático harmonizado para este estudo; não keywords originais dos artigos.

suppressPackageStartupMessages(library(bibliometrix))
args_all <- commandArgs(trailingOnly = FALSE)
script_arg <- sub("^--file=", "", args_all[grep("^--file=", args_all)][1])
script_dir <- dirname(normalizePath(script_arg))
root <- normalizePath(file.path(script_dir, ".."))
in_file <- file.path(root, "artigo", "literatura", "artigos_verificados_doi.csv")
out_dir <- file.path(root, "artigo", "literatura", "bibliometria")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

D <- read.csv(in_file, fileEncoding = "UTF-8-BOM", stringsAsFactors = FALSE, check.names = FALSE)
stopifnot(nrow(D) >= 80, all(nzchar(D$doi)), all(nzchar(D$title)))
review_file <- file.path(root, "artigo", "literatura", "dois_para_revisao_manual.csv")
review_n <- if (file.exists(review_file)) nrow(read.csv(review_file, fileEncoding = "UTF-8-BOM", stringsAsFactors = FALSE)) else 0L

country_patterns <- c(
  "Brazil"="Brasil|Brazil|Brazilian|Brazil's",
  "China"="China|Chinese|PRC|Zhejiang",
  "United States"="United States|U\\.S\\.|USA|American states|Virginia|Michigan|Wisconsin|California|federal highway",
  "Sweden"="Sweden|Swedish",
  "Germany"="Germany|German|Germany's",
  "Canada"="Canada|Canadian|Quebec|Québec",
  "Finland"="Finland|Finnish",
  "Australia"="Australia|Australian",
  "Italy"="Italy|Italian",
  "Spain"="Spain|Spanish",
  "Israel"="Israel|Israeli",
  "Japan"="Japan|Japanese",
  "Bolivia"="Bolivia|Bolivian",
  "Tanzania"="Tanzania|Tanzanian",
  "South Africa"="South Africa|South African",
  "Philippines"="Philippines|Filipino",
  "Indonesia"="Indonesia|Indonesian",
  "Denmark"="Denmark|Danish",
  "Ecuador"="Ecuador|Ecuadorian",
  "India"="India|Indian",
  "Europe/multiple"="European regions|Europe|cross-country|international comparative"
)
code_country <- function(x) {
  # Prefer explicit study locations in relevance/finding/title over general topic terms.
  s <- paste(x, collapse = " ")
  hits <- names(country_patterns)[vapply(country_patterns, function(p) grepl(p, s, ignore.case = TRUE, perl = TRUE), logical(1))]
  if (length(hits) == 0) "Não especificado" else paste(hits, collapse = "; ")
}

make_keywords <- function(x) {
  s <- tolower(paste(x, collapse = " "))
  k <- character()
  if (grepl("flypaper", s)) k <- c(k, "efeito flypaper")
  if (grepl("fiscal illusion|ilusão fiscal|illusion", s)) k <- c(k, "ilusão fiscal")
  if (grepl("transfer|grant|repasse|transferência", s)) k <- c(k, "transferências intergovernamentais")
  if (grepl("tax effort|tax collection|arrecada|own.source|tribut|tax policy|receita própria", s)) k <- c(k, "receita própria e esforço fiscal")
  if (grepl("spend|expenditure|gasto|despesa|budget|orçament", s)) k <- c(k, "despesa pública local")
  if (grepl("equaliz|equaliza|disparit|desigualdade fiscal", s)) k <- c(k, "equalização fiscal")
  if (grepl("decentral|descentral|federalism|federalismo", s)) k <- c(k, "federalismo e descentralização fiscal")
  if (grepl("growth|crescimento|income|renda|poverty|pobreza|employment|emprego", s)) k <- c(k, "atividade econômica e desenvolvimento")
  if (grepl("instrument|regression.discontinuity|discontinuity|causal|endogeneity|identification|identificação|endogeneidade", s)) k <- c(k, "identificação e métodos causais")
  ctry <- code_country(x)
  if (grepl("Brazil|Brasil", ctry)) k <- c(k, "Brasil")
  if (grepl("China", ctry)) k <- c(k, "China")
  unique(k)
}

context_text <- paste(D$title, D$relevance, D$finding, sep = " ")
D$study_country <- vapply(context_text, code_country, character(1))
D$harmonized_keywords <- vapply(context_text, function(s) paste(make_keywords(s), collapse = ";"), character(1))
D$AU <- D$authors
D$PY <- as.integer(D$year)
D$SO <- D$journal
D$TI <- D$title
D$DI <- D$doi
D$DE <- D$harmonized_keywords
D$ID <- D$harmonized_keywords
M <- D[, c("AU", "PY", "SO", "TI", "DI", "DE", "ID")]
M$DB <- "wos"
M$JI <- M$SO
M$J9 <- M$SO

# Core bibliometrix analysis. The source has no cited-reference or author-affiliation
# records, so summary fields that require those inputs are intentionally not inferred.
BA <- bibliometrix::biblioAnalysis(M, sep = ";")
capture.output(str(BA), file = file.path(out_dir, "resumo_bibliometrix.txt"))

split_semicolon <- function(x) unlist(strsplit(x[!is.na(x) & nzchar(x)], ";\\s*", perl = TRUE), use.names = FALSE)
frequency_table <- function(x, label) {
  z <- sort(table(trimws(split_semicolon(x))), decreasing = TRUE)
  data.frame(item = names(z), count = as.integer(z), stringsAsFactors = FALSE)
}
annual <- as.data.frame(table(year = D$PY), stringsAsFactors = FALSE)
names(annual) <- c("year", "articles")
annual$year <- as.integer(as.character(annual$year)); annual$articles <- as.integer(annual$articles)
annual <- annual[order(annual$year), ]
journals <- head(frequency_table(D$SO, "journal"), 15)
authors <- head(frequency_table(D$AU, "author"), 15)
countries <- head(frequency_table(D$study_country, "country_setting"), 15)
keywords <- head(frequency_table(D$harmonized_keywords, "keyword"), 20)
write.csv(annual, file.path(out_dir, "producao_por_ano.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(journals, file.path(out_dir, "periodicos_mais_relevantes.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(authors, file.path(out_dir, "autores_mais_relevantes.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(countries, file.path(out_dir, "paises_contexto_estudo.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(keywords, file.path(out_dir, "palavras_chave_harmonizadas.csv"), row.names = FALSE, fileEncoding = "UTF-8")
write.csv(D, file.path(out_dir, "corpus_bibliometrix_com_campos.csv"), row.names = FALSE, fileEncoding = "UTF-8")

# Network of keyword co-occurrence, computed and visualized with bibliometrix.
M <- bibliometrix::metaTagExtraction(M, Field = "SR")
net <- bibliometrix::biblioNetwork(M, analysis = "co-occurrences", network = "keywords", sep = ";")
write.csv(as.matrix(net), file.path(out_dir, "matriz_coocorrencia_palavras_chave.csv"), fileEncoding = "UTF-8")
png(file.path(out_dir, "rede_coocorrencia_palavras_chave.png"), width = 1800, height = 1400, res = 180)
tryCatch(
  bibliometrix::networkPlot(net, normalize = "association", n = 20, Title = "Coocorrência de palavras-chave harmonizadas",
                            type = "fruchterman", label = TRUE, labelsize = 0.75, label.n = 20,
                            cluster = "walktrap", remove.isolates = TRUE, edges.min = 1, seed = 42, verbose = FALSE),
  error = function(e) { plot.new(); text(0.5, 0.5, paste("Falha ao renderizar a rede:", conditionMessage(e))) }
)
dev.off()

# Concise machine-readable indicators for article reporting.
metrics <- data.frame(
  indicator = c("registros_incluidos", "anos_cobertos", "periodicos_distintos", "autores_distintos", "contextos_nacionais_codificados", "doi_com_titulo_crossref_compativel"),
  value = c(nrow(D), paste(min(D$PY), max(D$PY), sep = "–"), length(unique(D$SO)), length(unique(trimws(split_semicolon(D$AU)))), length(unique(unlist(strsplit(D$study_country, "; ")))), nrow(D)),
  note = c(paste0("artigos com DOI e título compatível; ", review_n, " registros em revisão manual não foram usados"), "ano inicial e final de publicação", "conforme a fonte editorial normalizada", "contagem por nome em campo autor", "codificação do contexto empírico, não afiliação institucional", "Crossref status 200 e similaridade de título >= 0,72"),
  stringsAsFactors = FALSE
)
write.csv(metrics, file.path(out_dir, "indicadores_bibliometricos.csv"), row.names = FALSE, fileEncoding = "UTF-8")
writeLines(capture.output(sessionInfo()), file.path(out_dir, "sessionInfo.txt"), useBytes = TRUE)
cat("bibliometrix", as.character(packageVersion("bibliometrix")), "| N=", nrow(D), "| years=", min(D$PY), "-", max(D$PY), "| journals=", length(unique(D$SO)), "| authors=", length(unique(trimws(split_semicolon(D$AU)))), "\n")
