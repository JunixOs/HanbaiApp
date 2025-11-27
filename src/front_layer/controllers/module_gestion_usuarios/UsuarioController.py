import os
from datetime import datetime

from flask import (
    render_template, Blueprint, request, redirect, url_for, flash
)
from flask_login import login_required, current_user, logout_user

# Importaciones de tus servicios y modelos
from src.builders.BuildUsuarioService import BuildUsuarioService
from src.builders.BuildRolService import BuildRolService
from src.front_layer.controllers.AuthByRol import roles_required
from src.bussines_layer.models.UsuarioDomainEntity import UsuarioDomainEntity

# Configuración del Blueprint
template_dir = os.path.abspath("src/front_layer/templates")
usuario_controller = Blueprint('usuario', __name__, template_folder=template_dir)

# ########################### AUTENTICACION ###########################

@usuario_controller.get("/login")
def LoginPage():
    """Muestra el formulario de login."""
    if current_user.is_authenticated:
        return redirect(url_for("usuario.Dashboard"))
    return render_template("module_gestion_usuarios/login.html")

@usuario_controller.post("/login")
def LoginUsuario():
    """Procesa los datos del login."""
    correo = request.form["correo"]
    password = request.form["password"]

    usuario_service = BuildUsuarioService.build()
    usuario_login_message = usuario_service.IniciarSesion(password, correo)

    if usuario_login_message == "Sesion iniciada con exito":
        return redirect(url_for("usuario.Dashboard"))
    else:
        flash(usuario_login_message, "error")
        return redirect(url_for("usuario.LoginPage"))

@usuario_controller.route("/logout")
@login_required
def LogoutUsuario():
    """Cierra la sesión del usuario."""
    logout_user()
    return redirect(url_for("home.ShowHome"))

# ########################### PÁGINAS PÚBLICAS ###########################

@usuario_controller.get("/contactar-soporte")
def ContactarSoporte():
    return render_template("ContactarSoporte.html")

@usuario_controller.get("/sobre-nosotros")
def SobreNosotros():
    return render_template("SobreNosotros.html")

# ########################### DASHBOARD Y GESTIÓN ###########################

@usuario_controller.get("/dashboard")
@login_required
def Dashboard():
    """Muestra el panel principal del usuario."""
    nombre = current_user.nombre
    correo = current_user.correo
    rol = current_user.rol.nombre if current_user.rol else "Sin Rol"

    return render_template(
        "module_gestion_usuarios/Dashboard.html",
        nombre=nombre,
        correo=correo,
        rol=rol
    )

@usuario_controller.get("/usuarios")
@roles_required("ADMINISTRADOR")
def VerTodosLosUsuarios():
    """Lista todos los usuarios (Solo Admin)."""
    usuario_service = BuildUsuarioService.build()
    list_usuarios = usuario_service.VerTodosLosUsuarios()

    return render_template(
        "module_gestion_usuarios/VerUsuarios.html",
        usuarios=list_usuarios
    )

# ########################### REGISTRO ###########################

@usuario_controller.post("/registrar/cliente")
def RegistrarUsuarioComoClientePost():
    """Registro público de clientes."""
    rol_service = BuildRolService.build()
    usuario_service = BuildUsuarioService.build()

    rol_domain_entity = rol_service.ObtenerRolPorNombre(rol_name="CLIENTE")
    usuario_domain_entity = UsuarioDomainEntity()
    now_timestamp = datetime.now().timestamp()

    usuario_domain_entity.nombre = request.form["nombre"]
    usuario_domain_entity.correo = request.form["correo"]
    usuario_domain_entity.password_hash = request.form["password"]
    usuario_domain_entity.dni = request.form["dni"]
    usuario_domain_entity.creado_en = now_timestamp
    usuario_domain_entity.actualizado_en = now_timestamp
    
    if rol_domain_entity:
        usuario_domain_entity.rol_id = rol_domain_entity.id_rol
        usuario_service.RegistrarUsuario(usuario_domain_entity)
        flash("Usuario registrado con éxito", "success")
    else:
        flash("Error: Rol CLIENTE no encontrado", "error")

    return redirect(url_for("usuario.LoginPage"))

@usuario_controller.get("/registrar")
@roles_required("ADMINISTRADOR")
def RegistrarUsuarioGet():
    """Muestra formulario para crear usuario (Admin)."""
    rol_service = BuildRolService.build()
    list_roles = rol_service.VerTodosLosRoles()

    return render_template(
        "module_gestion_usuarios/RegistrarUsuarios.html",
        roles=list_roles
    )

@usuario_controller.post("/registrar")
@roles_required("ADMINISTRADOR")
def RegistrarUsuarioPost():
    """Procesa creación de usuario (Admin)."""
    usuario_service = BuildUsuarioService.build()
    now_timestamp = datetime.now().timestamp()
    usuario = UsuarioDomainEntity()

    usuario.correo = request.form["correo"]
    usuario.nombre = request.form["nombre"]
    usuario.password_hash = request.form["password"]
    usuario.dni = request.form["dni"]
    usuario.creado_en = now_timestamp
    usuario.actualizado_en = now_timestamp
    usuario.rol_id = request.form["rol_id"]

    try:
        usuario_service.RegistrarUsuario(usuario)
        flash("Usuario registrado con éxito", "success")
    except Exception as e:
        flash(f"Error en el registro: {str(e)}", "error")
    
    return redirect(url_for("usuario.VerTodosLosUsuarios"))

# ########################### EDICIÓN DE PERFIL (Usuario) ###########################

@usuario_controller.get("/editar")
@login_required
def EditarInformacionGet():
    """Muestra formulario para editar perfil propio."""
    id_usuario = current_user.id_usuario
    usuario_service = BuildUsuarioService.build()
    rol_service = BuildRolService.build()

    usuario_domain = usuario_service.ObtenerUsuarioPorId(id_usuario)
    usuario_domain.password_hash = "" # Ocultar pass
    
    rol_obj = rol_service.ObtenerRolPorId(usuario_domain.rol_id)
    rol_name = rol_obj.nombre if rol_obj else "N/A"

    return render_template(
        "module_gestion_usuarios/EditarUsuario.html",
        usuario=usuario_domain,
        rol_name=rol_name
    )

@usuario_controller.post("/editar") # Usamos POST para el form
@login_required
def EditarInformacionPost():
    """Procesa edición de perfil propio."""
    usuario_service = BuildUsuarioService.build()
    usuario = UsuarioDomainEntity()
    
    usuario.id_usuario = current_user.id_usuario # Importante: ID del usuario logueado
    usuario.correo = request.form["correo"]
    usuario.nombre = request.form["nombre"]
    usuario.password_hash = request.form.get("password", "")
    usuario.dni = request.form["dni"]
    usuario.actualizado_en = datetime.now().timestamp()

    if usuario_service.EditarUsuario(usuario):
        flash("Información actualizada con éxito", "success")
    else:
        flash("No se pudo actualizar la información", "error")
        
    return redirect(url_for("usuario.Dashboard"))

# ########################### GESTIÓN DE USUARIOS (Admin) ###########################

@usuario_controller.get("/editar-usuario/<string:id_usuario>")
@roles_required("ADMINISTRADOR")
def EditarUsuarioAdminGet(id_usuario):
    """Muestra formulario para editar otro usuario (Admin)."""
    usuario_service = BuildUsuarioService.build()
    rol_service = BuildRolService.build()

    usuario_domain = usuario_service.ObtenerUsuarioPorId(id_usuario)
    usuario_domain.password_hash = ""
    list_roles = rol_service.VerTodosLosRoles()

    return render_template(
        "module_gestion_usuarios/EditarUsuario.html",
        usuario=usuario_domain,
        roles=list_roles
    )

@usuario_controller.post("/editar-usuario")
@roles_required("ADMINISTRADOR")
def EditarUsuarioAdminPost():
    """Procesa edición de otro usuario (Admin)."""
    usuario_service = BuildUsuarioService.build()
    usuario = UsuarioDomainEntity()
    
    # Necesitas pasar el ID del usuario a editar en un campo oculto en el HTML
    # o extraerlo de alguna manera. Asumiré que viene en el form.
    # Si no, ajusta tu HTML para incluir <input type="hidden" name="id_usuario" value="...">
    usuario.id_usuario = request.form.get("id_usuario") 
    
    usuario.correo = request.form["correo"]
    usuario.nombre = request.form["nombre"]
    usuario.password_hash = request.form.get("password", "")
    usuario.dni = request.form["dni"]
    usuario.actualizado_en = datetime.now().timestamp()
    usuario.rol_id = request.form["rol_id"]

    if usuario_service.EditarUsuario(usuario):
        flash("Usuario actualizado correctamente", "success")
    else:
        flash("Error al actualizar usuario", "error")
        
    return redirect(url_for("usuario.VerTodosLosUsuarios"))

@usuario_controller.post("/eliminar") # Usamos POST para eliminar
@login_required
def EliminarCuenta():
    """Elimina la cuenta propia."""
    usuario_service = BuildUsuarioService.build()
    id_usuario = current_user.id_usuario
    logout_user()
    
    if usuario_service.EliminarUsuario(id_usuario):
        flash("Cuenta eliminada correctamente", "success")
    else:
        flash("Error al eliminar la cuenta", "error")

    return redirect(url_for("home.ShowHome"))