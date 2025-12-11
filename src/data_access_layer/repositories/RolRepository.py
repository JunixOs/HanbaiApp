from src.data_access_layer.repositories.interfaces.IRolRepository import IRolRepository
from src.data_access_layer.models.RolModel import RolModel
from typing import List
from sqlalchemy.orm import Session

class RolRepository(IRolRepository):
    __session_local_hanbai_db: Session

    def __init__(self , session_local_hanbai_db: Session) -> None:
        self.__session_local_hanbai_db = session_local_hanbai_db

    def findById(self , id_rol: str) -> RolModel | None:
        return self.__session_local_hanbai_db.query(RolModel).filter_by(id_rol = id_rol).first()

    def findAll(self) -> List[RolModel]:
        return self.__session_local_hanbai_db.query(RolModel).all()

    def deleteById(self , id_rol: str) -> None:
        rol_to_delete = self.__session_local_hanbai_db.query(RolModel).filter_by(id_rol = id_rol).first()
        if rol_to_delete:
            self.__session_local_hanbai_db.delete(rol_to_delete)

    def save(self , rol_model: RolModel) -> None:
        self.__session_local_hanbai_db.add(rol_model)
        self.__session_local_hanbai_db.commit()

    def findByNombre(self, rol_name: str) -> RolModel | None:
        # CORRECCIÓN: Agregar return
        return self.__session_local_hanbai_db.query(RolModel).filter_by(nombre = rol_name).first()