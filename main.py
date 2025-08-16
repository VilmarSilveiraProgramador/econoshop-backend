from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Cria a instância do FastAPI
app = FastAPI()

# Configuração do CORS (Cross-Origin Resource Sharing)
# ESSENCIAL para permitir que seu frontend React no Netlify
# se comunique com este backend.
origins = [
    # Adicione a URL do seu site no Netlify aqui.
    # Exemplo: https://prismatic-griffin-246daf.netlify.app
    "https://prismatic-griffin-246daf.netlify.app",
    # Adicione outras URLs de ambientes de teste se necessário
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
