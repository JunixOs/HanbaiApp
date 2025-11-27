import sys
import os

current_dir = os.path.abspath(os.path.dirname(__file__))

# Agregar el directorio actual (src) al path para importar módulos
sys.path.insert(0, current_dir)

from flask import Flask
from flask_login import LoginManager
from front_layer.controllers.HomeController import home_controller
from front_layer.controllers.module_gestion_usuarios.UsuarioController import usuario_controller
from front_layer.controllers.module_gestion_usuarios.RolController import rol_controller
from src.front_layer.controllers.module_gestion_productos.ProductoController import products_bp

from data_access_layer.session import get_db_session

static_path = os.path.join(current_dir, 'front_layer', 'static')
template_path = os.path.join(current_dir, 'front_layer', 'templates')

hanbai_main_app = Flask(
    __name__,
    static_folder=static_path,
    static_url_path='/static',
    template_folder=template_path
)

hanbai_main_app.secret_key = "190106_abc"

# Aqui registro el controller para home
hanbai_main_app.register_blueprint(home_controller)

# Aqui registro el controller para users pero cada ruta que ella cree tendra el prefijo "users"
hanbai_main_app.register_blueprint(usuario_controller , url_prefix = "/gestion_usuarios/usuario")
hanbai_main_app.register_blueprint(rol_controller , url_prefix = "/gestion_usuarios/rol")
hanbai_main_app.register_blueprint(products_bp, url_prefix="/gestion_productos")

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

        usuario_model = session.get(UsuarioModel, user_uuid)
        if not usuario_model:
            return None

        from src.bussines_layer.models.UsuarioLogin import UsuarioLogin
        usuario_login = UsuarioLogin()
        usuario_login.id_usuario = str(usuario_model.id_usuario) # type: ignore
        usuario_login.nombre = usuario_model.nombre # type: ignore
        usuario_login.correo = usuario_model.correo # type: ignore
        usuario_login.rol_id = str(usuario_model.rol_id) # type: ignore
        usuario_login.rol_name = usuario_model.rol.nombre

        return usuario_login

@hanbai_main_app.cli.command("seed")
def seed():
    """Inserta datos de prueba en las tablas rol y usuario sin duplicarlos."""
    import uuid
    from src.bussines_layer.services.module_gestion_usuarios.BcryptService import BcryptService
    from src.data_access_layer.session import get_db_session
    from src.data_access_layer.models.RolModel import RolModel
    from src.data_access_layer.models.UsuarioModel import UsuarioModel

    with get_db_session() as session:

        print("Insertando roles...")

        # Lista de roles a insertar
        roles_data = [
            ("ADMINISTRADOR", "Acceso total al sistema."),
            ("ENCARGADO_DE_TIENDA", "Gestiona inventarios y productos."),
            ("CLIENTE", "Cliente estándar sin permisos especiales.")
        ]

        roles_dict = {}

        for nombre, descripcion in roles_data:
            # Buscar si el rol ya existe
            rol = session.query(RolModel).filter_by(nombre=nombre).first()

            if not rol:
                rol = RolModel(
                    id_rol=uuid.uuid4(),
                    nombre=nombre,
                    descripcion=descripcion
                )
                session.add(rol)
                session.commit()
                print(f"Rol creado: {nombre}")
            else:
                print(f"Rol ya existía: {nombre}")

            roles_dict[nombre] = rol

        print("Insertando usuarios...")

        usuarios_data = [
            ("Admin Principal", "admin@demo.com", "12345678", "00000000", "ADMINISTRADOR"),
            ("Encargado de Tienda", "encargadotienda@demo.com", "12345678", "10101010", "ENCARGADO_DE_TIENDA"),
            ("Cliente", "cliente@demo.com", "12345678", "11111111", "CLIENTE")
        ]

        for nombre, correo, password, dni, rol_nombre in usuarios_data:

            # Buscar si ya existe un usuario con ese correo
            usuario = session.query(UsuarioModel).filter_by(correo=correo).first()

            if not usuario:
                usuario = UsuarioModel(
                    id_usuario=uuid.uuid4(),
                    nombre=nombre,
                    correo=correo,
                    dni=dni,
                    password_hash=BcryptService.HashPassword(password),
                    rol_id=roles_dict[rol_nombre].id_rol
                )
                session.add(usuario)
                session.commit()
                print(f"Usuario creado: {correo}")
            else:
                print(f"Usuario ya existía: {correo}")

        print("Datos insertados correctamente sin duplicar.")

if __name__ == "__main__":
    hanbai_main_app.run(
        debug=True,
        use_reloader=True,
        host='127.0.0.1',
        port=5000
    )