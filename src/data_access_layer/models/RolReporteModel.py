from src.data_access_layer.base import Base

from sqlalchemy import (
    Table , Column , ForeignKey , TIMESTAMP , func
)
from sqlalchemy.dialects.postgresql import UUID

rol_reporte = Table(
    "rol_reporte" , 
    Base.metadata , 
    Column(
        "reporte_id" , 
        UUID(as_uuid=True) , 
        ForeignKey("reporte.id_reporte") , 
        primary_key=True
    ),
    Column(
        "rol_id" , 
        UUID(as_uuid=True) , 
        ForeignKey("rol.id_rol") , 
        primary_key=True
    ) , 
    Column(
        "asignado_en" , 
        TIMESTAMP(timezone=True) , 
        server_default=func.now()
    )
)