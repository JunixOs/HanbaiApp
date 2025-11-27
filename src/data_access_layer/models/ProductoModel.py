from src.data_access_layer.base import Base
from src.data_access_layer.models.ComprobanteProductoModel import comprobante_producto
from src.data_access_layer.models.ComprobanteModel import ComprobanteModel 
from src.data_access_layer.models.CategoriaModel import CategoriaModel
# --------------------------

import uuid
from sqlalchemy import (
    Column , String , Text , Numeric , Integer , ForeignKey , UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class ProductoModel(Base):
    __tablename__ = "producto"

    id_producto = Column(
        UUID(as_uuid=True) , 
        name="id_producto",
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

    categoria_id = Column(
        UUID(as_uuid=True) , 
        ForeignKey("categoria.id_categoria" , ondelete="SET NULL") ,
        name="categoria_id" , 
        nullable=True
    )
    
    categoria = relationship(
        "CategoriaModel" ,
        back_populates="producto"
    )

    comprobante = relationship(
        "ComprobanteModel" , 
        secondary=comprobante_producto , 
        back_populates="producto" , 
        passive_deletes=True
    )

    __table_args__ = (
        UniqueConstraint("id_producto" , "nombre" , name="Producto_UQ"),
    )