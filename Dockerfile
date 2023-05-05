# Imagem base
FROM python:3.8-slim-buster

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte para o diretório de trabalho
COPY . .

# Expõe a porta 8050 (padrão do Dash)
EXPOSE 8050

# Define o comando a ser executado quando a imagem for iniciada
CMD ["python", "index.py"]