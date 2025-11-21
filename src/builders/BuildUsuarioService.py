from src.bussines_layer.services.module_gestion_usuarios.UsuarioService import UsuarioService

from src.data_access_layer.repositories.interfaces.IUsuarioRepository import IUsuarioRepository
from src.data_access_layer.repositories.UsuarioRepository import UsuarioRepository

from src.data_access_layer.session import get_db_session

class BuildUsuarioService:

    @staticmethod
    def build() -> UsuarioService:
        with get_db_session() as session:
            usuario_repository: IUsuarioRepository = UsuarioRepository(session)

            return UsuarioService(
                usuario_repository
            )