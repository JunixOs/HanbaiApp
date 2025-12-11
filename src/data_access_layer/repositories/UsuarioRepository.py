from src.data_access_layer.repositories.interfaces.IUsuarioRepository import IUsuarioRepository
from src.data_access_layer.models.UsuarioModel import UsuarioModel
from typing import List
from sqlalchemy.orm import Session

class UsuarioRepository(IUsuarioRepository):
    __session_local_hanbai_db: Session

    def __init__(self , session_local_hanbai_db: Session) -> None:
        self.__session_local_hanbai_db = session_local_hanbai_db

    def findByCorreo(self, correo: str) -> UsuarioModel | None:
        return self.__session_local_hanbai_db.query(UsuarioModel).filter_by(correo=correo).first()

    def findById(self, id_usuario: str) -> UsuarioModel | None:
        return self.__session_local_hanbai_db.query(UsuarioModel).filter_by(id_usuario=id_usuario).first()

    def findAll(self) -> List[UsuarioModel]:
        return self.__session_local_hanbai_db.query(UsuarioModel).all()

    def deleteById(self, id_usuario: str) -> None:
        usuario = self.findById(id_usuario)
        if usuario:
            self.__session_local_hanbai_db.delete(usuario)
            self.__session_local_hanbai_db.commit()

    def save(self, usuario_model: UsuarioModel) -> None:
        self.__session_local_hanbai_db.add(usuario_model)
        self.__session_local_hanbai_db.commit() # CORRECCIÓN: Agregado commit