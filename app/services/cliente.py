from .base import BaseService
from app.models.cliente import Cliente, Endereco
from sqlmodel import select
from fastapi import HTTPException

class EnderecoService(BaseService[Endereco]):
    def update(self, session, endereco_id, endereco_update, cliente_id):
        endereco = session.get(Endereco, endereco_id)
        if not endereco:
            raise HTTPException(status_code=404, detail="Endereço não encontrado")
        
        if endereco.cliente_id != cliente_id:
            raise HTTPException(status_code=403, detail="Acesso negado ao endereço")
        
        for key, value in endereco_update.items():
            if key == "atual" and value:
                # Se o endereço atualizado for marcado como atual, desmarcar os outros endereços do cliente
                session.exec(
                    select(Endereco)
                    .where(Endereco.cliente_id == cliente_id, Endereco.id != endereco_id)
                    .with_for_update(nowait=False)
                ).all()
                session.query(Endereco).filter(
                    Endereco.cliente_id == cliente_id, Endereco.id != endereco_id
                ).update({"atual": False}, synchronize_session=False)

            setattr(endereco, key, value)
        
        session.add(endereco)
        session.commit()
        session.refresh(endereco)
        return endereco


class ClienteService(BaseService[Cliente]):
    def autenticar(self, session, telefone):
        cliente = session.exec(select(Cliente).where(Cliente.telefone == telefone)).one_or_none()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        return cliente
    
    
cliente_service = ClienteService(Cliente)
endereco_service = EnderecoService(Endereco)