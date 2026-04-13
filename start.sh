#!/bin/bash
# Script de inicialização para Railway
set -e

echo "🚀 Iniciando Emma em Railway..."
export RAILWAY_MODE=true

# Executar a aplicação
python run.py
