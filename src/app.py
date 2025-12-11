import sys
import os

# Configuración de rutas
current_dir = os.path.abspath(os.path.dirname(__file__))
# Asegurar que la raíz del proyecto está en el path
sys.path.insert(0, os.path.dirname(current_dir))

from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from src.front_layer.controllers.HomeController import home_controller
from src.front_layer.controllers.module_gestion_usuarios.UsuarioController import usuario_controller
from src.front_layer.controllers.module_gestion_usuarios.RolController import rol_controller
from src.front_layer.controllers.module_gestion_productos.ProductoController import producto_controller

from src.data_access_layer.session import get_db_session
from src.data_access_layer.models.UsuarioModel import UsuarioModel

static_path = os.path.join(current_dir, 'front_layer', 'static')
template_path = os.path.join(current_dir, 'front_layer', 'templates')

hanbai_main_app = Flask(
    __name__,
    static_folder=static_path,
    static_url_path='/static',
    template_folder=template_path
)

hanbai_main_app.secret_key = "190106_abc"

# Registro de Blueprints
hanbai_main_app.register_blueprint(home_controller)
hanbai_main_app.register_blueprint(usuario_controller, url_prefix="/gestion_usuarios/usuario")
hanbai_main_app.register_blueprint(rol_controller, url_prefix="/gestion_usuarios/rol")
hanbai_main_app.register_blueprint(producto_controller, url_prefix="/gestion_productos/producto")

# Configuración Login
login_manager = LoginManager()
login_manager.init_app(hanbai_main_app)
login_manager.login_view = 'usuario.LoginUsuarioGet'

@login_manager.user_loader
def load_user(user_id):
    from uuid import UUID
    from src.bussines_layer.models.UsuarioLogin import UsuarioLogin
    from src.data_access_layer.models.RolModel import RolModel
    
    with get_db_session() as session:
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            return None

        usuario_model = session.query(UsuarioModel).get(user_uuid)
        
        if not usuario_model:
            return None

        # Recuperar el nombre del rol de forma segura
        nombre_rol = "SIN_ROL"
        if usuario_model.rol_id:
            # Intentamos acceder a la relación si está cargada
            if hasattr(usuario_model, 'rol') and usuario_model.rol:
                nombre_rol = usuario_model.rol.nombre
            else:
                # Si no, buscamos manualmente
                rol_obj = session.query(RolModel).get(usuario_model.rol_id)
                if rol_obj:
                    nombre_rol = rol_obj.nombre

        usuario_login = UsuarioLogin()
        usuario_login.id_usuario = str(usuario_model.id_usuario)
        usuario_login.nombre = usuario_model.nombre
        usuario_login.correo = usuario_model.correo
        usuario_login.dni = usuario_model.dni
        usuario_login.rol_id = str(usuario_model.rol_id)
        usuario_login.rol_name = nombre_rol 

        return usuario_login

# Ruta Raíz
@hanbai_main_app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('producto.index'))
    return redirect(url_for('usuario.LoginUsuarioGet'))

# Comando Seed Mejorado
@hanbai_main_app.cli.command("seed")
def seed():
    """Inserta o repara datos de prueba."""
    import uuid
    from sqlalchemy import or_ # Importación necesaria para la corrección
    from src.bussines_layer.services.module_gestion_usuarios.BcryptService import BcryptService
    from src.data_access_layer.models.RolModel import RolModel
    from src.data_access_layer.models.UsuarioModel import UsuarioModel
    # Importar modelos extra para evitar errores de mapper
    from src.data_access_layer.models.VentaModel import VentaModel
    from src.data_access_layer.models.EstadoVentaModel import EstadoVentaModel
    from src.data_access_layer.models.ComprobanteModel import ComprobanteModel 

    with get_db_session() as session:
        print("--- Iniciando Seed ---")
        
        # 1. ROLES
        roles_data = [
            ("ADMINISTRADOR", "Acceso total"), 
            ("ENCARGADO_DE_TIENDA", "Gestión"), 
            ("CLIENTE", "Usuario final")
        ]
        roles_dict = {}

        for nombre, descripcion in roles_data:
            rol = session.query(RolModel).filter_by(nombre=nombre).first()
            if not rol:
                rol = RolModel(id_rol=uuid.uuid4(), nombre=nombre, descripcion=descripcion)
                session.add(rol)
                session.commit()
                print(f"[+] Rol creado: {nombre}")
            else:
                print(f"[OK] Rol existe: {nombre}")
            roles_dict[nombre] = rol

        # 2. USUARIOS
        usuarios_data = [
            ("Admin Principal", "admin@demo.com", "12345678", "00000000", "ADMINISTRADOR"),
            ("Encargado Tienda", "encargado@demo.com", "12345678", "10101010", "ENCARGADO_DE_TIENDA"),
            ("Cliente Demo", "cliente@demo.com", "12345678", "11111111", "CLIENTE")
        ]

        for nombre, correo, password, dni, rol_nom in usuarios_data:
            # CORRECCIÓN: Buscamos por Correo O DNI para evitar conflicto de Unique Key
            user = session.query(UsuarioModel).filter(
                or_(UsuarioModel.correo == correo, UsuarioModel.dni == dni)
            ).first()

            if not user:
                # Crear nuevo usuario si no existe ni el correo ni el DNI
                if rol_nom in roles_dict:
                    user = UsuarioModel(
                        id_usuario=uuid.uuid4(),
                        nombre=nombre,
                        correo=correo,
                        dni=dni,
                        password_hash=BcryptService.HashPassword(password),
                        rol_id=roles_dict[rol_nom].id_rol
                    )
                    session.add(user)
                    session.commit()
                    print(f"[+] Usuario creado: {correo}")
            else:
                # Si existe (por correo o DNI), ACTUALIZAMOS sus datos para que coincidan con el seed
                if rol_nom in roles_dict:
                    user.nombre = nombre
                    user.correo = correo
                    user.dni = dni
                    user.rol_id = roles_dict[rol_nom].id_rol
                    # Opcional: Actualizar contraseña si quieres resetearla siempre
                    # user.password_hash = BcryptService.HashPassword(password)
                    session.commit()
                    print(f"[^] Usuario actualizado/corregido: {correo}")

        print("--- Seed Finalizado con Éxito ---")

if __name__ == "__main__":
    hanbai_main_app.run(debug=True, use_reloader=True, host='127.0.0.1', port=5000)