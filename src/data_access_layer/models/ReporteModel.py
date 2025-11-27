from src.data_access_layer.base import Base
from src.data_access_layer.models.RolReporteModel import rol_reporte
from src.data_access_layer.models.FormatoReporteModel import FormatoReporteModel

import uuid
from sqlalchemy import (
    Column , String , TIMESTAMP , func , ForeignKey , UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class ReporteModel(Base):
    __tablename__ = "reporte"

    id_reporte = Column(
        UUID(as_uuid=True) ,
        primary_key=True , 
        default=uuid.uuid4 , 
        nullable=False , 
        name="id_reporte"
    )

    nombre = Column(
        String(100) , 
        name="nombre" , 
        nullable=False , 
        unique=True , 
    )

    formato_archivo = Column(
        String(10) , 
        name="formato_archivo" , 
        nullable=False , 
    )

    periodo_persistencia = Column(
        TIMESTAMP(timezone=True) , 
        name="periodo_persistencia" , 
        server_default=func.now()
    )

    url = Column(
        String(200) , 
        name="url" , 
        nullable=False , 
        unique=True
    )

    formato_reporte_id = Column(
        UUID(as_uuid=True) , 
        ForeignKey("formato_reporte.id_formato_reporte") , 
        name="formato_reporte_id" , 
        nullable=False
    )

    formato_reporte = relationship(
        "FormatoReporteModel" , 
        back_populates="reporte"
    )

    rol = relationship(
        "RolModel" , 
        secondary=rol_reporte , 
        back_populates="reporte" , 
        passive_deletes=True
    )

    __table_args__ = (
        UniqueConstraint("id_reporte" , "nombre" , name="Reporte_UQ"),
    )