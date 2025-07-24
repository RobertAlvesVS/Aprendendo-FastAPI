from fastapi import APIRouter, Depends, HTTPException
from aprendendo_fastapi.models import Usuario
from aprendendo_fastapi.dependencies import pegar_sessao
from sqlalchemy.orm import Session
from aprendendo_fastapi.main import bcrypt_context
from aprendendo_fastapi.schemas import LoginSchema, UsuarioSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])


def criar_token(email):
    token = f"awdhavdjavsdh{email}"
    return token


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
    usuario = session.query(Usuario).filter(Usuario.email == login_schema.email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    access_token = criar_token(usuario.id)
    return {"access_token": access_token, "token_type": "Bearer"}
