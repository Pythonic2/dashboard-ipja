# Usar uma imagem base oficial do Python
FROM python:3.10

# Definir o diretório de trabalho no contêiner
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Instalar o Streamlit e outras dependências do projeto
RUN pip install streamlit

# Expor a porta que o Streamlit vai rodar (padrão 8501)
EXPOSE 8501

# Comando para rodar o Streamlit
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
