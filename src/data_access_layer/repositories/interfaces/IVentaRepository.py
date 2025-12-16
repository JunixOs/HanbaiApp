from abc import ABC, abstractmethod
from typing import List
from src.data_access_layer.models.VentaModel import VentaModel

class IVentaRepository(ABC):

    @abstractmethod
    def findAll(self) -> List[VentaModel]:
        pass

    @abstractmethod
    def findById(self, id_venta: str) -> VentaModel:
        pass

    @abstractmethod
    def findByUsuario(self, usuario_id: str) -> List[VentaModel]:
        pass

    @abstractmethod
    def save(self, venta: VentaModel) -> None:
        pass

    @abstractmethod
    def delete(self, venta: VentaModel) -> None:
        pass

    # --- FILTRADO PARA HISTORIAL / ADMIN ---
    @abstractmethod
    def find_with_filters(
        self,
        usuario_id: str = None,
        estado_venta_id: str = None
    ) -> List[VentaModel]:
        pass
