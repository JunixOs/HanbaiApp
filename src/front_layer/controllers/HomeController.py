from flask import render_template, Blueprint
from flask_login import current_user
# Importamos el constructor del servicio de productos
from src.builders.BuildProductoService import BuildProductoService

home_controller = Blueprint('home', __name__)

@home_controller.route("/")
def ShowHome():
    productos_destacados = []
    
    # Intentamos obtener productos reales de la Base de Datos
    try:
        producto_service = BuildProductoService.build()
        todos_productos = producto_service.ObtenerTodosLosProductos()
        
        # Si hay productos, tomamos los primeros 4 o 6 para mostrar
        if todos_productos:
            # Invertimos la lista [::-1] para mostrar los más nuevos primero
            productos_destacados = todos_productos[::-1][:6] 
            
    except Exception as e:
        print(f"Error cargando productos en Home: {e}")
        # Si falla (ej. tabla vacía), simplemente no mostramos nada, no rompe la app
        productos_destacados = []

    return render_template(
        "home.html", 
        authenticated=current_user.is_authenticated,
        productos=productos_destacados
    )