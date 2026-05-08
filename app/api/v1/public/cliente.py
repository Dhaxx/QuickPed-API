from fastapi import APIRouter, Depends, status
from app.models.cliente import Cliente
from app.schemas.cliente import (
    ClienteRead,
    ClienteUpdate,
    EnderecoCreate,
    EnderecoRead,
    EnderecoUpdate,
)
from app.services.cliente import cliente_service, endereco_service
from app.services.correios_client import buscar_cep
from app.database.engine import get_session
from app.auth.public.dependencies import get_current_cliente

router = APIRouter()


@router.get("/", response_model=ClienteRead, status_code=status.HTTP_200_OK)
def ler_cliente(cliente: Cliente = Depends(get_current_cliente)):
    return cliente


@router.put("/", response_model=ClienteRead, status_code=status.HTTP_200_OK)
def atualizar_cliente(
    cliente_update: ClienteUpdate,
    cliente: Cliente = Depends(get_current_cliente),
    session=Depends(get_session),
):
    return cliente_service.update(session, cliente.id, cliente_update)


@router.post(
    "/endereco", response_model=EnderecoRead, status_code=status.HTTP_201_CREATED
)
def adicionar_endereco_cliente(
    endereco: EnderecoCreate,
    cliente: Cliente = Depends(get_current_cliente),
    session=Depends(get_session),
):
    cliente_id = cliente.id
    dados_endereco = endereco.model_dump()
    dados_endereco["cliente_id"] = cliente_id
    return endereco_service.create(session, dados_endereco)


@router.put("/endereco/{endereco_id}", response_model=EnderecoRead, status_code=status.HTTP_200_OK)
def atualizar_endereco_cliente(
    endereco_id: int,
    endereco_update: EnderecoUpdate,
    cliente: Cliente = Depends(get_current_cliente),
    session=Depends(get_session),
):
    cliente_id = cliente.id
    dados_endereco = endereco_update.model_dump(exclude_unset=True)
    return endereco_service.update(session, endereco_id, dados_endereco, cliente_id)


@router.get("/endereco/buscar-cep/{cep}")
async def buscar_endereco_por_cep(cep: str):
    cep_limpo = cep.replace("-", "").replace(".", "")
    if len(cep_limpo) != 8:
        return {"error": "CEP inválido"}

    result = await buscar_cep(cep_limpo)
    if not result:
        return {"error": "CEP não encontrado"}

    return {
        "cep": result.cep,
        "logradouro": result.logradouro,
        "bairro": result.bairro,
        "cidade": result.cidade,
        "uf": result.uf,
    }
