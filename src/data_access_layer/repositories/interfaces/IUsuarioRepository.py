from abc import ABC, abstractmethod

from src.data_access_layer.models.UsuarioModel import UsuarioModel
from typing import List

class IUsuarioRepository(ABC):

    @abstractmethod
    def findAll(self) -> List[UsuarioModel]:
        pass

    @abstractmethod
    def findById(self , id_usuario: str) -> UsuarioModel | None:
        pass

    @abstractmethod
    def deleteById(self , id_usuario: str) -> None:
        pass

    @abstractmethod
    def save(self , usuario_model: UsuarioModel) -> None:
        pass

    @abstractmethod
    def findByCorreo(self, correo: str) -> UsuarioModel | None:
        pass

    # Actualizar datos
    # with get_db_session() as db:
    #     usuario = db.query(UsuarioModel).filter_by(dni="12345678").first()
    #     
    #     if usuario:
    #         usuario.nombre = "Ana Actualizada"
    #         usuario.correo = "ana.nuevo@mail.com"
    #         # No necesitas db.add(usuario), SQLAlchemy detecta cambios automáticamente