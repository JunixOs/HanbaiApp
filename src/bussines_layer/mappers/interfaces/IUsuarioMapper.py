from src.data_access_layer.models.UsuarioModel import UsuarioModel
from src.bussines_layer.models.UsuarioDomainEntity import UsuarioDomainEntity

from abc import ABC, abstractmethod


class IUsuarioMapper(ABC):

    @staticmethod       
    @abstractmethod     
    def toORM(usuario_domain_etity: UsuarioDomainEntity) -> UsuarioModel:
        pass

    @staticmethod      
    @abstractmethod     
    def toDomain(usuario_model: UsuarioModel) -> UsuarioDomainEntity:
        pass