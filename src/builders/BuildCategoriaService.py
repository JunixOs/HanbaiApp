from src.data_access_layer.repositories.CategoriaRepository import CategoriaRepository
from src.data_access_layer.repositories.interfaces.ICategoriaRepository import ICategoriaRepository
from src.data_access_layer.session import get_db_session

from src.bussines_layer.services.module_gestion_productos.CategoriaService import CategoriaService

class BuildCategoriaService:
    @staticmethod
    def build():
        with get_db_session() as session:
            categoria_repository: ICategoriaRepository = CategoriaRepository(session)

            return CategoriaService(categoria_repository)