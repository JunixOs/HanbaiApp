from src.data_access_layer.base import Base
from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class DetalleVentaModel(Base):
    __tablename__ = "detalle_venta"

    # Clave compuesta o ID propio. Usaremos ID propio por simplicidad y escalabilidad.
    id_detalle = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    venta_id = Column(UUID(as_uuid=True), ForeignKey("venta.id_venta"), nullable=False)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("producto.id_producto"), nullable=False)
    
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False) # Guardamos el precio al momento de la venta
    subtotal = Column(Numeric(12, 2), nullable=False)

    # Relaciones
    venta = relationship("VentaModel", back_populates="detalles")
    producto = relationship("ProductoModel")