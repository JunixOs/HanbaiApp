from src.bussines_layer.models.UsuarioDomainEntity import UsuarioDomainEntity

from abc import ABC, abstractmethod
from typing import List , Tuple

class IUsuarioService(ABC):
    
    @abstractmethod
    def RegistrarUsuario(self, usuario_domain_entity: UsuarioDomainEntity) -> None:
        pass

    @abstractmethod
    def IniciarSesion(self , password: str , correo: str) -> Tuple[str , bool]:
        pass

    @abstractmethod
    def EliminarUsuario(self , usuario_id: str) -> bool:
        pass

    @abstractmethod
    def EditarUsuario(self , usuario_domain_entity: UsuarioDomainEntity) -> bool:
        pass

    @abstractmethod
    def VerTodosLosUsuarios(self) -> List[UsuarioDomainEntity]:
        pass

    @abstractmethod
    def ObtenerUsuarioPorId(self, id_usuario: str) -> UsuarioDomainEntity:
        pass