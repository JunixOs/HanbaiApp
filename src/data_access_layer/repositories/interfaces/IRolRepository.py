from src.data_access_layer.models.RolModel import RolModel

from abc import ABC, abstractmethod
from typing import List

class IRolRepository(ABC):

    @abstractmethod
    def findById(self , id_rol: str) -> RolModel:
        pass

    @abstractmethod
    def findAll(self) -> List[RolModel]:
        pass

    @abstractmethod
    def deleteById(self , id_rol: str) -> None:
        pass

    @abstractmethod
    def save(self , rol_model: RolModel) -> None:
        pass