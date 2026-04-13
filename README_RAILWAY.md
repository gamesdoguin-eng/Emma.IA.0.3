# 🚀 Deploy da Emma no Railway

## Pré-requisitos

1. **Conta no Railway** - [railway.app](https://railway.app)
2. **GitHub** - Seu repositório com o código
3. **Chaves de API**:
   - GROQ_API_KEY_LLM (obtenha em [console.groq.com](https://console.groq.com))
   - GROQ_API_KEY_VISION
   - DISCORD_BOT_TOKEN (obtenha em [discord.com/developers](https://discord.com/developers))
   - NVIDIA_API_KEY (obtenha em [api.nvidia.com](https://api.nvidia.com))

## Passos para Deploy

### 1. Preparar o Repositório
```bash
# Certifique-se de que seu repositório tem:
# - Procfile (já existe)
# - requirements.txt (já existe)
# - .env.example (já existe)
```

### 2. Fazer Push para GitHub
```bash
git add .
git commit -m "Preparando para deploy no Railway"
git push origin main
```

### 3. Conectar Railway ao GitHub
1. Acesse [railway.app](https://railway.app)
2. Clique em "New Project"
3. Selecione "GitHub Repo"
4. Conecte sua conta GitHub
5. Selecione o repositório `Emma.IA.0.3`

### 4. Configurar Variáveis de Ambiente
No painel do Railway, vá para **Variables** e configure:

```
RAILWAY_MODE=true
GROQ_API_KEY_LLM=sua_chave_aqui
GROQ_API_KEY_VISION=sua_chave_aqui
DISCORD_BOT_TOKEN=seu_token_aqui
NVIDIA_API_KEY=sua_chave_aqui
```

### 5. Deploy
Railway fará deploy automaticamente quando você fazer push no GitHub.

## Monitorar

No Dashboard do Railway você pode:
- Ver logs em tempo real
- Monitorar consumo de recursos
- Redeploy na necessidade

## Logs

Para ver logs em tempo real:
```bash
railway logs
```

## O que Funciona em Railway

✅ **Discord Bot** - Totalmente funcional
✅ **IA Groq/NVIDIA** - Todas as capacidades mantidas
✅ **Personalidade da Emma** - Intacta 100%
✅ **Pesquisa DDG** - Funcional
✅ **Brain/Memória** - Persistida em arquivos JSON

## O que NÃO Funciona em Railway

❌ **GUI Tkinter** - Desativada (sem display)
❌ **Atalhos de Teclado** - Desativados (não há teclado)
❌ **Modo Voz/Áudio** - Desativado (sem microfone)
❌ **Click-to-Talk** - Desativado
❌ **VTuber Overlay** - Desativado
❌ **App Launcher** - Desativado (não há sistema de apps)

## Modo de Uso

Em Railway, a Emma funciona **apenas via Discord Bot**:

1. Envie DMs para o bot
2. Ou mencione o bot em servidores: `@Emma sua_pergunta`
3. O bot responderá usando as mesmas capacidades de IA

## Troubleshooting

### "GROQ_API_KEY_LLM não configurada"
- Verifique se configurou as variáveis no Railway Dashboard
- Clique em "Deploy" novamente após adicionar as variáveis

### Bot não responde
- Verifique o token do Discord está correto
- Verifique permissões do bot no servidor Discord
- Veja os logs: `railway logs`

### Erro de memória
- Railway tem limite de RAM
- Limpe a pasta `Arcana/armazen` se ficar muito grande

## Recursos Railway

- **Plano Gratuito**: 5GB de storage, rodas durante 500 horas/mês
- **Plano Pro**: Mais recursos, $5/mês

---

**A IA e personalidade da Emma são 100% preservadas em Railway!** 🎭
