# 🔧 CORREÇÃO 3 - Railway Build Detection

## O Problema

```
⚠️ Script start.sh not found
❌ Railpack could not determine how to build the app
```

Railway não consegue detectar a linguagem/setup automaticamente.

## A Solução - Abordagem Manual no Dashboard

Esta é a melhor forma de resolver:

### Passos no Railway Dashboard:

1. **Abra seu projeto Emma**

2. **Clique em "Settings" → "Build"**

3. **Configure assim:**
   ```
   Build Command: pip install -r requirements.txt
   Start Command: python run.py
   ```

4. **Em "Variables" adicione:**
   ```
   RAILWAY_MODE=true
   GROQ_API_KEY_LLM=sua_chave
   DISCORD_BOT_TOKEN=seu_token
   NVIDIA_API_KEY=sua_chave
   ```

5. **Clique em "Deploy"** ou "Redeploy"

### Alternativa: CLI do Railway

```bash
# 1. Instalar Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Link ao projeto
railway link

# 4. Deploy
railway up

# 5. Ver logs
railway logs
```

## 📁 Arquivos Criados para Suporte

- `Procfile` - Configuração tradicional
- `start.sh` - Script de início
- `railway.yaml` - Config Railway
- `heroku.yml` - Config Heroku (alternativa)

O Railway vai tentar usar esses arquivos para determinar como fazer build.

## 🎯 Próximas Ações

**Opção A (Dashboard):**
1. Abra Railway Dashboard
2. Vá em Configurações do projeto
3. Configure manualmente conforme acima
4. Clique "Redeploy"

**Opção B (CLI):**
1. Execute `railway login`
2. Execute `railway link`
3. Execute `railway up`

## ✅ Deve Funcionar Depois

Com a configuração manual no Dashboard, Railway saberá exatamente o que fazer e fará build sem erros.

---

**A configuração manual é mais confiável que auto-detection!** 🎉
