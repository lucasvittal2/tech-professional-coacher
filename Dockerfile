# Imagem base slim para produção
FROM python:3.11-slim

# Diretório de trabalho no container
WORKDIR /app

# Instala dependências do sistema necessárias
RUN apt-get update && \
    apt-get install -y gcc curl build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copia apenas o arquivo wheel para o container
COPY dist/tech_professional_coacher-0.1.0-py3-none-any.whl ./


#copia arquivos de configuracao e dependencias externas
COPY .env ./
COPY pyproject.toml ./
COPY uv.lock ./
COPY README.md ./

# copia codigo fonte
COPY tech_professional_coacher/ ./tech_professional_coacher/



# Instala o pacote wheel
RUN pip install --no-cache-dir tech_professional_coacher-0.1.0-py3-none-any.whl
RUN pip install --no-cache-dir gunicorn uvicorn
RUN pip install --no-cache-dir uv
RUN uv sync

# Expõe a porta do app
EXPOSE 8070

# Comando para rodar o app usando Gunicorn com UvicornWorker
CMD ["gunicorn", "tech_professional_coacher.api.app:testApp", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8070"]
