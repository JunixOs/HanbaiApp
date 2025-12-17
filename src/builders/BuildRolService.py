from src.data_access_layer.session import LocalSession
from src.data_access_layer.repositories.RolRepository import RolRepository
from src.bussines_layer.services.module_gestion_usuarios.RolService import RolService

class BuildRolService:
    @staticmethod
    def build():
        session = LocalSession()
        rol_repository = RolRepository(session)
        rol_service = RolService(rol_repository)
        return rol_service