from src.bussines_layer.services.module_gestion_usuarios.RolService import RolService

from src.data_access_layer.repositories.interfaces.IRolRepository import IRolRepository
from src.data_access_layer.repositories.RolRepository import RolRepository
from src.data_access_layer.session import get_db_session

class BuildRolService:

    @staticmethod
    def build() -> RolService:
        with get_db_session() as session:
            rol_repository: IRolRepository = RolRepository(session)

            return RolService(rol_repository)