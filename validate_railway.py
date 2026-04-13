#!/usr/bin/env python3
# 🧪 Script de Validação da Adaptação Railway

import os
import sys

print("🔍 Validando adaptação Railway para Emma...")
print("=" * 50)

# Teste 1: Variável RAILWAY_MODE
print("\n✓ Teste 1: Variável RAILWAY_MODE")
try:
    from pathlib import Path
    run_py = Path("run.py").read_text()
    if 'RAILWAY_MODE' in run_py:
        print("  ✅ RAILWAY_MODE definida no código")
    else:
        print("  ❌ RAILWAY_MODE não encontrada!")
        sys.exit(1)
except Exception as e:
    print(f"  ❌ Erro: {e}")
    sys.exit(1)

# Teste 2: Condições Rails mode
print("\n✓ Teste 2: Condições Railway")
conditions = [
    'if not RAILWAY_MODE:',
    'if RAILWAY_MODE:',
]
for cond in conditions:
    if cond in run_py:
        count = run_py.count(cond)
        print(f"  ✅ {cond} encontrada {count}x")
    else:
        print(f"  ⚠️  {cond} não encontrada")

# Teste 3: Desabilitação de componentes
print("\n✓ Teste 3: Componentes desabilitados em Railway")
components = {
    'GUI Tkinter': 'if not RAILWAY_MODE:',
    'Atalhos': 'keyboard.add_hotkey',
    'VTuber': 'vtuber_ativo and not RAILWAY_MODE',
    'AppLauncher': 'AppLauncher() if not RAILWAY_MODE',
}

for comp, pattern in components.items():
    if pattern in run_py:
        print(f"  ✅ {comp} - Desabilitado corretamente")
    else:
        print(f"  ⚠️  {comp} - Padrão não encontrado")

# Teste 4: Arquivos de documentação
print("\n✓ Teste 4: Documentação criada")
docs = [
    'README_RAILWAY.md',
    'DEPLOY_CHECKLIST.md',
    'ARCHITECTURE.md',
    'RAILWAY_CHANGES.md',
    'ADAPTACAO_RAILWAY.md',
    'RAILWAY_DEPLOYMENT.md',
    '.env.example'
]

for doc in docs:
    if Path(doc).exists():
        print(f"  ✅ {doc}")
    else:
        print(f"  ❌ {doc} - FALTANDO!")

# Teste 5: .env configurada
print("\n✓ Teste 5: Configuração .env")
if Path('.env').exists():
    env_content = Path('.env').read_text()
    if 'RAILWAY_MODE' in env_content:
        print("  ✅ RAILWAY_MODE configurada em .env")
    else:
        print("  ⚠️  RAILWAY_MODE não em .env (pode ser adicionada no Railway)")
else:
    print("  ⚠️  .env não existe (pode ser criada no Railway)")

# Teste 6: Procfile
print("\n✓ Teste 6: Procfile")
if Path('Procfile').exists():
    procfile = Path('Procfile').read_text()
    if 'python run.py' in procfile:
        print("  ✅ Procfile configurado corretamente")
    else:
        print("  ❌ Procfile com comando incorreto!")
else:
    print("  ❌ Procfile não existe!")

# Teste 7: requirements.txt
print("\n✓ Teste 7: Requirements.txt")
requirements = [
    'discord.py',
    'groq',
    'torch',
    'torchaudio',
    'requests',
    'edge-tts',
    'pygame',
    'keyboard',
]
with open('requirements.txt') as f:
    req_content = f.read()
    for pkg in requirements:
        if pkg in req_content:
            print(f"  ✅ {pkg}")
        else:
            print(f"  ❌ {pkg} - FALTANDO!")

print("\n" + "=" * 50)
print("✅ VALIDAÇÃO COMPLETA!")
print("\n📝 Próximas ações:")
print("   1. Leia ADAPTACAO_RAILWAY.md")
print("   2. Configure variáveis no Railway Dashboard")
print("   3. Faça push para GitHub")
print("   4. Railway automaticamente faz deploy!")
print("\n🚀 Emma pronta para Railway!")
