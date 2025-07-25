from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Bem-vindo à API de Autenticação FastAPI"}
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from aprendendo_fastapi.order_routes import order_router
from aprendendo_fastapi.auth_routes import auth_router

app.include_router(auth_router)
app.include_router(order_router)
