from src.data_access_layer.base import Base
from src.data_access_layer.models.ComprobanteCargoModel import comprobante_cargo

from sqlalchemy import (
    Column , String , Numeric , Text , TIMESTAMP , func
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

class CargoModel(Base):
    __tablename__ = "cargo"

    id_cargo = Column(
        UUID(as_uuid=True) ,
        name="id_cargo", 
        primary_key=True , 
        default=func.now() , 
        nullable=False
    )

    nombre = Column(
        String(100) , 
        name="nombre" , 
        nullable=False
    )

    porcentaje_total = Column(
        Numeric(5 , 2) , 
        name="porcentaje_total",
        nullable=False , 
    )

    descripcion = Column(
        Text , 
        name="descripcion" , 
        nullable=True
    )

    creadoEn = Column(
        TIMESTAMP(timezone=True) , 
        server_default=func.now() , 
        name="creado_en" , 
        nullable=False
    )

    actualizadoEn = Column(
        TIMESTAMP(timezone=True) , 
        server_default=func.now() , 
        name="actualizado_en" , 
        nullable=False
    )

    comprobante = relationship(
        "ComprobanteModel" , 
        secondary=comprobante_cargo , 
        back_populates="cargo"
    )