from src.data_access_layer.base import Base

import uuid
from sqlalchemy import (
    Column , String , TIMESTAMP , Numeric , func , ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class VentaModel(Base):
    __tablename__ = "venta"

    id_venta = Column(
        UUID(as_uuid=True) ,
        primary_key=True ,
        default=uuid.uuid4 , 
        nullable=False , 
        name="id_venta"
    )

    fecha = Column(
        TIMESTAMP(timezone=True) , 
        name="fecha" , 
        server_default=func.now() , 
        nullable=False 
    )

    total = Column(
        Numeric(14 , 4) ,
        name="total" ,
        nullable=False
    )

    estado_venta_id = Column(
        UUID(as_uuid=True) , 
        ForeignKey("estado_venta.id_estado_venta") , 
        name="estado_venta_id",
        nullable=False
    )
    estado_venta = relationship(
        "EstadoVentaModel" , 
        back_populates="venta" , 
        uselist=False
    )

    usuario_id = Column(
        UUID(as_uuid=True) , 
        ForeignKey("usuario.id_usuario") ,
        name="usuario_id" ,
        nullable=False , 
    )
    usuario = relationship(
        "UsuarioModel" , 
        back_populates="venta" , 
        uselist=False
    )