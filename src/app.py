import sys
import os

# 1. Configuración de rutas del sistema
current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(current_dir))

from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user

# 2. Importación de Controladores (Blueprints)
from src.front_layer.controllers.HomeController import home_controller
from src.front_layer.controllers.module_gestion_usuarios.UsuarioController import usuario_controller
from src.front_layer.controllers.module_gestion_usuarios.RolController import rol_controller
from src.front_layer.controllers.module_gestion_productos.ProductoController import producto_controller
from src.front_layer.controllers.module_gestion_ventas.VentaController import venta_controller

# 3. Importaciones de Base de Datos y Modelos necesarios para Login
from src.data_access_layer.session import get_db_session
from src.data_access_layer.models.UsuarioModel import UsuarioModel
from src.data_access_layer.models.RolModel import RolModel # Importamos RolModel para usarlo abajo

# Configuración de carpetas de plantillas y estáticos
static_path = os.path.join(current_dir, 'front_layer', 'static')
template_path = os.path.join(current_dir, 'front_layer', 'templates')

# 4. Inicialización de la APP
hanbai_main_app = Flask(
    __name__,
    static_folder=static_path,
    static_url_path='/static',
    template_folder=template_path
)

hanbai_main_app.secret_key = "190106_abc" # En producción, esto debería ir en un .env

# 5. Registro de Blueprints (Rutas)
hanbai_main_app.register_blueprint(home_controller)
hanbai_main_app.register_blueprint(usuario_controller, url_prefix="/gestion_usuarios/usuario")
hanbai_main_app.register_blueprint(rol_controller, url_prefix="/gestion_usuarios/rol")
hanbai_main_app.register_blueprint(producto_controller, url_prefix="/gestion_productos/producto")
hanbai_main_app.register_blueprint(venta_controller, url_prefix="/gestion_ventas/venta")

# 6. Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(hanbai_main_app)
# Si no está logueado, lo mandamos al Login (o podrías mandarlo al Home si prefieres)
login_manager.login_view = 'usuario.LoginUsuarioGet'

@login_manager.user_loader
def load_user(user_id):
    """Carga el usuario desde la BD para la sesión"""
    from uuid import UUID
    from src.bussines_layer.models.UsuarioLogin import UsuarioLogin
    
    with get_db_session() as session:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return None

        usuario_model = session.query(UsuarioModel).get(user_uuid)
        
        if not usuario_model:
            return None

        # Recuperar el nombre del rol
        nombre_rol = "SIN_ROL"
        if usuario_model.rol_id:
            # Intentamos usar la relación ORM primero
            if hasattr(usuario_model, 'rol') and usuario_model.rol:
                nombre_rol = usuario_model.rol.nombre
            else:
                # Fallback manual si la relación no cargó
                rol_obj = session.query(RolModel).get(usuario_model.rol_id)
                if rol_obj:
                    nombre_rol = rol_obj.nombre

        # Mapeamos al objeto de sesión (UsuarioLogin)
        usuario_login = UsuarioLogin()
        usuario_login.id_usuario = str(usuario_model.id_usuario)
        usuario_login.nombre = usuario_model.nombre
        usuario_login.correo = usuario_model.correo
        usuario_login.dni = usuario_model.dni
        usuario_login.rol_id = str(usuario_model.rol_id)
        usuario_login.rol_name = nombre_rol 

        return usuario_login

# 7. Ruta Principal (Raíz)
@hanbai_main_app.route('/')
def index():
    # CAMBIO IMPORTANTE:
    # Siempre redirigimos al Home Controller. 
    # El Home Controller decidirá si muestra la "Bienvenida" (invitado) o el "Dashboard" (usuario).
    return redirect(url_for('home.ShowHome'))

if __name__ == "__main__":
    hanbai_main_app.run(debug=True, use_reloader=True, host='127.0.0.1', port=5000)