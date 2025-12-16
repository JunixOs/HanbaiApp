from abc import ABC, abstractmethod
from src.data_access_layer.models.VentaModel import VentaModel
from src.bussines_layer.models.VentaDomainEntity import VentaDomainEntity

class IVentaMapper(ABC):

    @abstractmethod
    def toORM(self, domain_entity: VentaDomainEntity) -> VentaModel:
        pass

    @abstractmethod
    def toDomain(self, model: VentaModel) -> VentaDomainEntity:
        pass
