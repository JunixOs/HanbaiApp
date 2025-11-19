from src.data_access_layer.base import Base

import uuid
from sqlalchemy import (
    Column , String , TIMESTAMP , func , UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class FormatoReporteModel(Base):
    __tablename__ = "formato_reporte"

    id_formato_reporte = Column(
        UUID(as_uuid=True) , 
        primary_key=True , 
        default=uuid.uuid4 , 
        nullable=False
    )

    nombre = Column(
        String(100) , 
        name="nombre" , 
        nullable=False , 
        unique=True
    )

    creado_en = Column(
        TIMESTAMP(timezone=True) , 
        name="creado_en",
        server_default=func.now() , 
        nullable=False
    )

    actualizado_en = Column(
        TIMESTAMP(timezone=True) , 
        name="actualizado_en",
        server_default=func.now(),
        nullable=False
    )

    reporte = relationship(
        "ReporteModel" , 
        back_populates="formato_reporte"
    )

    __table_args__ = (
        UniqueConstraint("id_formato_reporte" , "nombre" , name="FormatoReporte_UQ"),
    )