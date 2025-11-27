import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..' , '..' , '..')))

from flask import render_template , Blueprint

# Siempre construye la ruta desde la raiz del proyecto sin un "/" inicial
template_dir = os.path.abspath("src/front_layer/templates")

# Para trabajar por modulos puedo hacer esto
home_controller = Blueprint('home' , __name__ , template_folder=template_dir)

@home_controller.route("/")
def ShowHome():
    return render_template("home.html")