from src.data_access_layer.session import LocalSession
from src.data_access_layer.repositories.UsuarioRepository import UsuarioRepository
from src.bussines_layer.services.module_gestion_usuarios.UsuarioService import UsuarioService

class BuildUsuarioService:
    @staticmethod
    def build():
        # CORRECCIÓN: Usamos LocalSession() para obtener una sesión directa
        # en lugar de get_db_session() que es un context manager.
        session = LocalSession() 
        usuario_repository = UsuarioRepository(session)
        usuario_service = UsuarioService(usuario_repository)
        return usuario_service