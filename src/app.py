import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from flask import Flask
from flask_login import LoginManager

from src.front_layer.controllers.HomeController import home_controller
from src.front_layer.controllers.module_gestion_usuarios.UsuarioController import usuario_controller
from src.front_layer.controllers.module_gestion_usuarios.RolController import rol_controller
from src.front_layer.controllers.module_gestion_productos.products_controller import products_controller 

from src.data_access_layer.session import get_db_session
from src.data_access_layer.models.UsuarioModel import UsuarioModel 
from uuid import UUID

static_path = os.path.join(current_dir, 'front_layer', 'static')
template_path = os.path.join(current_dir, 'front_layer', 'templates')

hanbai_main_app = Flask(
    __name__,
    static_folder=static_path,
    static_url_path='/static',
    template_folder=template_path
)

hanbai_main_app.secret_key = 'super_secret_key_cambiar_en_produccion'

hanbai_main_app.register_blueprint(home_controller)
hanbai_main_app.register_blueprint(usuario_controller, url_prefix="/gestion_usuarios/usuario")
hanbai_main_app.register_blueprint(rol_controller, url_prefix="/gestion_usuarios/rol")
hanbai_main_app.register_blueprint(products_controller, url_prefix="/gestion_productos/producto")

login_manager = LoginManager()
login_manager.init_app(hanbai_main_app)
login_manager.login_view = 'usuario.LoginPage'

@login_manager.user_loader
def load_user(user_id):
    with get_db_session() as session:
        try:
            user_uuid = UUID(user_id)
            usuario = session.get(UsuarioModel, user_uuid)
            # Si necesitas usar el objeto fuera de la sesión, podrías necesitar:
            # session.expunge(usuario) 
            return usuario
        except ValueError:
            return None

if __name__ == "__main__":
    hanbai_main_app.run(
        debug=True,
        use_reloader=True,
        host='127.0.0.1',
        port=5000
    )