from typing import Type, TypeVar, Generic, Optional, List
from sqlmodel import Session, SQLModel, select

ModelType = TypeVar("ModelType", bound=SQLModel)

class BaseService(Generic[ModelType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    def get(self, session: Session, obj_id: int) -> Optional[ModelType]:
        return session.get(self.model, obj_id)
    

    def get_all(self, session: Session, entidade_id: int) -> List[ModelType]:
        stmt = select(self.model).where(self.model.entidade_id == entidade_id)
        return session.exec(stmt).all() # type: ignore
    

    def create(self, session: Session, model_data: dict) -> ModelType:
        obj = self.model(**model_data)

        session.add(obj)
        session.commit()
        session.refresh(obj)

        return obj
    
    
    def update(self, session: Session, obj_id: int, model_data: dict) -> Optional[ModelType]:
        obj = session.get(self.model, obj_id)

        if not obj:
            return None
        
        data = model_data

        for column, value in data.items():
            setattr(obj, column, value)

        session.add(obj)
        session.commit()
        session.refresh(obj)

        return obj
    

    def delete(self, session: Session, obj_id: int) -> Optional[ModelType]:
        obj = session.get(self.model, obj_id)

        if not obj:
            return None
        
        session.delete(obj)
        session.commit()
        session.refresh(obj)

        return obj