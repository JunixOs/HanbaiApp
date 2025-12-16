from uuid import UUID
from typing import List
from sqlalchemy.orm import Session

from src.data_access_layer.repositories.interfaces.IVentaRepository import IVentaRepository
from src.data_access_layer.models.VentaModel import VentaModel

class VentaRepository(IVentaRepository):
    def __init__(self, session: Session):
        self.session = session

    def findAll(self) -> List[VentaModel]:
        return self.session.query(VentaModel).all()

    def findById(self, id_venta: str) -> VentaModel:
        try:
            uuid_obj = UUID(id_venta)
            return (
                self.session
                .query(VentaModel)
                .filter_by(id_venta=uuid_obj)
                .first()
            )
        except ValueError:
            return None

    def findByUsuario(self, usuario_id: str) -> List[VentaModel]:
        try:
            uuid_user = UUID(usuario_id)
            return (
                self.session
                .query(VentaModel)
                .filter(VentaModel.usuario_id == uuid_user)
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

    def find_with_filters(
        self,
        usuario_id: str = None,
        estado_venta_id: str = None
    ) -> List[VentaModel]:

        query = self.session.query(VentaModel)

        if usuario_id:
            try:
                uuid_user = UUID(usuario_id)
                query = query.filter(VentaModel.usuario_id == uuid_user)
            except ValueError:
                pass

        if estado_venta_id:
            try:
                uuid_estado = UUID(estado_venta_id)
                query = query.filter(VentaModel.estado_venta_id == uuid_estado)
            except ValueError:
                pass

        return query.all()
