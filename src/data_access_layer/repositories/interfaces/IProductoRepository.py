from abc import ABC, abstractmethod
from typing import List
from src.data_access_layer.models.ProductoModel import ProductoModel

class IProductoRepository(ABC):
    @abstractmethod
    def findAll(self) -> List[ProductoModel]:
        pass

    @abstractmethod
    def findById(self, id_producto: str) -> ProductoModel:
        pass

    @abstractmethod
    def save(self, producto: ProductoModel) -> None:
        pass

    @abstractmethod
    def delete(self, producto: ProductoModel) -> None:
        pass

    # --- NUEVO MÉTODO AGREGADO ---
    @abstractmethod
    def find_with_filters(self, nombre: str = None, categoria_id: str = None) -> List[ProductoModel]:
        pass