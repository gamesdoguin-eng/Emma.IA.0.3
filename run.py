# ============//======================//================
#region 📚 CHAMADAS E MODOS
# ======================================================
import asyncio
import json
from xmlrpc import client
import discord
from dotenv import load_dotenv
import re
import io
import wave
import torch
import numpy as np
# import pyaudio  # Removido - não funciona em Railway. Import condicional abaixo.
import requests
import edge_tts
import random
import pygame
import keyboard
import threading
import os
import base64
import tkinter as tk
import subprocess  # Adicionado
import sys         # Adicionado
from tkinter import ttk
from PIL import ImageGrab
from datetime import datetime
from groq import Groq
from openai import OpenAI  # Apenas para o LLM principal Kimi via NVIDIA
from dotenv import load_dotenv
#import tkinter as tk

# 🔥 IMPORTAÇÃO DA INTERFACE GRÁFICA ATUALIZADA
from Arcana.Apps.gui_handler import RemGUI

# 🔥 IMPORTAÇÃO DO SEU MÓDULO DE PESQUISA
import Arcana.Net.search_ddg as search_ddg

#from Arcana.Net.discord_Rem import run_discord_bot

# 🔥 IMPORTAÇÃO DO SEU MÓDULO DE AUTOMAÇÃO DE APPS
from Arcana.Aura.app_launcher import AppLauncher 

# Carrega as chaves do ficheiro .env
load_dotenv()
GROQ_API_KEY_LLM = os.getenv("GROQ_API_KEY_LLM")
GROQ_API_KEY_VISION = os.getenv("GROQ_API_KEY_VISION")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY") # Chave da NVIDIA
RAILWAY_MODE = os.getenv("RAILWAY_MODE", "False").lower() == "true" # Modo Railway (nuvem)

# 🔥 VALIDAÇÃO DE CHAVES ANTES DE INICIALIZAR
if not GROQ_API_KEY_LLM:
    print("\n❌ ERRO: GROQ_API_KEY_LLM não configurada no arquivo .env")
    print("   Adicione sua chave Groq ao arquivo .env e tente novamente.")
    sys.exit(1)

if RAILWAY_MODE:
    print("🚀 [RAILWAY MODE] Emma iniciando em ambiente de nuvem (Discord Bot apenas)")
else:
    try:
        import pyaudio  # Apenas em modo local
    except ImportError:
        pyaudio = None
        print("⚠️ PyAudio não instalado - modo voz desativado")

#endregion
# ======================================================
#region 🤖 CONFIGURAÇÃO DO BOT DE DISCORD (GROQ)
# ======================================================
intent = discord.Intents.default()
intent.message_content = True
intent.guilds = True
intent.messages = True

client = discord.Client(intents=intent)
groq = Groq(api_key=GROQ_API_KEY_LLM)

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    is_dm = isinstance(message.channel, discord.DMChannel)
    mentions_bot = client.user in message.mentions
    if not is_dm and not mentions_bot:
        return

    print(f"[Discord] mensagem recebida de {message.author}: {message.content}")
    print(f"[Discord] DM={is_dm}, mentions_bot={mentions_bot}, mentions={message.mentions}")

    user_msg = message.content
    if mentions_bot:
        user_msg = re.sub(rf'<@!?(?:{client.user.id})>', '', user_msg).strip()

    if not user_msg:
        return

    try:
        resposta = groq.chat.completions.create(
            messages=[{"role": "user", "content": user_msg}],
            model=os.getenv("GROQ_MODEL_DISCORD", "meta-llama/llama-4-scout-17b-16e-instruct")
        )
        reply = resposta.choices[0].message.content
        await message.reply(reply)
    except Exception as e:
        print(f"[Discord] erro ao responder: {e}")
        try:
            await message.reply("Desculpa, tive um problema ao processar sua mensagem. Tente de novo em alguns segundos.")
        except Exception:
            pass


def run_discord_bot():
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("Erro no bot do Discord: DISCORD_BOT_TOKEN não encontrado.")
        return
    try:
        client.run(token)
    except Exception as e:
        print(f"Erro no bot do Discord: {e}")
#endregion
# ======================================================
#region 🧠 VARIÁVEIS GLOBAIS E PAINEL
# ======================================================
# Cria a pasta automaticamente se ela não existir
os.makedirs("Arcana/armazen", exist_ok=True)

# 🔥 ARQUIVOS FIXOS
BRAIN_FILE = "Arcana/armazen/brain.json"
MEMORIA_FILE = "Arcana/armazen/memoria.json"
SEARCH_MEMORY_FILE = "Arcana/armazen/pesquisa_memoria.json" 

VISAO_HABILITADA = False # Controlo global do F2
CONTADOR_VISAO = 0       # Contador para limpar a memória visual

def abrir_gui_modelos():
    def salvar():
        if os.path.exists(BRAIN_FILE):
            with open(BRAIN_FILE, 'r', encoding='utf-8') as f: data = json.load(f)
            data["modelos_ativos"] = {"local": var_local.get(), "discord": var_discord.get()}
            with open(BRAIN_FILE, 'w', encoding='utf-8') as f: json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\n [SISTEMA] Cérebro atualizado! Local: {var_local.get().upper()} | Discord: {var_discord.get().upper()}")
        janela.destroy()

    janela = tk.Tk()
    janela.title("Painel de Controle IA - Rem")
    janela.geometry("400x320")
    janela.configure(bg="#1e1e2e")
    style = ttk.Style()
    style.configure("TLabel", background="#1e1e2e", foreground="#cdd6f4", font=("Segoe UI", 11))
    style.configure("TRadiobutton", background="#1e1e2e", foreground="#a6adc8", font=("Segoe UI", 10))

    ttk.Label(janela, text=" Cérebro Principal (Local):", font=("Segoe UI", 12, "bold"), foreground="#f38ba8").pack(pady=(15, 5))
    var_local = tk.StringVar()
    ttk.Radiobutton(janela, text="NVIDIA (Kimi 2.5)", variable=var_local, value="nvidia").pack()
    ttk.Radiobutton(janela, text="GROQ (Scout 17b)", variable=var_local, value="groq").pack()

    ttk.Label(janela, text=" Cérebro do Discord:", font=("Segoe UI", 12, "bold"), foreground="#a6e3a1").pack(pady=(20, 5))
    var_discord = tk.StringVar()
    ttk.Radiobutton(janela, text="NVIDIA (Kimi 2.5)", variable=var_discord, value="nvidia").pack()
    ttk.Radiobutton(janela, text="GROQ (Scout 17b)", variable=var_discord, value="groq").pack()

    try:
        with open(BRAIN_FILE, 'r', encoding='utf-8') as f:
            mod = json.load(f).get("modelos_ativos", {"local": "nvidia", "discord": "groq"})
            var_local.set(mod.get("local", "nvidia")); var_discord.set(mod.get("discord", "groq"))
    except: var_local.set("nvidia"); var_discord.set("groq")

    tk.Button(janela, text=" Salvar e Aplicar", command=salvar, bg="#89b4fa", fg="#1e1e2e", font=("Segoe UI", 10, "bold")).pack(pady=25)
    janela.attributes('-topmost', True)
    janela.mainloop()
#endregion
# ======================================================
#region 👁️ VISÃO COMPUTACIONAL E INJETORES
# ======================================================
def toggle_visao(e):
    global VISAO_HABILITADA
    VISAO_HABILITADA = not VISAO_HABILITADA
    play_beep("inicio" if VISAO_HABILITADA else "fim")
    print(f"\n[SISTEMA] 👁️ Permissão de Visão (F2): {'LIGADA' if VISAO_HABILITADA else 'DESLIGADA'}")

def toggle_gatilho(e):
    # 🔥 F3 GLOBAL RESOLVIDO: Não trava mais no microfone!
    if os.path.exists(BRAIN_FILE):
        try:
            with open(BRAIN_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            novo_estado = not data.get("trigger_active", False)
            data["trigger_active"] = novo_estado
            with open(BRAIN_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            play_beep("inicio" if novo_estado else "fim")
            print(f"\n[SISTEMA] 🎤 Gatilho de Voz (F3): {'LIGADO' if novo_estado else 'DESLIGADO'}")
        except Exception as ex:
            pass

def requer_visao(texto):
    texto_min = texto.lower()
    padrao_palavras = r"\b(olha|veja|tela|imagem|foto|analisa|analise|lê|leia|vendo)\b"
    frases_exatas = ["o que é isso", "o que e isso", "o que tem na tela"]
    if re.search(padrao_palavras, texto_min): return True
    if any(frase in texto_min for frase in frases_exatas): return True
    return False

def requer_despertar(texto, nome_ai):
    texto_min = texto.lower()
    padrao_gatilhos = rf"\b({nome_ai.lower()}|ei|acorda|ouve|escuta)\b"
    return bool(re.search(padrao_gatilhos, texto_min))

# 🔥 O SEU NOVO INJETOR CIRÚRGICO DE COMANDOS DE MÚSICA
def detectar_comando_musica(texto):
    t = texto.lower().strip()
    if re.search(r'\b(pausar|pausa|despausa|resume)\b', t): return "PAUSE"
    if re.search(r'\b(para a música|para tudo|stop|desliga a música|calar a boca)\b', t): return "STOP"
    if re.search(r'\b(pula|próxima|skip|pular|passa)\b', t): return "SKIP"
    
    padrao_tocar = r'\b(toca|tocar|coloca|colocar|põe|bota)\b.*?(música|músicas|som|playlist|rock|kpop|pop|lofi|clássica|jazz|rap|funk|metal|eletrônica|abertura|encerramento)'
    if re.search(padrao_tocar, t):
        query = re.sub(r'\b(toca|tocar|coloca|colocar|põe|bota|a|o|um|umas|uma|alguma|algumas|música|músicas|som|playlist|ai|aí|pra|mim)\b', '', t).strip()
        query = re.sub(r'[^a-zA-Z0-9\s\-\u00C0-\u00FF]', '', query).strip()
        return f"PLAY:{query}" if query else "PLAY:uma música aleatória"
    
    if len(t.split()) <= 6 and re.match(r'^(toca|coloca|põe|bota)\b', t):
        query = re.sub(r'^(toca|coloca|põe|bota|a|o|um|uma|umas|alguma)\b', '', t).strip()
        return f"PLAY:{query}" if query else "PLAY:uma recomendação aleatória"
        
    return None

def capturar_tela_b64():
    try:
        img = ImageGrab.grab()
        img.thumbnail((1024, 1024))
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=70)
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    except Exception as e:
        print(f" Erro ao capturar ecrã: {e}")
        return None
#endregion
# ======================================================
#region 🧠 BRAIN E PERSISTÊNCIA
# ======================================================
def carregar_brain():
    if not os.path.exists(BRAIN_FILE):    
        return {}, "Sistema Padrão", "Assistente", False, False, {"local": "nvidia"}, False # Agora retorna 7 valores corretos
    
    with open(BRAIN_FILE, 'r', encoding='utf-8') as f:
        brain = json.load(f)
        
    p = brain.get('personality', {'name': 'Assistente', 'role': 'Assistente de IA'})
    nome_ai = p.get('name', 'Assistente')
    traits = "\n- ".join(p.get('traits', []))
    
    r = "\n- ".join(brain.get('rules', {}).get('response_style', []))
    s = brain.get('emotional_analysis', {}).get('sentiment', 'Neutral')
    trigger = brain.get("trigger_active", False)
    discord_active = brain.get("discord_active", False) 
    modelos = brain.get("modelos_ativos", {"local": "nvidia", "discord": "groq"})
    vtuber_ativo = brain.get("vtuber_overlay_ativo", False)
    
    relacionamentos = brain.get('relationships', {})
    nome_user = list(relacionamentos.keys())[0] if relacionamentos else "Mestre"
    user_data = relacionamentos.get(nome_user, {})
    relacao = f"Nome do Usuário com quem você está falando: {nome_user}\nRelação: {user_data.get('relationship', 'Mestre')}\nComportamento com ele: {user_data.get('behavior', '')}"
    
    vocab_dict = brain.get('vocabulário', {})
    vocabulario = "\n- ".join([f"{k}: {v}" for k, v in vocab_dict.items()])

    tela_atual = brain.get('visual_context', {}).get('screen_content', '')

    prompt = (
        f"Nome: {nome_ai}\n"
        f"Papel: {p.get('role', 'Assistente')}\n\n"
        f"Traços de Personalidade:\n- {traits}\n\n"
        f"Sobre o Usuário:\n{relacao}\n\n"
        f"Estado Emocional: {s}\n\n"
        f"Diretrizes de Conversa (Incorpore de forma fluida e natural, varie as estruturas das frases):\n- {r}\n\n"
        f"Vocabulário Contextual (Use estas palavras/gírias de forma esporádica e APENAS se encaixar perfeitamente no assunto):\n- {vocabulario}"
    )
    
    if tela_atual:
        prompt += f"\n\n[CONTEXTO VISUAL ATUAL DA TELA]:\n- {tela_atual}"
    
    # 🔥 Retornando 7 variáveis rigorosamente na ordem correta
    return brain, prompt, nome_ai, trigger, discord_active, modelos, vtuber_ativo

def salvar_gatilho_brain(estado):
    if os.path.exists(BRAIN_FILE):
        with open(BRAIN_FILE, 'r', encoding='utf-8') as f: data = json.load(f)
        data["trigger_active"] = estado
        with open(BRAIN_FILE, 'w', encoding='utf-8') as f: json.dump(data, f, indent=4, ensure_ascii=False)

def salvar_discord_brain(estado):
    if os.path.exists(BRAIN_FILE):
        with open(BRAIN_FILE, 'r', encoding='utf-8') as f: data = json.load(f)
        data["discord_active"] = estado
        with open(BRAIN_FILE, 'w', encoding='utf-8') as f: json.dump(data, f, indent=4, ensure_ascii=False)

def salvar_visao_brain(descricao):
    if os.path.exists(BRAIN_FILE):
        with open(BRAIN_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if "visual_context" not in data: data["visual_context"] = {}
        data["visual_context"]["screen_content"] = descricao
        with open(BRAIN_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
#endregion
# ======================================================
#region 📚 GERENCIADOR DE MEMÓRIA
# ======================================================
def carregar_memoria():
    if not os.path.exists(MEMORIA_FILE): return {"master_summary": "", "recent_summaries": [], "mensagens": []}
    try:
        with open(MEMORIA_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    except: return {"master_summary": "", "recent_summaries": [], "mensagens": []}

def salvar_memoria(memoria):
    with open(MEMORIA_FILE, 'w', encoding='utf-8') as f:
        json.dump(memoria, f, indent=4, ensure_ascii=False)

def carregar_memoria_pesquisa():
    if not os.path.exists(SEARCH_MEMORY_FILE): return {"master_search_summary": "", "recent_searches": []}
    try:
        with open(SEARCH_MEMORY_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    except: return {"master_search_summary": "", "recent_searches": []}

async def gerenciar_memoria_pesquisa(client_llm, query, resultados):
    memoria = carregar_memoria_pesquisa()
    memoria["recent_searches"].append({"query": query, "resultados": resultados[:400]})

    if len(memoria["recent_searches"]) >= 5:
        print("\n [SISTEMA] Otimizando banco de dados de Pesquisas (Resumindo web)...")
        textos_resumo = [f"Busca: '{m['query']}' | Resultado: {m['resultados']}" for m in memoria["recent_searches"]]
        if memoria["master_search_summary"]: textos_resumo.insert(0, f"Conhecimento Web Anterior: {memoria['master_search_summary']}")
        master_resumo = await resumir_com_ia(client_llm, textos_resumo, "Você é um bibliotecário digital. Faça um resumo direto e conciso de todo o conhecimento e fatos adquiridos nestas pesquisas web. Descarte informações irrelevantes e foque apenas nos fatos úteis que podem servir de contexto no futuro.")
        if master_resumo:
            memoria["master_search_summary"] = master_resumo
            memoria["recent_searches"] = [] 

    with open(SEARCH_MEMORY_FILE, 'w', encoding='utf-8') as f: json.dump(memoria, f, indent=4, ensure_ascii=False)
    return memoria

async def resumir_com_ia(client_llm, textos, comando):
    texto_junto = "\n".join(textos)
    try:
        res = await asyncio.to_thread(lambda: client_llm.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct", 
            messages=[{"role": "system", "content": comando}, {"role": "user", "content": texto_junto}],
            temperature=0.3
        ))
        return res.choices[0].message.content
    except Exception as e:
        print(f" Erro ao resumir memória: {e}")
        return ""

async def gerenciar_e_salvar_memoria(client_llm, sender, message):
    memoria = carregar_memoria()
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    memoria["mensagens"].append({"timestamp": agora, "sender": sender, "message": message})

    if len(memoria["mensagens"]) >= 15:
        print("\n [SISTEMA] Otimizando memória (Resumindo conversas antigas)...")
        msgs_para_resumir = memoria["mensagens"][:10]
        textos_resumo = [f"[{m['timestamp']}] {m['sender']}: {m['message']}" for m in msgs_para_resumir]
        
        novo_resumo = await resumir_com_ia(client_llm, textos_resumo, "Faça um resumo direto e curto sobre o que foi conversado nessas mensagens.")
        if novo_resumo:
            memoria["recent_summaries"].append(novo_resumo)
            memoria["mensagens"] = memoria["mensagens"][10:] 

        if len(memoria["recent_summaries"]) >= 5:
            print(" [SISTEMA] Consolidando Resumo Mestre...")
            textos_master = memoria["recent_summaries"].copy()
            if memoria["master_summary"]: textos_master.insert(0, f"Resumo Histórico: {memoria['master_summary']}")
            master_resumo = await resumir_com_ia(client_llm, textos_master, "Integre todos esses resumos em um único 'Resumo Mestre' detalhando tudo o que já aconteceu com o usuário.")
            if master_resumo:
                memoria["master_summary"] = master_resumo
                memoria["recent_summaries"] = [] 

    salvar_memoria(memoria)
    return memoria

def construir_historico_para_api(sys_prompt, memoria, nome_ai, launcher=None):
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 🔥 INJETOR DE AUTORIDADE E CAPACIDADES CRÍTICAS 🔥
    prompt_completo = sys_prompt + f"\n\n[SISTEMA DE CAPACIDADES MÁXIMAS]:"
    prompt_completo += "\n1. CONTROLO DE MÚSICA: Você É o bot de música. Nunca diga que não pode tocar. Use OBRIGATORIAMENTE a tag <PLAY:pedido> para tocar qualquer coisa no Discord."
    prompt_completo += "\n2. CONTROLO DO PC: Você tem acesso total ao PC do Nero. Use <APP:abrir:alvo> ou <APP:fechar:alvo> para comandar o computador. Não invente que é apenas uma IA de texto."
    prompt_completo += "\n3. BUSCA WEB: Use [PESQUISAR: termo] para ler notícias e dados atuais. Você é conectada à internet."
    
    prompt_completo += f"\n\n[SISTEMA DE TEMPO]\nO momento atual exato é: {agora}.\nVocê recebe o horário para entender o ritmo da conversa."
    
    prompt_completo += "\n\n[REGRAS ESTRITAS DE RESPOSTA]:"
    prompt_completo += "\n- ZERO ROLEPLAY: Proibido narrar ações físicas, usar itálicos ou asteriscos (ex: *sorri*). Fale como uma pessoa real."
    prompt_completo += "\n- ZERO TAGS FALSAS: Nunca invente tags como <ignore> ou <pensamento>. Use apenas as oficiais ensinadas aqui."
    prompt_completo += "\n- SEJA CURTA E GROSSA: Responda em 1 ou 2 frases curtas. Você odeia textões e explicações desnecessárias."
    
    if launcher and hasattr(launcher, 'obter_nomes_dos_apps'):
        nomes_apps = launcher.obter_nomes_dos_apps()
        prompt_completo += f"\n\n[INTEGRAÇÃO COM O COMPUTADOR]:"
        prompt_completo += f"\n📂 APLICATIVOS INSTALADOS: {nomes_apps}."
        prompt_completo += "\nPara abrir ou pesquisar no navegador/youtube, use: <APP:abrir:alvo:termo_de_busca>."
        
        prompt_completo += "\n\n[MANUAL DO PLAYER DE MÚSICA]:"
        prompt_completo += "\n- TOCAR: <PLAY:nome_da_musica>"
        prompt_completo += "\n- PULAR: <SKIP>"
        prompt_completo += "\n- PAUSAR: <PAUSE>"
        prompt_completo += "\n- PARAR: <STOP>"
        prompt_completo += "\n🚨 REGRA DE OURO DA MÚSICA:"
        prompt_completo += "\n1. É OBRIGATÓRIO escrever uma frase sua (entre 1 e 7 palavras) ANTES de colocar a tag. NUNCA envie apenas a tag! (Ex: 'Aqui está a sua música. <PLAY:rock>')."
        prompt_completo += "\n2. NUNCA tente adivinhar nomes de músicas de animes ou séries. O sistema usa o YouTube, por isso gere a tag EXATAMENTE com as palavras que o usuário usou."
        prompt_completo += "\n3. É ESTRITAMENTE PROIBIDO tocar música do nada. NUNCA use a tag <PLAY> se o usuário não lhe deu uma ordem clara para tocar algo."
    # Integração de Memórias
    memoria_pesquisa = carregar_memoria_pesquisa()
    if memoria_pesquisa.get("master_search_summary"):
        prompt_completo += f"\n\n[CONHECIMENTO WEB ADQUIRIDO]:\n{memoria_pesquisa['master_search_summary']}"

    if memoria["master_summary"]:
        prompt_completo += f"\n\n[MEMÓRIA DE LONGO PRAZO]:\n{memoria['master_summary']}"
        
    if memoria["recent_summaries"]:
        prompt_completo += f"\n\n[ACONTECIMENTOS RECENTES]:\n" + "\n".join(memoria["recent_summaries"])

    # Construção do histórico para a API
    historico = [{"role": "system", "content": prompt_completo}]
    
    for m in memoria["mensagens"]:
        role = "assistant" if m["sender"] == nome_ai else "user"
        if role == "user":
            historico.append({"role": role, "content": f"[Enviado em {m['timestamp']}] {m['message']}"})
        else:
            msg_limpa = m['message'].split("] ", 1)[-1] if m['message'].startswith("[2026") else m['message']
            msg_limpa = re.sub(rf"^{nome_ai} disse:\s*", "", msg_limpa, flags=re.IGNORECASE)
            msg_limpa = re.sub(rf"^{nome_ai}:\s*", "", msg_limpa, flags=re.IGNORECASE)
            historico.append({"role": role, "content": msg_limpa.strip()})
            
    return historico
#endregion
# ======================================================
#region 🎵 FEEDBACKS SONOROS E ÁUDIO
# ======================================================
def play_beep(tipo="inicio"):
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2)
        duration = 0.1
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        freq = 800 if tipo == "inicio" else 400
        t = np.linspace(0, duration, n_samples, False)
        signal = np.sin(2 * np.pi * freq * t) * 0.3
        sound_array = (signal * 32767).astype(np.int16)
        stereo_array = np.column_stack((sound_array, sound_array))
        sound = pygame.sndarray.make_sound(stereo_array)
        sound.play()
    except Exception as e:
        pass

class LocalVoiceFilter:
    def __init__(self):
        self.model, _ = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', force_reload=False)
    
    def is_human_voice(self, audio_data, rate=16000):
        audio_int16 = np.frombuffer(audio_data, dtype=np.int16)
        if np.max(np.abs(audio_int16)) < 300: return False
        audio_float32 = audio_int16.astype(np.float32) / 32768.0
        tensor = torch.from_numpy(audio_float32)
        with torch.no_grad():
            confidence = self.model(tensor, rate).item()
        return confidence > 0.75

async def microsoft_speak(text): 
    if not text: return
    VOICE = "pt-BR-FranciscaNeural" 
    output_file = "vocal_.mp3"
    
    # 🔥 Limpa tags do sistema (<APP...>, etc)
    text_limpo_voz = re.sub(r'<[^>]+>', '', text).strip()
    
    # 🔥 SALVAÇÃO DA MATEMÁTICA: Se o * estiver entre números, vira "vezes"
    text_limpo_voz = re.sub(r'(?<=\d)\s*\*\s*(?=\d)', ' vezes ', text_limpo_voz)
    
    # 🔥 Arranca qualquer outro asterisco inútil que sobrou (formatação/roleplay)
    text_limpo_voz = text_limpo_voz.replace('*', '') 
    
    if not text_limpo_voz:
        text_limpo_voz = "Comando executado."
        
    communicate = edge_tts.Communicate(text_limpo_voz, VOICE)
    await communicate.save(output_file)
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy(): await asyncio.sleep(0.1)
    pygame.mixer.quit()

async def whisper_transcription(audio_frames, api_key):
    audio_data = b''.join(audio_frames)
    with io.BytesIO() as wb:
        with wave.open(wb, 'wb') as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(16000)
            wf.writeframes(audio_data)
        wb.seek(0)
        final_wav = wb.read()
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    head = {"Authorization": f"Bearer {api_key}"}
    files = {"file": ("input.wav", final_wav, "audio/wav"), "model": (None, "whisper-large-v3-turbo"), "language": (None, "pt")}
    resp = await asyncio.to_thread(requests.post, url, headers=head, files=files)
    return resp.json().get("text", "") if resp.status_code == 200 else None
#endregion
# ======================================================
#region 🕹️ CÉREBRO DA IA (PROCESSAMENTO INTEGRADO LLM + SCOUT)
# ======================================================
async def processar_ia(client_nvidia, client_llm, client_vision, sys_prompt, texto, nome_ai, usuario_nome, launcher, modo_chat=False):
    if not modo_chat:
        print(f"{usuario_nome}: {texto}")
        
    await gerenciar_e_salvar_memoria(client_llm, usuario_nome, texto)
    memoria_atual = carregar_memoria()
    
    historico_api = construir_historico_para_api(sys_prompt, memoria_atual, nome_ai, launcher)
    
    # 🔥 INJETOR DE PRESSÃO: Força o LLM a não esquecer a tag da música
    comando_musica = detectar_comando_musica(texto)
    if comando_musica:
        alerta = f"\n\n[ALERTA DE SISTEMA DO CÉREBRO]: Você OBRIGATORIAMENTE deve incluir a tag <{comando_musica}> no final da sua próxima fala para a música obedecer ao usuário. Sem a tag, a música não mudará!"
        historico_api[-1]["content"] += alerta
    
    # 👁️ LÓGICA DE VISÃO
    if VISAO_HABILITADA and requer_visao(texto):
        print(" [SISTEMA] Intenção visual detetada! A analisar o ecrã com o Scout...")
        b64_img = capturar_tela_b64()
        if b64_img:
            prompt_vision = f"Descreva a imagem. Identifique contexto, textos, ações e detalhes.\nO usuário pediu: '{texto}'. Foque nisso."
            try:
                res_vision = await asyncio.to_thread(lambda: client_vision.chat.completions.create(
                    model="meta-llama/llama-4-scout-17b-16e-instruct",
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_vision},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
                        ]
                    }],
                    max_tokens=1024,
                    temperature=0.1
                ))
                descricao_imagem = res_vision.choices[0].message.content
                print(f" [ANÁLISE SCOUT CONCLUÍDA]")
                
                salvar_visao_brain(descricao_imagem)
                _, sys_prompt_atualizado, _, _, _, _, *_ = carregar_brain()
                historico_api = construir_historico_para_api(sys_prompt_atualizado, memoria_atual, nome_ai, launcher)
                historico_api[-1]["content"] += "\n\n[SISTEMA: Acabei de analisar o ecrã a teu pedido. O contexto visual atualizado já se encontra na tua mente.]"
                
            except Exception as e:
                print(f" Erro na API de Visão (Scout): {e}")

    # 🧠 LÓGICA DO CÉREBRO PRINCIPAL
    _, _, _, _, _, modelos_config, *_ = carregar_brain()
    provedor_local = modelos_config.get("local", "nvidia")
    
    if provedor_local == "nvidia":
        cliente_ativo = client_nvidia
        id_modelo = "moonshotai/kimi-k2.5"
        extra = {"chat_template_kwargs": {"thinking": False}}
    else:
        cliente_ativo = client_llm
        id_modelo = "meta-llama/llama-4-scout-17b-16e-instruct"
        extra = None

    try:
        kwargs_initial = {
            "model": id_modelo,
            "messages": historico_api,
            "temperature": 0.7
        }
        if extra: kwargs_initial["extra_body"] = extra

        res = await asyncio.to_thread(lambda: cliente_ativo.chat.completions.create(**kwargs_initial))
        resposta_inicial = res.choices[0].message.content
        resposta_inicial = re.sub(r'<think>.*?</think>', '', resposta_inicial, flags=re.IGNORECASE | re.DOTALL).strip()
        
        resposta_final = resposta_inicial
        precisa_nova_resposta = False

        # 🔥 1. INTERCEPTADOR E LIMPEZA DE MÚSICA LOCAL
        match_musica = re.search(r'<(PLAY:[^>]+|SKIP|PAUSE|STOP|RESUME)[^>]*>', resposta_inicial, re.IGNORECASE)
        if match_musica:
            tag_musica = match_musica.group(1).upper()
            tag_completa = match_musica.group(0)
            
            resposta_inicial = resposta_inicial.replace(tag_completa, "").strip()
            resposta_final = resposta_inicial 

            try:
                if os.path.exists(BRAIN_FILE):
                    with open(BRAIN_FILE, "r+", encoding="utf-8") as f:
                        brain_data = json.load(f)
                        brain_data["pending_music"] = f"<{tag_musica}>"
                        f.seek(0)
                        json.dump(brain_data, f, indent=4, ensure_ascii=False)
                        f.truncate()
                print(f"🎵 [SISTEMA] Comando de música enviado ao Discord: <{tag_musica}>")
            except Exception as e:
                print(f"❌ Erro ao enviar comando remoto para o Discord: {e}")

        # 🔥 2. VERIFICAÇÃO DE AÇÕES (APP E PESQUISA)
        if "<APP:" in resposta_inicial:
            resultado_app = launcher.process_llm_tag(resposta_inicial)
            if resultado_app:
                historico_api.append({"role": "assistant", "content": resposta_inicial})
                historico_api.append({"role": "user", "content": f"[SISTEMA DE AUTOMAÇÃO]: {resultado_app}"})
                precisa_nova_resposta = True

        if "PESQUISAR:" in resposta_inicial.upper():
            match = re.search(r"[\[<]PESQUISAR:\s*(.*?)[\]>]", resposta_inicial, re.IGNORECASE)
            if match:
                termo = match.group(1).strip()
                print(f" [SISTEMA] IA ativou busca autônoma para: '{termo}'")
                
                resultados_web = search_ddg.search_ddg(termo)
                await gerenciar_memoria_pesquisa(client_llm, termo, resultados_web)
                
                if not precisa_nova_resposta:
                    msg_limpa = re.sub(r"[\[<]PESQUISAR:.*?[\]>]", "", resposta_inicial, flags=re.IGNORECASE).strip()
                    if msg_limpa:
                        historico_api.append({"role": "assistant", "content": msg_limpa})
                
                historico_api.append({"role": "user", "content": f"[SISTEMA DE BUSCA]: Resultados encontrados para '{termo}':\n{resultados_web}"})
                precisa_nova_resposta = True

        if precisa_nova_resposta:
            historico_api.append({"role": "user", "content": "Agora dê a sua resposta definitiva ao usuário incorporando o que aconteceu. REGRA ABSOLUTA: Fale com a sua personalidade de forma fluida. É PROIBIDO FAZER ROLEPLAY DE AÇÕES (NUNCA use asteriscos). NUNCA use a palavra 'pesquisa', não diga que buscou na web, e não mencione tags ou comandos. Aja simplesmente como se você tivesse lembrado dessa informação de cabeça."})
            
            kwargs_final = {
                "model": id_modelo,
                "messages": historico_api,
                "temperature": 0.7
            }
            if extra: kwargs_final["extra_body"] = extra

            res_final = await asyncio.to_thread(lambda: cliente_ativo.chat.completions.create(**kwargs_final))
            resposta_final = res_final.choices[0].message.content
            resposta_final = re.sub(r'<think>.*?</think>', '', resposta_final, flags=re.IGNORECASE | re.DOTALL).strip()

        # 🧹 LIMPEZA BRUTAL FINAL: Remove qualquer outra tag <...> do terminal 
        resposta_final = re.sub(r'<[^>]+>', '', resposta_final).strip()

        # 🔥 NOVO: Se a IA enviar só a tag e a resposta ficar vazia, o próprio LLM gera a frase curta!
        if not resposta_final:
            historico_fallback = [{"role": "system", "content": f"Aja como {nome_ai}, usando a sua personalidade sarcástica. Fale uma frase curta (entre 1 a 7 palavras) confirmando que acabou de executar o comando que o usuário pediu. Não use tags nem asteriscos."}]
            try:
                res_fall = await asyncio.to_thread(lambda: cliente_ativo.chat.completions.create(
                    model=id_modelo, messages=historico_fallback, temperature=0.9, extra_body=extra
                ))
                resposta_final = res_fall.choices[0].message.content
                resposta_final = re.sub(r'<think>.*?</think>', '', resposta_final, flags=re.IGNORECASE | re.DOTALL)
                resposta_final = re.sub(r'<[^>]+>', '', resposta_final).strip()
            except:
                resposta_final = "Feito."

        print(f"{nome_ai}: {resposta_final}")
        await gerenciar_e_salvar_memoria(client_llm, nome_ai, resposta_final)
        await microsoft_speak(resposta_final)
        
    except Exception as e:
        print(f" Erro na API LLM ({provedor_local}): {e}")
#endregion
# ======================================================
# region 🎤 MODOS DE OPERAÇÃO
# ======================================================
async def run_modo_continuo(client_nvidia, client_llm, client_vision, sys_prompt, voice_filter, api_key_whisper, nome_ai, usuario_nome, launcher):
    if not pyaudio:
        print("❌ PyAudio não disponível - Modo voz desativado")
        print("   Configure PyAudio localmente para usar este modo")
        return
    
    print("\n" + "="*30)
    print(" MODO VOZ ATIVA (ESCUTA CONTÍNUA)")
    print("F1: Gatilho de Voz | F2: Visão Computacional | HOME: Menu")
    print("="*30)
    
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=512)
    frames, is_recording, silence_timer = [], False, 0

    while True:
        if keyboard.is_pressed('home'): break

        data = stream.read(512, exception_on_overflow=False)
        if voice_filter.is_human_voice(data):
            if not is_recording: is_recording = True
            frames.append(data); silence_timer = 0
        elif is_recording:
            silence_timer += 1
            if silence_timer > 35: # Tempo de silêncio para processar
                is_recording = False
                texto = await whisper_transcription(frames, api_key_whisper)
                frames = []
                if texto:
                    # 🔥 LÊ O ESTADO ATUALIZADO DO GATILHO ANTES DE PROCESSAR
                    _, _, _, trigger_ativo, _, _, *_ = carregar_brain()
                    if trigger_ativo:
                        if requer_despertar(texto, nome_ai): 
                            await processar_ia(client_nvidia, client_llm, client_vision, sys_prompt, texto, nome_ai, usuario_nome, launcher, modo_chat=False)
                        else:
                            print(f" [IGNORADO] Áudio captado: '{texto}' (Palavra de despertar não detetada)")
                    else:
                        await processar_ia(client_nvidia, client_llm, client_vision, sys_prompt, texto, nome_ai, usuario_nome, launcher, modo_chat=False)
        await asyncio.sleep(0.01)
    stream.stop_stream(); stream.close(); p.terminate()
    
async def run_modo_click(client_nvidia, client_llm, client_vision, sys_prompt, api_key_whisper, nome_ai, usuario_nome, launcher):
    if not pyaudio:
        print("❌ PyAudio não disponível - Modo Click-to-Talk desativado")
        print("   Configure PyAudio localmente para usar este modo")
        return
    
    print("\n" + "="*30)
    print(" MODO CLICK-TO-TALK")
    print("R-SHIFT: Clica Grava / Clica Envia")
    print("F3: Gatilho | F2: Visão | HOME: Menu")
    print("="*30)
    
    RATE = 16000
    CHUNK = 1024

    while True:
        try:
            while True:
                if keyboard.is_pressed('home'): return
                if keyboard.is_pressed('right shift'):
                    play_beep("inicio")
                    break
                await asyncio.sleep(0.05)

            while keyboard.is_pressed('right shift'): await asyncio.sleep(0.01)

            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
            frames = []
            
            print(" A gravar... (Clica R-SHIFT para enviar)")
            while True:
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
                
                if keyboard.is_pressed('home'):
                    stream.stop_stream(); stream.close(); p.terminate()
                    return
                if keyboard.is_pressed('right shift'):
                    play_beep("fim")
                    break
                await asyncio.sleep(0.001)
                
            stream.stop_stream(); stream.close(); p.terminate()
            print(" A enviar para a IA...")
            while keyboard.is_pressed('right shift'): await asyncio.sleep(0.01)

            texto = await whisper_transcription(frames, api_key_whisper)
            if texto: 
                # 🔥 LÊ O ESTADO ATUALIZADO DO GATILHO ANTES DE PROCESSAR
                _, _, _, trigger_ativo, _, _, *_ = carregar_brain()
                if trigger_ativo:
                    if nome_ai.lower() in texto.lower(): 
                        await processar_ia(client_nvidia, client_llm, client_vision, sys_prompt, texto, nome_ai, usuario_nome, launcher, modo_chat=False)
                    else:
                        print(f" [IGNORADO] Gatilho ativo, mas o nome '{nome_ai}' não foi mencionado.")
                else:
                    await processar_ia(client_nvidia, client_llm, client_vision, sys_prompt, texto, nome_ai, usuario_nome, launcher, modo_chat=False)

        except Exception as e:
            print(f" Erro no Modo Clique: {e}")
            break
#endregion
# ======================================================
#region 🚀 MAIN
# ======================================================
def main():
    brain_raw, sys_prompt, nome_ai, trigger, discord_active, modelos, vtuber_ativo = carregar_brain()

    print(f"🎨 Iniciando Emma...")
    
    # 🚀 Em modo Railway, desabilita componentes locais
    if not RAILWAY_MODE:
        # GUI thread comentada - RemGUI ainda não implementada
        # gui_thread = threading.Thread(target=RemGUI.iniciar_gui_loop, args=(nome_ai,), daemon=True)
        # gui_thread.start()

        # 🔥 REGISTRANDO OS ATALHOS GLOBAIS ABSOLUTOS (AGORA APENAS UMA ÚNICA VEZ!)
        try:
            keyboard.add_hotkey('f4', lambda: print("F4 - GUI Toggle (em desenvolvimento)"))
            keyboard.on_press_key('f2', toggle_visao)
            keyboard.on_press_key('f3', toggle_gatilho)
            print("✅ Atalhos de teclado ativados (F2, F3, F4)")
        except Exception as e:
            print(f"⚠️ Aviso: Atalhos de teclado desativados (requer sudo ou permissões elevadas): {e}")
            print("   Você pode usar o menu interativo normalmente.")
    else:
        print("⏭️  [RAILWAY] GUI e atalhos desativados em modo nuvem")

    NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
    GROQ_API_KEY_LLM = os.getenv("GROQ_API_KEY_LLM")
    GROQ_API_KEY_VISION = os.getenv("GROQ_API_KEY_VISION")

    if not GROQ_API_KEY_LLM or not GROQ_API_KEY_VISION or not NVIDIA_API_KEY:
        print(" ERRO FATAL: Chaves da Groq ou NVIDIA não encontradas. Verifica o teu ficheiro .env!")
        return
    
    # Atualiza as variáveis do cérebro caso o usuário tenha salvo algo no painel
    brain_raw, sys_prompt, nome_ai, trigger, discord_active, modelos, vtuber_ativo = carregar_brain()

    # 🔥 CHAMA O SCRIPT DO VTUBER SE ESTIVER ATIVADO (Desabilidado em Railway)
    if vtuber_ativo and not RAILWAY_MODE:
        print("🎭 Iniciando módulo VTuber Overlay em segundo plano...")
        try:
            subprocess.Popen([sys.executable, "Arcana/Net/vtuber_overlay.py"])
        except Exception as e:
            print(f"❌ Erro ao iniciar o VTuber Overlay: {e}")

    # 🧠 TRÊS CLIENTES SEPARADOS (A puxar do .env)
    client_nvidia = OpenAI(api_key=NVIDIA_API_KEY, base_url="https://integrate.api.nvidia.com/v1")
    client_llm = Groq(api_key=GROQ_API_KEY_LLM)
    client_vision = Groq(api_key=GROQ_API_KEY_VISION)
    
    voice_filter = LocalVoiceFilter()
    
    # Puxando o nome do Usuário dinamicamente
    relacionamentos_main = brain_raw.get('relationships', {})
    usuario_nome = list(relacionamentos_main.keys())[0] if relacionamentos_main else "Usuário"
    
    # 🔥 INICIA O MÓDULO DE AUTOMAÇÃO INVISÍVEL (Desabilidado em Railway)
    launcher = AppLauncher() if not RAILWAY_MODE else None

    carregar_memoria()
    
    # [O ERRO ESTAVA AQUI: Existia um keyboard.on_press_key('f2', toggle_visao) fantasma! Removido.]

    discord_thread = None
    if discord_active:
        print("\n🌐 Despertando a Emma no Discord...")
        # Em Railway modo, inicia Discord Bot como processo principal
        if RAILWAY_MODE:
            print("🚀 [RAILWAY MODE] Iniciando Discord Bot como processo principal...")
            run_discord_bot()
            return
        else:
            pass
#        discord_thread = threading.Thread(target=run_discord_bot, daemon=True)
#        discord_thread.start()

    # Em modo local, mostra menu interativo
    if RAILWAY_MODE:
        print("⚠️ [RAILWAY] Modo interativo desativado. Use Discord Bot API.")
        return
    
    while True:
        _, _, _, trigger, discord_active, modelos, _ = carregar_brain()
        print(f"\n{'='*15} MENU {nome_ai} {'='*15}")
        print(f"Gatilho F3: {'LIGADO' if trigger else 'DESLIGADO'}")
        print(f"Visão F2: {'LIGADA' if VISAO_HABILITADA else 'DESLIGADA'}")
        print(f"Discord: {'LIGADO' if discord_active else 'DESLIGADO'}")
        print(f"Utilizador atual: {usuario_nome}")
        print("| 1. Chat")
        print("| 2. Voz Contínua")
        print("| 3. Click-to-Talk")
        print("| 4. Alternar Discord")
        print("| 5.  Painel Gráfico (Mudar Cérebro Nvidia/Groq)")
        print("| q. Sair")
        
        op = input("Opção: ")
        if op == '1':
            while True:
                msg = input("Você: ")
                if msg == 'q': break
                asyncio.run(processar_ia(client_nvidia, client_llm, client_vision, sys_prompt, msg, nome_ai, usuario_nome, launcher, modo_chat=True))
        elif op == '2': 
            if not RAILWAY_MODE:
                asyncio.run(run_modo_continuo(client_nvidia, client_llm, client_vision, sys_prompt, voice_filter, GROQ_API_KEY_LLM, nome_ai, usuario_nome, launcher))
            else:
                print("⚠️ Modo Voz não disponível em Railway")
        elif op == '3': 
            if not RAILWAY_MODE:
                asyncio.run(run_modo_click(client_nvidia, client_llm, client_vision, sys_prompt, GROQ_API_KEY_LLM, nome_ai, usuario_nome, launcher))
            else:
                print("⚠️ Click-to-Talk não disponível em Railway")
        elif op == '4':
            discord_active = not discord_active
            salvar_discord_brain(discord_active)
            if discord_active:
                print(f"\n [SISTEMA] Discord foi LIGADO e salvo na memória.")
                if discord_thread is None or not discord_thread.is_alive():
                    print("🌐 Despertando a Emma no Discord...")
                    discord_thread = threading.Thread(target=run_discord_bot, daemon=True)
                    discord_thread.start()
            else:
                print(f"\n [SISTEMA] Discord foi DESLIGADO (A ligação ao servidor será encerrada no próximo reinício do script).")
        elif op == '5':
            if not RAILWAY_MODE:
                abrir_gui_modelos()
            else:
                print("⚠️ Painel Gráfico não disponível em Railway")
        
        elif op == 'q': break

if __name__ == "__main__":
    main()
#endregion
# ============//======================//================