FROM python:3.9-slim

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivo de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p darms inserts

# Definir volumes para dados
VOLUME ["/app/darms", "/app/inserts"]

# Expor porta (se necessário para interface web futura)
# EXPOSE 8000

# Comando padrão
CMD ["python", "darm_processor.py"] 