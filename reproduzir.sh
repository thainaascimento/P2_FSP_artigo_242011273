#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export R_LIBS_USER="${R_LIBS_USER:-$HOME/R/library}"
mkdir -p "$R_LIBS_USER"

python3 codigo/01_coleta_siconfi.py
python3 codigo/02_transformacao_analise.py
python3 codigo/03_extensao_fiscal_2016_2025.py
FINANCAS_USE_ARCHIVED_CORPUS=1 python3 codigo/04_preparar_corpus_bibliometrix.py
Rscript codigo/05_bibliometria.R
python3 codigo/06_resultados_artigo.py
python3 codigo/07_preparar_citacoes_e_bibliometria.py
typst compile artigo/main.typ artigo/main.pdf

echo "Reprodução concluída: artigo/main.pdf"
