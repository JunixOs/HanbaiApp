from abc import ABC, abstractmethod
from typing import List
from src.bussines_layer.models.VentaDomainEntity import VentaDomainEntity

class IVentaService(ABC):

    @abstractmethod
    def ListarTodas(self) -> List[VentaDomainEntity]:
        pass

    @abstractmethod
    def ListarPorUsuario(self, usuario_id) -> List[VentaDomainEntity]:
        pass

    @abstractmethod
    def RegistrarVenta(self, venta_dto: dict) -> None:
        pass
