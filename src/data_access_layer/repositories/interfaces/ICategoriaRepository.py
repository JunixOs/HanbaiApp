from src.data_access_layer.models.CategoriaModel import CategoriaModel

from abc import ABC , abstractmethod
from typing import List


class ICategoriaRepository(ABC):

    @abstractmethod
    def findAll(self) -> List[CategoriaModel]:
        pass

    @abstractmethod
    def findById(self , id_categoria) -> CategoriaModel | None:
        pass

    @abstractmethod
    def save(self , categoria_model: CategoriaModel) -> None:
        pass