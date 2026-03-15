from typing import Type, TypeVar, Generic, Optional, List
from sqlmodel import Session, SQLModel, select

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchema = TypeVar("CreateSchema", bound=SQLModel)
UpdateSchema = TypeVar("UpdateSchema", bound=SQLModel)

class BaseService(Generic[ModelType, CreateSchema, UpdateSchema]):
    def __init__(self, model: type[ModelType], create_schema: type[CreateSchema], update_schema: type[UpdateSchema]):
        self.model = model
        self.create_schema = create_schema
        self.update_schema = update_schema


    def get(self, session: Session, obj_id: int) -> Optional[ModelType]:
        return session.get(self.model, obj_id)
    

    def get_all(self, session: Session) -> List[ModelType]:
        stmt = select(self.model)
        return session.exec(stmt).all() # type: ignore
    

    def create(self, session: Session, model_data: CreateSchema) -> ModelType:
        obj = self.model(**model_data.model_dump())

        session.add(obj)
        session.commit()
        session.refresh(obj)

        return obj
    
    
    def update(self, session: Session, obj_id: int, model_data: UpdateSchema) -> Optional[ModelType]:
        obj = session.get(self.model, obj_id)

        if not obj:
            return None
        
        data = model_data.model_dump(exclude_unset=True)

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