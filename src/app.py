from flask import Flask
from flask_login import LoginManager
from src.front_layer.controllers.HomeController import home_controller
from front_layer.controllers.module_gestion_usuarios.UsuarioController import usuario_controller
from front_layer.controllers.module_gestion_usuarios.RolController import rol_controller

from data_access_layer.session import get_db_session

hanbai_main_app = Flask(__name__)

# Aqui registro el controller para home
hanbai_main_app.register_blueprint(home_controller)

# Aqui registro el controller para users pero cada ruta que ella cree tendra el prefijo "users"
hanbai_main_app.register_blueprint(usuario_controller , url_prefix = "/gestion_usuarios/usuario")
hanbai_main_app.register_blueprint(rol_controller , url_prefix = "/gestion_usuarios/rol")

login_manager = LoginManager()

login_manager.init_app(hanbai_main_app)
login_manager.login_view = 'login' # type: ignore

@login_manager.user_loader
def load_user(user_id):
    from src.data_access_layer.models.UsuarioModel import UsuarioModel
    from src.data_access_layer.session import get_db_session

    with get_db_session() as session:
        # user_id viene como string → lo convertimos a UUID
        from uuid import UUID
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return None

        usuario = session.get(UsuarioModel, user_uuid)
        return usuario

if(__name__ == "__main__"):
    hanbai_main_app.run(debug=True)