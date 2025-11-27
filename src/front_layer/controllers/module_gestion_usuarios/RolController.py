import os
from datetime import datetime

from flask import (
    render_template, Blueprint, request, redirect, url_for, flash
)
from flask_login import login_required, current_user

# Importaciones de servicios y modelos
from src.builders.BuildRolService import BuildRolService
from src.front_layer.controllers.AuthByRol import roles_required
from src.bussines_layer.models.RolDomainEntity import RolDomainEntity

template_dir = os.path.abspath("src/front_layer/templates")
rol_controller = Blueprint('rol', __name__, template_folder=template_dir)

# ==============================================================================
# VER ROLES
# ==============================================================================
@rol_controller.get("/roles")
@roles_required("ADMINISTRADOR")
def VerTodosLosRoles():
    if current_user.is_authenticated:
        rol_service = BuildRolService.build()
        list_roles = rol_service.VerTodosLosRoles()

        return render_template(
            "module_gestion_usuarios/VerRoles.html",
            roles=list_roles
        )
    else:
        return redirect(url_for("usuario.LoginPage"))

# ==============================================================================
# CREAR ROL
# ==============================================================================
@rol_controller.post("/crear")
@roles_required("ADMINISTRADOR")
def CrearRol():
    if current_user.is_authenticated:
        now_timestamp = datetime.now().timestamp()
        rol_service = BuildRolService.build()
        rol_domain_entity = RolDomainEntity()

        rol_domain_entity.nombre = request.form["nombre"]
        rol_domain_entity.descripcion = request.form["descripcion"]
        rol_domain_entity.creado_en = now_timestamp
        rol_domain_entity.actualizado_en = now_timestamp

        try:
            rol_service.CrearRol(rol_domain_entity)
            flash("Rol registrado con éxito", "success")
        except Exception as e:
            flash(f"No se pudo registrar el rol: {str(e)}", "error")
        
        # CORRECCIÓN: Redirigir a la lista de roles, no al template HTML
        return redirect(url_for("rol.VerTodosLosRoles"))

    else:
        return redirect(url_for("usuario.LoginPage"))

# ==============================================================================
# EDITAR ROL
# ==============================================================================
@rol_controller.get("/editar/<string:id_rol>")
@roles_required("ADMINISTRADOR")
def EditarRolGet(id_rol):
    if current_user.is_authenticated:
        rol_service = BuildRolService.build()
        rol_domain_entity = rol_service.ObtenerRolPorId(id_rol)

        return render_template(
            "module_gestion_usuarios/EditarRol.html", 
            rol_name=rol_domain_entity.nombre, 
            rol_description=rol_domain_entity.descripcion,
            id_rol=id_rol 
        )
    else:
        return redirect(url_for("usuario.LoginPage"))

@rol_controller.post("/editar/<string:id_rol>") # CORRECCIÓN: PUT -> POST
@roles_required("ADMINISTRADOR")
def EditarRolPost(id_rol):
    if current_user.is_authenticated:
        rol_service = BuildRolService.build()
        rol_domain_entity = RolDomainEntity()

        # CORRECCIÓN: Asignar el ID para que el servicio sepa cuál editar
        rol_domain_entity.id_rol = id_rol
        
        rol_domain_entity.nombre = request.form["nombre"]
        rol_domain_entity.descripcion = request.form["descripcion"]
        rol_domain_entity.actualizado_en = datetime.now().timestamp()

        # CORRECCIÓN: Llamada al servicio que faltaba en tu código original
        if rol_service.EditarRol(rol_domain_entity):
            flash("Rol editado con éxito", "success")
        else:
            flash("Error al editar el rol", "error")

        return redirect(url_for("rol.VerTodosLosRoles"))
    else:
        return redirect(url_for("usuario.LoginPage"))

# ==============================================================================
# ELIMINAR ROL
# ==============================================================================
@rol_controller.post("/eliminar/<string:id_rol>") # CORRECCIÓN: DELETE -> POST
@roles_required("ADMINISTRADOR")
def EliminarRolPost(id_rol):
    if current_user.is_authenticated:
        rol_service = BuildRolService.build()

        if rol_service.EliminarRol(id_rol):
            flash("Rol eliminado con éxito.", "success")
        else:
            flash("No se pudo eliminar el Rol.", "error")

        # CORRECCIÓN: Redirigir a la lista, no a la edición del rol borrado
        return redirect(url_for("rol.VerTodosLosRoles"))
    else:
        return redirect(url_for("usuario.LoginPage"))