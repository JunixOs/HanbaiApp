from abc import ABC, abstractmethod
from src.data_access_layer.models.ProductoModel import ProductoModel
from src.bussines_layer.models.ProductoDomainEntity import ProductoDomainEntity

class IProductoMapper(ABC):
    @abstractmethod
    def toORM(self, domain_entity: ProductoDomainEntity) -> ProductoModel:
        pass

    @abstractmethod
    def toDomain(self, model: ProductoModel) -> ProductoDomainEntity:
        pass