from src.data_access_layer.models.UsuarioModel import UsuarioModel
from src.bussines_layer.models.UsuarioDomainEntity import UsuarioDomainEntity

from abc import ABC, abstractmethod


class IUsuarioMapper(ABC):

    @abstractmethod
    @staticmethod
    def toORM(usuario_domain_entity: UsuarioDomainEntity) -> UsuarioModel:
        pass

    @abstractmethod
    @staticmethod
    def toDomain(usuario_model: UsuarioModel) -> UsuarioDomainEntity:
        pass