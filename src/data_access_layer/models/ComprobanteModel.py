from src.data_access_layer.base import Base
from src.data_access_layer.models.ComprobanteProductoModel import comprobante_producto
from src.data_access_layer.models.ComprobanteCargoModel import comprobante_cargo
from src.data_access_layer.models.VentaModel import VentaModel
from src.data_access_layer.models.CargoModel import CargoModel

import uuid
from sqlalchemy import (
    Column , String , ForeignKey , Numeric , TIMESTAMP , func , UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class ComprobanteModel(Base):
    __tablename__ = "comprobante"

    id_comprobante = Column(
        UUID(as_uuid=True) ,
        name="id_comprobante" ,
        primary_key=True ,
        default=uuid.uuid4 , 
        nullable=False
    )

    # Relacion con venta
    venta_id = Column(
        UUID(as_uuid=True) , 
        ForeignKey("venta.id_venta") , 
        name="venta_id" , 
        nullable=False
    )
    
    venta = relationship(
        "VentaModel" , 
        back_populates="comprobante"
    )

    total = Column(
        Numeric(14 , 5) , 
        name="total" , 
        nullable=True
    )

    fecha_venta = Column(
        TIMESTAMP(timezone=True) , 
        name="fecha_venta" , 
        nullable=True , 
        server_default=func.now()
    )

    lugar_venta = Column(
        String(100) , 
        name="lugar_venta" , 
        nullable=True , 
    )

    producto = relationship(
        "ProductoModel" , 
        secondary=comprobante_producto , 
        back_populates="comprobante"
    )

    cargo = relationship(
        "CargoModel" , 
        secondary=comprobante_cargo , 
        back_populates="comprobante"
    )

    __table_args__ = (
        UniqueConstraint("id_comprobante" , "venta_id" , name="Comprobante_UQ"),
    )