from src.bussines_layer.models.CategoriaDomainEntity import CategoriaDomainEntity

from abc import ABC, abstractmethod
from typing import List

class ICategoriaService(ABC):

    @abstractmethod
    def ObtenerTodo(self) -> List[CategoriaDomainEntity]:
        pass

    @abstractmethod
    def ObtenerPorId(self , id_categoria) -> CategoriaDomainEntity | None:
        pass

    @abstractmethod
    def RegistrarCategoria(self , categoria_domain_entity) -> None:
        pass