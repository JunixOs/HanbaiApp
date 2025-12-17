from src.builders.BuildCategoriaService import BuildCategoriaService
from src.front_layer.controllers.AuthByRol import roles_required

from src.bussines_layer.models.CategoriaDomainEntity import CategoriaDomainEntity

import os
from flask import (
    Blueprint , request , flash , redirect , render_template
)
from flask_login import current_user

template_dir = os.path.abspath("src/front_layer/templates/module_gestion_productos")
categoria_producto_controller = Blueprint('categoria_productos' , __name__ , template_folder=template_dir)

@categoria_producto_controller.post("/crear")
# CAMBIO REALIZADO: Se agregan ambos roles al decorador
@roles_required("ENCARGADO_DE_TIENDA", "ADMINISTRADOR")
def CrearCategoriaProducto():
    if(current_user.is_authenticated):

        categoria_service = BuildCategoriaService.build()

        categoria_domain_entity = CategoriaDomainEntity()

        categoria_domain_entity.nombre = request.form["nombre"]
        categoria_domain_entity.descripcion = request.form["descripcion"]

        try:
            categoria_service.RegistrarCategoria(categoria_domain_entity)
        except Exception:
            flash("No se pudo registrar la categoria" , "message")
        else:
            flash("Categoria registrada con exito" , "message")

        return redirect("module_gestion_productos/list.html")

    else:
        return render_template("module_gestion_usuarios/login.html")