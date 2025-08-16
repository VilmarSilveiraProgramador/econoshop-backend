# Use uma imagem base do Python com o Ubuntu (onde apt-get está disponível)
FROM python:3.11-slim

# Instale o Tesseract OCR e as linguagens necessárias
RUN apt-get update && apt-get install -y tesseract-ocr && apt-get install -y libtesseract-dev && apt-get install -y tesseract-ocr-por

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos do projeto para o diretório de trabalho
COPY . .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]