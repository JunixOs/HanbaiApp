from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import desc

# Interfaces y Modelos
from src.data_access_layer.repositories.interfaces.IVentaRepository import IVentaRepository
from src.data_access_layer.models.VentaModel import VentaModel
from src.data_access_layer.models.UsuarioModel import UsuarioModel
from src.data_access_layer.models.EstadoVentaModel import EstadoVentaModel
from src.data_access_layer.models.ComprobanteModel import ComprobanteModel

class VentaRepository(IVentaRepository):
    def __init__(self, session: Session):
        self.session = session

    def findAll(self) -> List[VentaModel]:
        # Hacemos Join con Comprobante para ordenar por fecha real
        return (
            self.session.query(VentaModel)
            .join(ComprobanteModel)
            .order_by(desc(ComprobanteModel.fecha_venta))
            .all()
        )

    def findById(self, id_venta: str) -> VentaModel:
        try:
            uuid_obj = UUID(id_venta)
            return self.session.query(VentaModel).filter_by(id_venta=uuid_obj).first()
        except ValueError:
            return None

    # CORREGIDO: El nombre es findByUsuario (sin Id al final)
    def findByUsuario(self, usuario_id: str) -> List[VentaModel]:
        try:
            uuid_user = UUID(usuario_id)
            return (
                self.session.query(VentaModel)
                .join(ComprobanteModel)
                .filter(VentaModel.usuario_id == uuid_user)
                .order_by(desc(ComprobanteModel.fecha_venta))
                .all()
            )
        except ValueError:
            return []

    def save(self, venta: VentaModel) -> None:
        self.session.add(venta)
        self.session.commit()

    def delete(self, venta: VentaModel) -> None:
        self.session.delete(venta)
        self.session.commit()

    def find_with_filters(self, cliente_nombre: str = None, estado_id: str = None) -> List[VentaModel]:
        # Iniciamos query base uniendo tablas necesarias
        query = self.session.query(VentaModel).join(UsuarioModel).join(EstadoVentaModel)

        # Filtro por Nombre parcial (case insensitive)
        if cliente_nombre:
            query = query.filter(UsuarioModel.nombre.ilike(f"%{cliente_nombre}%"))

        # Filtro por Estado (UUID exacto)
        if estado_id and estado_id != "todos":
            try:
                uuid_estado = UUID(estado_id)
                query = query.filter(VentaModel.estado_venta_id == uuid_estado)
            except ValueError:
                pass 

        # Ordenar por fecha
        return query.join(ComprobanteModel).order_by(desc(ComprobanteModel.fecha_venta)).all()