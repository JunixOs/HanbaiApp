from src.data_access_layer.models.UsuarioModel import UsuarioModel
from src.bussines_layer.models.UsuarioDomainEntity import UsuarioDomainEntity

from abc import ABC, abstractmethod


class IUsuarioMapper(ABC):

    @abstractmethod
    def toORM(self, usuario_domain_etity: UsuarioDomainEntity) -> UsuarioModel:
        pass

    @abstractmethod
    def toDomain(self, usuario_model: UsuarioModel) -> UsuarioDomainEntity:
        pass