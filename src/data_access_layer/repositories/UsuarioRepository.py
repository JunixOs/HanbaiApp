from src.data_access_layer.repositories.interfaces.IUsuarioRepository import IUsuarioRepository
from src.data_access_layer.models.UsuarioModel import UsuarioModel

from uuid import UUID
from sqlalchemy.orm import Session

class UsuarioRepository(IUsuarioRepository):

    __session_local_hanbai_db: Session

    def __init__(self , session_local_hanbai_db: Session) -> None:
        self.__session_local_hanbai_db = session_local_hanbai_db

    def findById(self , id_usuario: str) -> UsuarioModel:
        return self.__session_local_hanbai_db.query(UsuarioModel).filter_by(correo = UUID(id_usuario)).first()