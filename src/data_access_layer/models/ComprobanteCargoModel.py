from src.data_access_layer.base import Base

from sqlalchemy import (
    Column , ForeignKey , Table
)
from sqlalchemy.dialects.postgresql import UUID

comprobante_cargo = Table(
    "comprobante_cargo" , 
    Base.metadata , 
    Column(
        "comprobante_id" , 
        UUID(as_uuid=True) , 
        ForeignKey("comprobante.id_comprobante" , ondelete="CASCADE") , 
        primary_key=True
    ) , 
    Column(
        "cargo_id" , 
        UUID(as_uuid=True) , 
        ForeignKey("cargo.id_cargo" , ondelete="CASCADE") , 
        primary_key=True
    )
)