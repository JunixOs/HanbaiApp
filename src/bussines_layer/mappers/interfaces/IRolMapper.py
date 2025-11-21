from src.bussines_layer.models.RolDomainEntity import RolDomainEntity
from src.data_access_layer.models.RolModel import RolModel

from abc import ABC, abstractmethod


class IRolMapper(ABC):
    @abstractmethod
    @staticmethod
    def toORM(usuario_domain_etity: RolDomainEntity) -> RolModel:
        pass

    @abstractmethod
    @staticmethod
    def toDomain(usuario_model: RolModel) -> RolDomainEntity:
        pass