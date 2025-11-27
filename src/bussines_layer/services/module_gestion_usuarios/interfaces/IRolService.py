from src.bussines_layer.models.RolDomainEntity import RolDomainEntity

from abc import ABC, abstractmethod
from typing import List

class IRolService(ABC):

    @abstractmethod
    def CrearRol(self , rol_domain_entity: RolDomainEntity) -> None:
        pass

    @abstractmethod
    def EliminarRol(self , id_rol: str) -> bool:
        pass

    @abstractmethod
    def EditarRol(self , rol_domain_entity: RolDomainEntity) -> bool:
        pass

    @abstractmethod
    def VerTodosLosRoles(self) -> List[RolDomainEntity]:
        pass

    @abstractmethod
    def ObtenerRolPorId(self, id_rol: str) -> RolDomainEntity:
        pass

    @abstractmethod
    def ObtenerRolPorNombre(self , rol_name: str) -> RolDomainEntity:
        pass