# Stage 1: Builder - instala dependências
FROM python:3.12-slim as builder

WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime - imagem final otimizada
FROM python:3.12-slim

WORKDIR /app

# Copiar apenas pacotes Python instalados do stage 1
COPY --from=builder /root/.local /root/.local

# Copiar apenas arquivos necessários
COPY run.py .
COPY Arcana/ Arcana/
COPY .env.example .

# Criar diretório de persistência
RUN mkdir -p Arcana/armazen

# Configurar PATH para usar pip packages
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV RAILWAY_MODE=true

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import discord; print('OK')" || exit 1

CMD ["python", "run.py"]
