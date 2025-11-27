from src.data_access_layer.models.CategoriaModel import CategoriaModel
from src.bussines_layer.models.CategoriaDomainEntity import CategoriaDomainEntity

from abc import ABC, abstractmethod

class ICategoriaMapper(ABC):

    @abstractmethod
    @staticmethod
    def toORM(categoria_domain_entity: CategoriaDomainEntity) -> CategoriaModel:
        pass
    
    @abstractmethod
    @staticmethod
    def toDomain(categoria_model: CategoriaModel) -> CategoriaDomainEntity:
        pass