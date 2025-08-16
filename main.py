from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pytesseract
from PIL import Image
import io

# Cria a instância do FastAPI
app = FastAPI()

# Configuração do CORS (Cross-Origin Resource Sharing)
origins = [
    "https://prismatic-griffin-246daf.netlify.app",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rota de teste
@app.get("/test")
async def test_connection():
    return {"message": "Backend do EconoShop está funcionando!"}


# Rota para processar a imagem com OCR
@app.post("/process-image")
async def process_image_with_ocr(file: UploadFile = File(...)):
    try:
        # Lê o conteúdo da imagem em memória
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        # Configura o Tesseract para usar a língua portuguesa
        # Você pode precisar ajustar o caminho do tesseract.exe se estiver rodando localmente no Windows
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        # Extrai o texto da imagem
        extracted_text = pytesseract.image_to_string(image, lang='por')

        # Opcional: processamento do texto para extrair dados (preço, quantidade)
        # Este é um passo futuro e pode ser mais complexo

        return {
            "filename": file.filename,
            "extracted_text": extracted_text,
            "status": "success"
        }
    except Exception as e:
        return {
            "error": f"Erro ao processar a imagem: {str(e)}",
            "status": "error"
        }

