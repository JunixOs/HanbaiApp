from abc import ABC, abstractmethod
from src.data_access_layer.models.ProductoModel import ProductoModel
from typing import List

class IProductoRepository(ABC):
    @abstractmethod
    def find_all(self) -> List[ProductoModel]: pass

    @abstractmethod
    def find_by_id(self, id_producto: str) -> ProductoModel: pass

    @abstractmethod
    def save(self, producto: ProductoModel) -> ProductoModel: pass

    @abstractmethod
    def update(self, producto: ProductoModel) -> ProductoModel: pass

    @abstractmethod
    def delete(self, producto: ProductoModel) -> None: pass