from abc import ABC, abstractmethod
from src.data_access_layer.models.VentaModel import VentaModel

class IVentaRepository(ABC):
    @abstractmethod
    def save(self, venta: VentaModel) -> VentaModel: pass
    @abstractmethod
    def find_all(self): pass
    @abstractmethod
    def find_by_id(self, id_venta: str): pass