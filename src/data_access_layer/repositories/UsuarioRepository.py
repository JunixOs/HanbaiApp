from src.data_access_layer.repositories.interfaces.IUsuarioRepository import IUsuarioRepository
from src.data_access_layer.models.UsuarioModel import UsuarioModel

from uuid import UUID
from sqlalchemy.orm import Session
from typing import List

class UsuarioRepository(IUsuarioRepository):

    __session_local_hanbai_db: Session

    def __init__(self , session_local_hanbai_db: Session) -> None:
        self.__session_local_hanbai_db = session_local_hanbai_db

    def findAll(self) -> List[UsuarioModel]:
        return self.__session_local_hanbai_db.query(UsuarioModel).all()

    def findById(self , id_usuario: str) -> UsuarioModel:
        return self.__session_local_hanbai_db.query(UsuarioModel).filter_by(correo = UUID(id_usuario)).first()
    
    def deleteById(self , id_usuario: str) -> None:

        usuario_to_delete: UsuarioModel = self.__session_local_hanbai_db.query(UsuarioModel).filter_by(id_usuario = id_usuario).first()

        if(usuario_to_delete == None):
            return

        self.__session_local_hanbai_db.delete(usuario_to_delete)

    def save(self , usuario_model: UsuarioModel) -> None:
        self.__session_local_hanbai_db.add(usuario_model)

    def findByCorreo(self , correo: str) -> UsuarioModel:
        return self.__session_local_hanbai_db.query(UsuarioModel).filter_by(correo = correo).first()