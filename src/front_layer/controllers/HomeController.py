import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..' , '..' , '..')))

from flask import render_template , Blueprint
from flask_login import current_user

# Siempre construye la ruta desde la raiz del proyecto sin un "/" inicial
template_dir = os.path.abspath("src/front_layer/templates")

# Para trabajar por modulos puedo hacer esto
home_controller = Blueprint('home' , __name__ , template_folder=template_dir)

# Buenas practicas con render_template() y redirect()
# Redirect siempre con url_for() → nunca hardcodees rutas, así es más robusto.
# Render template si quieres mostrar un HTML con datos.
# String solo para respuestas simples o debug; evita en producción.
# Si tu función tiene varios return, cada camino debe retornar explícitamente, nunca solo ejecutar render_template

@home_controller.route("/")
def ShowHome():
    return render_template(
        "home.html" , 
        authenticated = current_user.is_authenticated
    )