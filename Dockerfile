#camada base do aplicativo, baixa template do servidor 
FROM python:3.8.11-slim

#Setando as variáveis de ambiente
#Definindo a porta padrão
ENV PORT 8501

#estabelece a pasta raiz na imagem
WORKDIR /app

#COPY: copia os arquivos da máquina física para a imagem docker
COPY requirements.txt ./
COPY 07_app.py ./
COPY Models/encoder_v0.joblib ./Models/
COPY Models/classifier_v0.joblib ./Models/
COPY logo3.PNG ./

#instala as bibliotecas específicas na imagem
RUN pip install -U pip
RUN pip install -r requirements.txt

#códico a ser executado no terminal da imagem
CMD streamlit run --server.enableCORS=False --server.port=$PORT 07_app.py
