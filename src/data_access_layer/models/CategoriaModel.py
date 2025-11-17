from src.data_access_layer.base import Base

import uuid
from sqlalchemy import (
    Column , Numeric , Text , String , UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID

class CategoriaModel(Base):
    __tablename__ = "categoria"

    id_categoria = Column(
        UUID(as_uuid=True),
        primary_key=True , 
        default=uuid.uuid4 , 
        name="id_categoria",
        nullable=False
    )

    nombre = Column(
        String(100) , 
        name="nombre" , 
        nullable=False , 
        unique=True
    )

    descuento_categoria = Column(
        Numeric(5 , 2) , 
        name="descuento_categoria" , 
        nullable=True , 
    )

    descripcion = Column(
        Text , 
        name="descripcion" , 
        nullable=True
    )

    __table_args__ = (
        UniqueConstraint("id_categoria" , "nombre" , name="Categoria_UQ")
    )