from src.data_access_layer.base import Base

import uuid
from sqlalchemy import (
    Column , String , Text , UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class EstadoVentaModel(Base):
    __tablename__ = "estado_venta"

    id_estado_venta = Column(
        UUID(as_uuid=True) ,
        name="id_estado_venta" ,
        primary_key=True , 
        default=uuid.uuid4 ,
        nullable=False , 
    )

    nombre = Column(
        String(100) , 
        name="nombre" , 
        nullable=False
    )

    descripcion = Column(
        Text , 
        name="descripcion",
        nullable=True
    )

    venta = relationship(
        "VentaModel" , 
        back_populates="estado_venta"
    )

    # Unique constraint
    __table_args__ = (
        UniqueConstraint("id_estado_venta" , "nombre" , name="EstadoVenta_UQ"),
    )