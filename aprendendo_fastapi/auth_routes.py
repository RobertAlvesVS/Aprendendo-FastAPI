from fastapi import APIRouter, Depends, HTTPException
from aprendendo_fastapi.models import Usuario
from aprendendo_fastapi.dependencies import pegar_sessao
from sqlalchemy.orm import Session
from aprendendo_fastapi.main import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    bcrypt_context,
)
from aprendendo_fastapi.schemas import LoginSchema, UsuarioSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])


def criar_token(
    id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": id_usuario, "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_codificado


def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario


def verificar_token(token, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.id == 1).first()

    return usuario


@auth_router.get("/")
async def home():
    return {
        "mensagem": "Você acessou a rota padrão de autenticação",
        "autenticado": False,
    }


@auth_router.post("/criar_conta")
async def criar_conta(
    usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)
):
    usuario = (
        session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    )
    if usuario:
        raise HTTPException(status_code=400, detail="Usuário já existe com este email")
    senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
    novo_usuario = Usuario(
        nome=usuario_schema.nome, email=usuario_schema.email, senha=senha_criptografada
    )
    session.add(novo_usuario)
    session.commit()
    return {"mensagem": f"Usuário criado com sucesso {usuario_schema.email}"}


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(
            status_code=404, detail="Usuário não encontrado ou credenciais inválidas"
        )

    access_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id, timedelta(days=7))
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "refresh_token": refresh_token,
    }


@auth_router.get("/refresh")
async def use_refresh_token(token):
    usuario = verificar_token(token)
    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }
