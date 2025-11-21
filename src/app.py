from flask import Flask
from front_layer.controllers.home_controller import home
from front_layer.controllers.users_controller import users
from front_layer.controllers.ventas_controller import ventas
from front_layer.controllers.products_controller import products

hanbai_main_app = Flask(__name__)

# Aqui registro el controller para home
hanbai_main_app.register_blueprint(home)

# Aqui registro el controller para users pero cada ruta que ella cree tendra el prefijo "users"
hanbai_main_app.register_blueprint(users , url_prefix = "/users")

hanbai_main_app.register_blueprint(ventas, url_prefix="/ventas")

hanbai_main_app.register_blueprint(products, url_prefix="/products")

if(__name__ == "__main__"):
    hanbai_main_app.run(debug=True)