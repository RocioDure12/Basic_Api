from ..services.db_services import DbServices
from sqlmodel import Session, SQLModel,select
from ..models.role import Role
from typing import Optional


class RolesRepository:
    def __init__(self):
        self._db_services=DbServices()
        
    def create(self, item:Role):
        with Session(self._db_services.get_engine()) as session:
            session.add(item)
            session.commit()
            session.refresh(item)
        return item
            
    
    def read(self)->list[Role]:
        with Session(self._db_services.get_engine()) as session:
            statement = select(Role)
            results=session.exec(statement)
            roles=results.all()
        
        return roles
    
      
    def update(self,id:int,update_item:Role):
        with Session(self._db_services.get_engine()) as session:
            print("aca estoy")
            statement=select(Role).where(Role.id == id)
            result=session.exec(statement)
            role=result.one()
            role.name=update_item.name
            role.scopes=update_item.scopes
            role.is_admin=update_item.is_admin
    
            session.add(role)
            session.commit()
            session.refresh(role)
            
        return role
                    
            
    def delete(self,id:int):
        with Session(self._db_services.get_engine()) as session:
            statement=select(Role).where(Role.id == id)
            result=session.exec(statement)
            role=result.one()
            session.delete(role)
            session.commit()
      
            