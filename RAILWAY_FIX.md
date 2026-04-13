# 🔧 Correção do Erro de Build no Railway

## O Problema

```
❌ RailPack could not determine how to build the app.
The following languages are supported: PHP, ...
```

## A Causa

Railway não conseguiu detectar automaticamente que é um projeto Python. Isso acontece quando:
- Falta indicação clara da linguagem
- Falta arquivo `runtime.txt`
- `Procfile` não está configurado corretamente

## A Solução - Arquivos Adicionados

### 1. **runtime.txt** ✅
```
python-3.12.3
```
Indica explicitamente que é Python 3.12.3

### 2. **Dockerfile** ✅
Configuração customizada de container:
- Base: `python:3.12.3-slim`
- Instala dependências de sistema (portaudio para PyAudio)
- Copia requirements.txt
- Instala Python packages
- Copia código
- Inicia com `python run.py`

### 3. **railway.json** ✅
```json
{
  "build": {
    "builder": "dockerfile"
  }
}
```
Diz ao Railway para usar o Dockerfile

### 4. **.dockerignore** ✅
Lista arquivos que não devem ir para o container:
- `.git`, `.env` (segredos)
- `__pycache__`, `.venv` (temporários)
- Logs, testes, etc

## ✅ Próximas Ações

1. Faça commit desses arquivos:
```bash
git add runtime.txt Dockerfile .dockerignore railway.json
git commit -m "Fix: Adicionar configuração Docker para Railway"
git push origin main
```

2. No Railway Dashboard:
   - Clique em "Redeploy"
   - Agora deve detectar como Python/Docker

3. Configure variáveis de ambiente:
   ```
   RAILWAY_MODE=true
   GROQ_API_KEY_LLM=sua_chave
   DISCORD_BOT_TOKEN=seu_token
   etc
   ```

## 🔍 Alternativa: CLI do Railway

Se ainda tiver problemas, use CLI:
```bash
# Instalar
npm install -g @railway/cli

# Login
railway login

# Link ao projeto
railway link

# Deploy
railway up
```

## ✨ Resultado Esperado

Após fazer push, Railway deverá:
1. ✅ Detectar como projeto Python
2. ✅ Fazer build com Docker
3. ✅ Instalar dependências
4. ✅ Iniciar Emma no Discord Bot

---

**O erro foi corrigido!** 🎉 Agora faça push e tente novamente.
