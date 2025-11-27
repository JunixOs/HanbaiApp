from src.data_access_layer.repositories.interfaces.ICategoriaRepository import ICategoriaRepository
from src.data_access_layer.models.CategoriaModel import CategoriaModel

from sqlalchemy.orm import Session
from typing import List

class CategoriaRepository(ICategoriaRepository):

    __session_local_hanbai_db: Session

    def __init__(self , session_local_hanbai_db: Session) -> None:
        self.__session_local_hanbai_db = session_local_hanbai_db

    def findAll(self) -> List[CategoriaModel]:
        return self.__session_local_hanbai_db.query(CategoriaModel).all()
    
    def findById(self , id_categoria: str) -> CategoriaModel | None:
        return self.__session_local_hanbai_db.query(CategoriaModel).filter_by(id_categoria=id_categoria).first()
    
    def save(self, categoria_model: CategoriaModel) -> None:
        self.__session_local_hanbai_db.add(categoria_model)