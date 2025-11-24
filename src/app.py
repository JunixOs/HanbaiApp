import sys
import os

# Obtener la ruta de este archivo (que está en src/)
current_dir = os.path.abspath(os.path.dirname(__file__))

# Agregar el directorio actual (src) al path para importar módulos
sys.path.insert(0, current_dir)

from flask import Flask
from front_layer.controllers.home_controller import home
from front_layer.controllers.users_controller import users
from front_layer.controllers.products_controller import products_bp

# Construir rutas apuntando a front_layer/
static_path = os.path.join(current_dir, 'front_layer', 'static')
template_path = os.path.join(current_dir, 'front_layer', 'templates')

# Configurar Flask
hanbai_main_app = Flask(
    __name__,
    static_folder=static_path,
    static_url_path='/static',
    template_folder=template_path
)

# Registrar blueprints
hanbai_main_app.register_blueprint(home)
hanbai_main_app.register_blueprint(users, url_prefix="/users")
hanbai_main_app.register_blueprint(products_bp, url_prefix="/products")

if __name__ == "__main__":
    hanbai_main_app.run(
        debug=True,
        use_reloader=True,
        host='127.0.0.1',
        port=5000
    )