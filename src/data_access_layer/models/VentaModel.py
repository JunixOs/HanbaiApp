from src.data_access_layer.base import Base
import uuid
from sqlalchemy import Column, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class VentaModel(Base):
    __tablename__ = "venta"

    id_venta = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4, 
        nullable=False, 
        name="id_venta"
    )

    subtotal = Column(
        Numeric(14, 4),
        name="subtotal",
        nullable=False
    )

    # -----------------------------------------------------
    # RELACIÓN CON ESTADO DE VENTA
    # -----------------------------------------------------
    estado_venta_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("estado_venta.id_estado_venta"), 
        name="estado_venta_id",
        nullable=False
    )
    
    # Relación para acceder a: venta.estado_venta.nombre
    estado_venta = relationship("EstadoVentaModel")

    # -----------------------------------------------------
    # RELACIÓN CON USUARIO (CLIENTE)
    # -----------------------------------------------------
    usuario_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("usuario.id_usuario", ondelete="CASCADE"),
        name="usuario_id",
        nullable=False
    )
    
    # Relación para acceder a: venta.usuario.nombre
    usuario = relationship("UsuarioModel")

    # -----------------------------------------------------
    # RELACIÓN CON COMPROBANTE (1 a 1)
    # -----------------------------------------------------
    # back_populates requiere que en ComprobanteModel exista "venta = relationship(...)"
    comprobante = relationship(
        "ComprobanteModel", 
        back_populates="venta",
        cascade="all, delete",
        uselist=False
    )