from ..services.db_services import DbServices
from typing import Generic, TypeVar, List, Optional, Type
from abc import ABC
from sqlmodel import Session, select, func
from sqlalchemy.orm import joinedload
from datetime import date

# Tipo genérico T para trabajar con diferentes tipos de modelos en la base de datos
T = TypeVar('T')

# Clase base que proporciona operaciones CRUD para interactuar con cualquier modelo que se le pase
# Permite realizar operaciones sobre cualquier entidad, sin necesidad de duplicar código.


class BaseRepository(ABC, Generic[T]):
    item: Type[T]  # El tipo de modelo (entidad) con el que se va a trabajar

    def __init__(self):
        # Instancia del servicio de base de datos
        self._db_services = DbServices()

     # Método para crear un nuevo registro en la base de datos
    def create(self, item: T) -> T:
        with Session(self._db_services.get_engine()) as session:
            session.add(item)
            session.commit()
            session.refresh(item)
        return item

    # Método para leer todos los registros del modelo (tabla)
    def read(self) -> List[T]:
        with Session(self._db_services.get_engine()) as session:
            statement = select(self.item)
            results = session.exec(statement)
            items = results.all()
        return items

    # Método para leer un registro por su id
    def read_by_id(self, id: int) -> Optional[T]:
        with Session(self._db_services.get_engine()) as session:
            statement = select(self.item).where(self.item.user_id == id)
            result = session.exec(statement)
            item = result.one_or_none()

        return item

    def get_total_items(self, id: int) -> int:
        with Session(self._db_services.get_engine()) as session:
            statement = select(func.count()).where(self.item.user_id == id)
            # Esto debería devolver un valor entero, no una tupla
            result = session.exec(statement).first()
        return result if result is not None else 0  # Retorna directamente el resultado

    # Método para actualizar un registro existente por su id
    def update(self, id: int, update_item: T) -> Optional[T]:
        with Session(self._db_services.get_engine()) as session:
            statement = select(self.item).where(self.item.id == id)
            result = session.exec(statement)
            item = result.one_or_none()

            if item:
                for key, value in update_item.dict(exclude_unset=True).items():
                    setattr(item, key, value)

                session.add(item)
                session.commit()
                session.refresh(item)
            return item

    def delete(self, id: int):
        with Session(self._db_services.get_engine()) as session:
            statement = select(self.item).where(self.item.id == id)
            result = session.exec(statement)
            item = result.one_or_none()
            if item:
                session.delete(item)
                session.commit()


    def get_items_paginated_with_total(
        self,
        offset: int,
        limit: int,
        filters: Optional[list] = None
    ) -> tuple[list[T], int]:
        with Session(self._db_services.get_engine()) as session:
            # 1. Armo el statement con los filtros (sin paginar)
            base_statement = select(self.item)
            if filters:
                base_statement=base_statement.where(*filters)
            
            base_statement = base_statement.order_by(self.item.due_date.asc())

            # 2. Calculo el total (sin paginar)
            total = session.exec(
                select(func.count()).select_from(base_statement.subquery())
            ).one()

            # 3. Aplico la paginación por separado
            paginated_statement = base_statement.offset(offset).limit(limit)
            items = session.exec(paginated_statement).all()

            return items, total


    def get_items_by_user_id(self, user_id: int) -> List[T]:
        with Session(self._db_services.get_engine()) as session:
            statement = select(self.item).where(self.item.user_id == user_id)
            results = session.exec(statement)
            items = results.all()
        return items
    
    
    def count_items(self, user_id:int):
        with Session(self._db_services.get_engine()) as session:
            statement = (
                select(func.count())
                .select_from(self.item)
                .where(self.item.user_id == user_id)
            )

            result = session.exec(statement).one()
            return result if isinstance(result, int) else result[0]
