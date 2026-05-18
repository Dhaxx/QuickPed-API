from fastapi import APIRouter, Depends, status, File, UploadFile, Request, HTTPException
from app.schemas.produto import ProdutoCreate, ProdutoRead, ProdutoUpdate
from app.services.produto import produto_service
from app.auth.admin.dependencies import get_current_estabelecimento, require_permission
from app.database.engine import get_session
from app.services.image_upload import ImageUploadService, get_image_upload_service
from pydantic import ValidationError
from decimal import Decimal
from typing import Optional

router = APIRouter()

# Resolvedor híbrido para ProdutoCreate (suporta JSON, Multipart ou URL-encoded)
async def get_produto_create_data(request: Request) -> ProdutoCreate:
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            body = await request.json()
            return ProdutoCreate(**body)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors())
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid JSON")
    elif "multipart/form-data" in content_type or "application/x-www-form-urlencoded" in content_type:
        try:
            form = await request.form()
            # Se enviaram em um único campo 'data' contendo JSON
            data_str = form.get("data")
            if data_str:
                return ProdutoCreate.model_validate_json(data_str)
            
            # Caso contrário, extrai cada campo individualmente
            nome = form.get("nome")
            preco_str = form.get("preco")
            categoria_id_str = form.get("categoria_id")
            descricao = form.get("descricao")
            imagem_url = form.get("imagem_url")
            produzido_por_str = form.get("produzido_por")
            imprime_str = form.get("imprime")
            
            # Validação de obrigatoriedade manual
            erros = []
            if nome is None:
                erros.append({"loc": ["body", "nome"], "msg": "Field required", "type": "missing"})
            if preco_str is None:
                erros.append({"loc": ["body", "preco"], "msg": "Field required", "type": "missing"})
            if categoria_id_str is None:
                erros.append({"loc": ["body", "categoria_id"], "msg": "Field required", "type": "missing"})
                
            if erros:
                raise HTTPException(status_code=422, detail=erros)
                
            imprime = None
            if imprime_str is not None:
                imprime = imprime_str.lower() in ("true", "1")
                
            return ProdutoCreate(
                nome=nome,
                preco=Decimal(preco_str),
                categoria_id=int(categoria_id_str),
                descricao=descricao,
                imagem_url=imagem_url,
                produzido_por=int(produzido_por_str) if produzido_por_str else None,
                imprime=imprime
            )
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors())
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid Form data: {str(e)}")
    else:
        raise HTTPException(status_code=415, detail="Unsupported media type")


# Resolvedor híbrido para ProdutoUpdate (suporta JSON, Multipart ou URL-encoded)
async def get_produto_update_data(request: Request) -> ProdutoUpdate:
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            body = await request.json()
            return ProdutoUpdate(**body)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors())
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid JSON")
    elif "multipart/form-data" in content_type or "application/x-www-form-urlencoded" in content_type:
        try:
            form = await request.form()
            # Se enviaram em um único campo 'data' contendo JSON
            data_str = form.get("data")
            if data_str:
                return ProdutoUpdate.model_validate_json(data_str)
                
            # Caso contrário, monta o dicionário com os campos presentes
            dados = {}
            if (nome := form.get("nome")) is not None:
                dados["nome"] = nome
            if (descricao := form.get("descricao")) is not None:
                dados["descricao"] = descricao
            if (preco_str := form.get("preco")) is not None:
                dados["preco"] = Decimal(preco_str)
            if (imagem_url := form.get("imagem_url")) is not None:
                dados["imagem_url"] = imagem_url
            if (categoria_id_str := form.get("categoria_id")) is not None:
                dados["categoria_id"] = int(categoria_id_str)
            if (ativo_str := form.get("ativo")) is not None:
                dados["ativo"] = ativo_str.lower() in ("true", "1")
            if (imprime_str := form.get("imprime")) is not None:
                dados["imprime"] = imprime_str.lower() in ("true", "1")
            if (produzido_por_str := form.get("produzido_por")) is not None:
                dados["produzido_por"] = int(produzido_por_str)
                
            return ProdutoUpdate(**dados)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors())
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid Form data: {str(e)}")
    else:
        raise HTTPException(status_code=415, detail="Unsupported media type")


# Rotas dos Produtos
@router.post("/", response_model=ProdutoRead, status_code=status.HTTP_201_CREATED)
async def create_produto(
    data: ProdutoCreate = Depends(get_produto_create_data), 
    imagem_file: Optional[UploadFile] = File(None),
    session = Depends(get_session), 
    estabelecimento_id: int = Depends(get_current_estabelecimento),
    image_upload_service: ImageUploadService = Depends(get_image_upload_service), 
    _=Depends(require_permission("produtos", "editar"))
):
    dados = data.model_dump()
    
    # Se houver upload de imagem binária, processa
    if imagem_file:
        dados["imagem_url"] = await image_upload_service.upload_image(imagem_file)
    
    # Remove o campo do arquivo temporário antes de persistir no banco
    if "imagem_file" in dados:
        del dados["imagem_file"]

    dados["estabelecimento_id"] = estabelecimento_id
    return produto_service.create(session, dados)


@router.get("/", response_model=list[ProdutoRead], status_code=status.HTTP_200_OK)
def get_produtos(
    session = Depends(get_session), 
    estabelecimento_id: int = Depends(get_current_estabelecimento), 
    _=Depends(require_permission("produtos", "visualizar"))
):
    return produto_service.get(session, estabelecimento_id)


@router.put("/", response_model=ProdutoRead, status_code=status.HTTP_200_OK)
async def update_produto(
    produto_id: int,
    data: ProdutoUpdate = Depends(get_produto_update_data),
    imagem_file: Optional[UploadFile] = File(None),
    session = Depends(get_session),
    estabelecimento_id: int = Depends(get_current_estabelecimento), 
    image_upload_service: ImageUploadService = Depends(get_image_upload_service),
    _=Depends(require_permission("produtos", "editar"))
):
    dados = data.model_dump(exclude_unset=True)
    
    # Se houver upload de imagem binária, processa
    if imagem_file:
        dados["imagem_url"] = await image_upload_service.upload_image(imagem_file)
    
    # Remove o campo do arquivo temporário se presente
    if "imagem_file" in dados:
        del dados["imagem_file"]

    return produto_service.update(session, produto_id, dados, estabelecimento_id)


@router.delete("/", response_model=ProdutoRead, status_code=status.HTTP_200_OK)
def delete_produto(
    produto_id: int, 
    session = Depends(get_session), 
    estabelecimento_id: int = Depends(get_current_estabelecimento), 
    _=Depends(require_permission("produtos", "editar"))
):
    return produto_service.delete(session, produto_id, estabelecimento_id)