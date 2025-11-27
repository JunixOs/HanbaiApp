from src.data_access_layer.base import Base

from sqlalchemy import (
    Table , Column , ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID

comprobante_producto = Table(
    "comprobante_producto" , 
    Base.metadata , 
    Column(
        "producto_id" , 
        UUID(as_uuid=True) , 
        ForeignKey("producto.id_producto" , ondelete="CASCADE") , 
        primary_key=True ,
    ) , 
    Column(
        "comprobante_id" , 
        UUID(as_uuid=True) , 
        ForeignKey("comprobante.id_comprobante" , ondelete="CASCADE") , 
        primary_key=True ,
    )
)