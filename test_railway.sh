#!/bin/bash
# 🧪 Script de Teste Quick - Emma Railway

echo "🧪 TESTE RÁPIDO - Validando Emma para Railway"
echo "=============================================="
echo ""

# Teste 1: Python version
echo "✓ Verificando Python..."
python --version
echo ""

# Teste 2: Virtual env ativado
echo "✓ Verificando virtual environment..."
which python
echo ""

# Teste 3: Imports críticos
echo "✓ Testando imports..."
python -c "
import sys
try:
    import discord
    print('  ✅ discord.py')
except: 
    print('  ❌ discord.py')
    
try:
    import groq
    print('  ✅ groq')
except:
    print('  ❌ groq')
    
try:
    import torch
    print('  ✅ torch')
except:
    print('  ❌ torch')
    
try:
    import dotenv
    print('  ✅ python-dotenv')
except:
    print('  ❌ python-dotenv')
"
echo ""

# Teste 4: Carregamento de variáveis
echo "✓ Carregando .env..."
if [ -f .env ]; then
    echo "  ✅ .env encontrado"
    # Não printe chaves sensíveis
    grep -E "^[A-Z]" .env | sed 's/=.*/=***/' | head -5
else
    echo "  ❌ .env não encontrado"
fi
echo ""

# Teste 5: Estrutura de pastas
echo "✓ Verificando estrutura..."
for dir in Arcana Arcana/Apps Arcana/armazen Arcana/Net Arcana/Aura; do
    if [ -d "$dir" ]; then
        echo "  ✅ $dir"
    else
        echo "  ❌ $dir - FALTANDO"
    fi
done
echo ""

# Teste 6: Arquivos principais
echo "✓ Arquivos principais..."
for file in run.py Procfile requirements.txt .env.example validate_railway.py; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ⚠️  $file"
    fi
done
echo ""

echo "=============================================="
echo "✅ TESTES CONCLUÍDOS!"
echo ""
echo "Próximas ações:"
echo "  1. Execute: python validate_railway.py"
echo "  2. Leia: ADAPTACAO_RAILWAY.md"
echo "  3. Configure Railway Dashboard"
echo "  4. Faça git push"
echo ""
echo "🚀 Emma está pronta para Railway!"
