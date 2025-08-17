from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import pytesseract
from PIL import Image
import io
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Cria a instância do FastAPI
app = FastAPI()

# Configuração do CORS
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

# Configuração do Banco de Dados PostgreSQL (Neon)
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de Dados do Carrinho
class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

# Cria a tabela no banco de dados se ela não existir
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota de teste
@app.get("/test")
async def test_connection():
    return {"message": "Backend do EconoShop está funcionando!"}

# Rota para processar a imagem com OCR
@app.post("/process-image")
async def process_image_with_ocr(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        pytesseract.pytesseract.tesseract_cmd = 'tesseract'
        extracted_text = pytesseract.image_to_string(image, lang='por')

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

# NOVO: Rota para adicionar um item ao carrinho
@app.post("/cart/add")
async def add_item_to_cart(user_id: str, name: str, price: float, db: Session = Depends(get_db)):
    db_item = CartItem(user_id=user_id, name=name, price=price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"message": "Item adicionado ao carrinho", "item": db_item}

# NOVO: Rota para carregar o carrinho de um usuário
@app.get("/cart/{user_id}")
async def get_user_cart(user_id: str, db: Session = Depends(get_db)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    return cart_items # CORREÇÃO: Retorna a lista diretamente, sem um objeto.

# NOVO: Rota para remover um item do carrinho
@app.delete("/cart/remove/{item_id}")
async def remove_item_from_cart(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado no carrinho")
    db.delete(db_item)
    db.commit()
    return {"message": "Item removido do carrinho"}