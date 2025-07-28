from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from aprendendo_fastapi.dependencies import pegar_sessao, verificar_token
from aprendendo_fastapi.schemas import PedidoSchema
from aprendendo_fastapi.models import Pedido, Usuario

order_router = APIRouter(
    prefix="/order", tags=["order"], dependencies=[Depends(verificar_token)]
)


@order_router.get("/")
async def pedidos():
    return {"mensagem": "Você acessou a rota de pedidos!"}


@order_router.post("/pedido")
async def criar_pedido(
    pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)
):
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do Pedido {novo_pedido.id}"}


@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(
    id_pedido: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(
            status_code=401, detail="Você não tem autorização para isso"
        )
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido numero {pedido.id} cancelado com sucesso",
        "pedido": pedido,
    }
