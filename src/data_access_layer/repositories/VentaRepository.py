from sqlalchemy.orm import Session
from src.data_access_layer.models.VentaModel import VentaModel
from src.data_access_layer.repositories.interfaces.IVentaRepository import IVentaRepository
from uuid import UUID

class VentaRepository(IVentaRepository):
    def __init__(self, session: Session):
        self._session = session

    def save(self, venta: VentaModel):
        self._session.add(venta)
        self._session.commit()
        self._session.refresh(venta)
        return venta

    def find_all(self):
        # Ordenar por fecha descendente si es posible
        return self._session.query(VentaModel).all()

    def find_by_id(self, id_venta: str):
        return self._session.query(VentaModel).filter_by(id_venta=UUID(id_venta)).first()