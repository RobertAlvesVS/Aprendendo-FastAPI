from aprendendo_fastapi.main import ALGORITHM, SECRET_KEY, oauth2_schema
from aprendendo_fastapi.models import Usuario, db
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException
from jose import jwt, JWTError


def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


def verificar_token(
    token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)
):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Acesso Negado, Verifique a validade do Token"
        )
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Invalido")

    return usuario
