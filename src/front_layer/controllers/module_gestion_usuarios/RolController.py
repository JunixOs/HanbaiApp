from src.builders.BuildRolService import BuildRolService
from src.bussines_layer.models.RolDomainEntity import RolDomainEntity
from src.front_layer.controllers.AuthByRol import roles_required

import os
from datetime import datetime

from flask import (
    render_template, Blueprint, request, redirect, url_for, flash
)
from flask_login import login_required, current_user

template_dir = os.path.abspath("src/front_layer/templates")
rol_controller = Blueprint('rol', __name__, template_folder=template_dir)

# ==============================================================================
# LISTADO (index)
# ==============================================================================
@rol_controller.route("/", methods=['GET'])
@roles_required("ADMINISTRADOR")
def index():
    if current_user.is_authenticated:
        rol_service = BuildRolService.build()
        list_roles = rol_service.VerTodosLosRoles()

        return render_template(
            "module_gestion_usuarios/VerRoles.html", 
            roles=list_roles
        )
    else:
        return redirect(url_for("usuario.LoginUsuarioGet"))

# ==============================================================================
# CREAR ROL
# ==============================================================================
@rol_controller.route("/crear", methods=['GET'])
@roles_required("ADMINISTRADOR")
def create_get():
    if current_user.is_authenticated:
        return render_template("module_gestion_usuarios/RegistrarRol.html")
    else:
        return redirect(url_for("usuario.LoginUsuarioGet"))

@rol_controller.route("/crear", methods=['POST'])
@roles_required("ADMINISTRADOR")
def create():
    if current_user.is_authenticated:
        now_val = datetime.now()
        rol_service = BuildRolService.build()
        rol_domain_entity = RolDomainEntity()

        rol_domain_entity.nombre = request.form["nombre"].upper()
        rol_domain_entity.descripcion = request.form["descripcion"]
        rol_domain_entity.creado_en = now_val
        rol_domain_entity.actualizado_en = now_val

        try:
            rol_service.CrearRol(rol_domain_entity)
            flash("Rol registrado con éxito", "success")
            return redirect(url_for("rol.index"))
        except Exception:
            flash("No se pudo registrar el rol", "error")
            return redirect(url_for("rol.create_get"))
    else:
        return redirect(url_for("usuario.LoginUsuarioGet"))

# ==============================================================================
# EDITAR ROL
# ==============================================================================
@rol_controller.route("/editar/<string:id_rol>", methods=['GET'])
@roles_required("ADMINISTRADOR")
def edit_get(id_rol: str):
    if current_user.is_authenticated:
        rol_service = BuildRolService.build()
        rol_domain_entity = rol_service.ObtenerRolPorId(id_rol)

        return render_template(
            "module_gestion_usuarios/EditarRol.html", 
            rol=rol_domain_entity
        )
    else:
        return redirect(url_for("usuario.LoginUsuarioGet"))

@rol_controller.route("/editar", methods=['POST'])
@roles_required("ADMINISTRADOR")
def edit():
    if current_user.is_authenticated:
        if request.form.get('_method') == 'PUT':
            pass

        rol_service = BuildRolService.build()
        rol_domain_entity = RolDomainEntity()
        now_val = datetime.now()

        rol_domain_entity.id_rol = request.form["id_rol"]
        rol_domain_entity.nombre = request.form["nombre"].upper()
        rol_domain_entity.descripcion = request.form["descripcion"]
        rol_domain_entity.actualizado_en = now_val

        if rol_service.EditarRol(rol_domain_entity): 
            flash("No se pudo editar el Rol", "error")
        else:
            flash("Rol editado con éxito", "success")
            
        return redirect(url_for("rol.index"))
    else:
        return redirect(url_for("usuario.LoginUsuarioGet"))

# ==============================================================================
# ELIMINAR ROL
# ==============================================================================
@rol_controller.route("/eliminar/<string:id_rol>", methods=['POST'])
@roles_required("ADMINISTRADOR")
def delete(id_rol: str):
    if current_user.is_authenticated:
        rol_service = BuildRolService.build()
        
        if rol_service.EliminarRol(id_rol):
            flash("Rol eliminado con éxito.", "success")
        else:
            flash("No se pudo eliminar el Rol.", "error")

        return redirect(url_for("rol.index"))
    else:
        return redirect(url_for("usuario.LoginUsuarioGet"))