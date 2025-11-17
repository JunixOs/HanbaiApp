from src.data_access_layer.base import Base

import uuid
from sqlalchemy import (
    Column , String , Text , Numeric , Integer , ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID

class ProductoModel(Base):
    __tablename__ = "producto"

    id_producto = Column(
        UUID(as_uuid=True) , 
        name="producto",
        primary_key=True ,
        default=uuid.uuid4 ,  
        nullable=False
    )

    nombre = Column(
        String(255) , 
        name="nombre" , 
        unique=True,
        nullable=False
    )

    descripcion = Column(
        Text , 
        name="descripcion" , 
        nullable=True
    )

    precio = Column(
        Numeric(8 , 2) , 
        name="precio" , 
        nullable=False
    )

    stock = Column(
        Integer , 
        name="stock" , 
        nullable=False
    )

    descuento_producto = Column(
        Numeric(5 , 2) , 
        name="descuento_producto" , 
        nullable=True
    )

    id_venta = Column(
        UUID(as_uuid=True) , 
        ForeignKey("venta.id_venta") ,
        name="id_venta" , 
        nullable=False
    )