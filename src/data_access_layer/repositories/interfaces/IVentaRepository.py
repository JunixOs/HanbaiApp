from abc import ABC, abstractmethod
from typing import List
from src.data_access_layer.models.VentaModel import VentaModel

class IVentaRepository(ABC):
    
    @abstractmethod
    def findAll(self) -> List[VentaModel]:
        """Obtiene todas las ventas."""
        pass

    @abstractmethod
    def findById(self, id_venta: str) -> VentaModel:
        """Busca una venta por ID."""
        pass

    @abstractmethod
    def findByUsuario(self, usuario_id: str) -> List[VentaModel]:
        """Busca ventas de un usuario específico."""
        pass

    @abstractmethod
    def save(self, venta: VentaModel) -> None:
        """Guarda una venta nueva."""
        pass

    @abstractmethod
    def delete(self, venta: VentaModel) -> None:
        """Elimina una venta."""
        pass

    @abstractmethod
    def find_with_filters(self, cliente_nombre: str = None, estado_id: str = None) -> List[VentaModel]:
        """Buscador avanzado para el Administrador."""
        pass