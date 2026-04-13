FROM python:3.12-slim

WORKDIR /app

# Copiar requirements e instalar (PyAudio removido - não funciona em Railway)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Criar diretório
RUN mkdir -p Arcana/armazen

# Executar
CMD ["python", "run.py"]
