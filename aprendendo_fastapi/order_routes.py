from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from aprendendo_fastapi.dependencies import pegar_sessao
from aprendendo_fastapi.schemas import PedidoSchema
from aprendendo_fastapi.models import Pedido

order_router = APIRouter(prefix="/order", tags=["order"])


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
    return {
        "mensagem": f"Pedido criado com sucesso para o usuário {pedido_schema.id_usuario}"
    }
