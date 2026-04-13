# 🚀 CHECKLIST DE DEPLOY NO RAILWAY

## Pré-Deploy ✓

- [ ] Verifique se o código foi testado localmente
- [ ] Confirme que `requirements.txt` está atualizado
- [ ] Verifique se `Procfile` existe
- [ ] Copie `DISCORD_BOT_TOKEN` de https://discord.com/developers
- [ ] Copie `GROQ_API_KEY_LLM` de https://console.groq.com
- [ ] Copie `GROQ_API_KEY_VISION` de https://console.groq.com
- [ ] Copie `NVIDIA_API_KEY` de https://api.nvidia.com

## No Railway ✓

1. **Nova Aplicação**
   - [ ] Clique em "New Project"
   - [ ] Escolha "GitHub Repo"
   - [ ] Conecte ao repositório Emma.IA.0.3

2. **Variáveis de Ambiente**
   - [ ] Clique em "Variables"
   - [ ] Configure as seguintes variáveis:
     ```
     RAILWAY_MODE=true
     GROQ_API_KEY_LLM=sua_chave
     GROQ_API_KEY_VISION=sua_chave
     DISCORD_BOT_TOKEN=seu_token
     NVIDIA_API_KEY=sua_chave
     OPENAI_API_KEY=sua_chave (se usar)
     ```

3. **Deploy**
   - [ ] Clique em "Deploy"
   - [ ] Aguarde 5-10 minutos
   - [ ] Verifique os logs

## Após Deploy ✓

### Verificar Status
```bash
# Se tiver Railway CLI instalado
railway logs
```

### Testes
1. [ ] Envie uma DM para o Discord Bot
2. [ ] Mencione o bot em um servidor
3. [ ] Verifique se recebe respostas
4. [ ] Teste funcionalidades: pesquisa, voz (se configurado), etc

### Problemas Comuns

| Erro | Solução |
|------|---------|
| Bot não responde | Verifique DISCORD_BOT_TOKEN no Railway |
| "GROQ_API_KEY não encontrada" | Redeploy após adicionar as variáveis |
| Memória cheia | Delete arquivos da pasta `Arcana/armazen` |

## Monitoramento Contínuo ✓

- [ ] Monitore uso de RAM/CPU no Railway Dashboard
- [ ] Revise logs regularmente
- [ ] Faça backup da pasta `Arcana/armazen` se necessário

## Rollback (Se Houver Problema)

```bash
# No Railway Dashboard:
# 1. Vá para a aba "Deployments"
# 2. Clique em um deployment anterior
# 3. Clique em "Redeploy"
```

---

## 🎉 Pronto para Production!

Após completar este checklist, sua Emma estará rodando 24/7 no Railway com:
✅ Discord Bot ativo
✅ IA Groq/NVIDIA funcional
✅ Personalidade intacta
✅ Memória persistida
