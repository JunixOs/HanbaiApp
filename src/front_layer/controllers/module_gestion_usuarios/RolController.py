from src.builders.BuildUsuarioService import BuildUsuarioService
from src.front_layer.controllers.AuthByRol import roles_required
from src.builders.BuildRolService import BuildRolService
from src.bussines_layer.models.RolDomainEntity import RolDomainEntity

import os
from datetime import datetime

from flask import (
    render_template , Blueprint , request , redirect , url_for , flash
)
from flask_login import login_required , current_user

template_dir = os.path.abspath("src/front_layer/templates")

rol_controller = Blueprint('rol' , __name__ , template_folder=template_dir)

@rol_controller.get("/roles")
@roles_required("ADMINISTRADOR")
def VerTodosLosRoles():
    if(current_user.is_authenticated):

        rol_service = BuildRolService.build()

        list_roles = rol_service.VerTodosLosRoles()

        return render_template(
            "VerRoles.html" ,
            roles=list_roles
        )

    else:
        return render_template("login.html")
    
@rol_controller.post("/crear")
@roles_required("ADMINISTRADOR")
def CrearRol():
    if(current_user.is_authenticated):

        now_timestamp = datetime.now().timestamp()

        rol_service = BuildRolService.build()

        rol_domain_entity = RolDomainEntity()

        rol_domain_entity.nombre = request.form["nombre"]
        rol_domain_entity.descripcion = request.form["descripcion"]
        rol_domain_entity.creado_en = now_timestamp
        rol_domain_entity.actualizado_en = now_timestamp


        try:
            rol_service.CrearRol(
                rol_domain_entity
            )
        except Exception:
            flash("No se pudo registrar el rol" , "message")
        else:
            flash("Rol registrado con exito" , "message")
        return redirect("module_gestion_usuarios/CrearRol.html")

    else:
        return render_template("login.html")


@rol_controller.get("/editar/<str:id_rol>")
@roles_required("ADMINISTRADOR")
def EditarRolGet():
    if(current_user.is_authenticated):

        rol_service = BuildRolService.build()

        return render_template("module_gestion_usuarios/EditarRol.html")

    else:
        return render_template("login.html")