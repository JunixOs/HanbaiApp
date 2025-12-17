from src.builders.BuildUsuarioService import BuildUsuarioService
from src.builders.BuildRolService import BuildRolService
from src.front_layer.controllers.AuthByRol import roles_required
from src.bussines_layer.models.UsuarioDomainEntity import UsuarioDomainEntity

import os
from datetime import datetime

from flask import (
    render_template, Blueprint, request, redirect, url_for, flash
)
from flask_login import login_required, current_user, logout_user

template_dir = os.path.abspath("src/front_layer/templates")
usuario_controller = Blueprint('usuario', __name__, template_folder=template_dir)

# ==============================================================================
# AUTENTICACIÓN
# ==============================================================================

@usuario_controller.route("/logout")
@login_required
def LogoutUsuario():
    logout_user()
    return redirect(url_for("home.ShowHome"))

@usuario_controller.route("/login")
def LoginUsuarioGet():
    if current_user.is_authenticated:
        # CAMBIO: Al Home
        return redirect(url_for("home.ShowHome"))
    return render_template("module_gestion_usuarios/login.html")

@usuario_controller.post("/login")
def LoginUsuarioPost():
    if current_user.is_authenticated:
        return redirect(url_for("home.ShowHome"))

    correo = request.form["correo"]
    password = request.form["password"]

    usuario_service = BuildUsuarioService.build()
    usuario_login_message, status = usuario_service.IniciarSesion(password, correo)

    if not status:
        flash("Credenciales incorrectas.", "error")
        return redirect(url_for("usuario.LoginUsuarioGet"))
    else:
        # CAMBIO: Al Home después de loguearse exitosamente
        return redirect(url_for("home.ShowHome"))

# ==============================================================================
# PÁGINAS PÚBLICAS
# ==============================================================================

@usuario_controller.get("/contactar-soporte")
def ContactarSoporte():
    return render_template("ContactarSoporte.html")

@usuario_controller.get("/sobre-nosotros")
def SobreNosotros():
    return render_template("SobreNosotros.html")

# ==============================================================================
# DASHBOARD
# ==============================================================================

@usuario_controller.get("/dashboard")
@login_required
def Dashboard():
    # Usamos .rol_name porque UsuarioLogin (sesión) solo tiene el texto, no el objeto
    nombre = current_user.nombre
    correo = current_user.correo
    rol = getattr(current_user, 'rol_name', 'Sin Rol')

    return render_template(
        "module_gestion_usuarios/Dashboard.html",
        nombre=nombre,
        correo=correo,
        rol=rol
    )
    
@usuario_controller.get("/usuarios")
@roles_required("ADMINISTRADOR")
def VerTodosLosUsuarios():
    usuario_service = BuildUsuarioService.build()
    list_usuarios = usuario_service.VerTodosLosUsuarios()

    return render_template(
        "module_gestion_usuarios/VerUsuarios.html", 
        usuarios=list_usuarios
    )

# ==============================================================================
# REGISTRO DE CLIENTES
# ==============================================================================

@usuario_controller.get("/registrar/cliente")
def RegistrarUsuarioComoClienteGet():
    if current_user.is_authenticated:
        return redirect(url_for("producto.index"))
    return render_template("module_gestion_usuarios/RegistrarUsuarioComoCliente.html")

@usuario_controller.post("/registrar/cliente")
def RegistrarUsuarioComoClientePost():
    try:
        rol_service = BuildRolService.build()
        usuario_service = BuildUsuarioService.build()

        rol_domain_entity = rol_service.ObtenerRolPorNombre(rol_name="CLIENTE")
        if not rol_domain_entity:
            flash("Error interno: Rol CLIENTE no encontrado.", "error")
            return redirect(url_for("usuario.LoginUsuarioGet"))

        usuario_domain_entity = UsuarioDomainEntity()
        now_val = datetime.now()

        usuario_domain_entity.nombre = request.form["nombre"]
        usuario_domain_entity.correo = request.form["correo"]
        usuario_domain_entity.password_hash = request.form["password"]
        usuario_domain_entity.dni = request.form["dni"]
        usuario_domain_entity.creado_en = now_val
        usuario_domain_entity.actualizado_en = now_val
        usuario_domain_entity.rol_id = rol_domain_entity.id_rol

        usuario_service.RegistrarUsuario(usuario_domain_entity)

        # Auto-login tras registro
        _, status = usuario_service.IniciarSesion(request.form["password"], request.form["correo"])
        if status:
            return redirect(url_for("producto.index"))
        
        return redirect(url_for("usuario.LoginUsuarioGet"))

    except Exception:
        flash("Error al registrar usuario.", "error")
        return redirect(url_for("usuario.RegistrarUsuarioComoClienteGet"))

# ==============================================================================
# GESTIÓN ADMINISTRATIVA (CREAR)
# ==============================================================================

@usuario_controller.get("/registrar")
@roles_required("ADMINISTRADOR")
def RegistrarUsuarioGet():
    rol_service = BuildRolService.build()
    list_roles = rol_service.VerTodosLosRoles()
    return render_template("module_gestion_usuarios/RegistrarUsuarios.html", roles=list_roles)

@usuario_controller.post("/registrar")
@roles_required("ADMINISTRADOR")
def RegistrarUsuarioPost():
    try:
        usuario_service = BuildUsuarioService.build()
        now_val = datetime.now()

        usuario_domain_entity = UsuarioDomainEntity()
        usuario_domain_entity.correo = request.form["correo"]
        usuario_domain_entity.nombre = request.form["nombre"]
        usuario_domain_entity.password_hash = request.form["password"]
        usuario_domain_entity.dni = request.form["dni"]
        usuario_domain_entity.creado_en = now_val
        usuario_domain_entity.actualizado_en = now_val
        usuario_domain_entity.rol_id = request.form["rol_id"]

        usuario_service.RegistrarUsuario(usuario_domain_entity)
        flash("Usuario registrado con éxito", "success")
        
    except Exception as e:
        print(f"❌ ERROR EN REGISTRO DE USUARIO: {e}")
        flash(f"Error en el registro: {e}", "error") # Opcional: mostrar detalle en web
    
    return redirect(url_for("usuario.VerTodosLosUsuarios"))

# ==============================================================================
# EDITAR INFORMACIÓN (PERFIL)
# ==============================================================================

@usuario_controller.get("/editar")
@login_required
def EditarInformacionGet():
    id_usuario = current_user.id_usuario
    if id_usuario is None:
        return redirect(url_for("usuario.LoginUsuarioGet"))

    usuario_service = BuildUsuarioService.build()
    rol_service = BuildRolService.build()

    # Buscamos en BD para obtener datos frescos
    usuario_domain = usuario_service.ObtenerUsuarioPorId(id_usuario)
    usuario_domain.password_hash = "" 
    
    # Obtenemos nombre del rol desde la BD
    rol_obj = rol_service.ObtenerRolPorId(usuario_domain.rol_id)
    rol_name = rol_obj.nombre if rol_obj else "Sin Rol"
    
    usuario_domain.rol_id = ""

    return render_template(
        "module_gestion_usuarios/EditarUsuario.html", 
        usuario=usuario_domain, 
        rol_name=rol_name
    )
    
@usuario_controller.post("/editar")
@login_required
def EditarInformacionPut():
    if request.form.get('_method') == 'PUT': pass 

    now_val = datetime.now()
    usuario_service = BuildUsuarioService.build()
    usuario_domain_entity = UsuarioDomainEntity()

    usuario_domain_entity.id_usuario = current_user.id_usuario
    usuario_domain_entity.correo = request.form["correo"]
    usuario_domain_entity.nombre = request.form["nombre"]
    
    password = request.form.get("password")
    if password:
        usuario_domain_entity.password_hash = password
    
    usuario_domain_entity.dni = request.form["dni"]
    usuario_domain_entity.actualizado_en = now_val

    error = usuario_service.EditarUsuario(usuario_domain_entity)

    if error:
        flash("No se pudo guardar la información.", "error")
    else:
        flash("Perfil actualizado con éxito.", "success")
    
    return redirect(url_for("usuario.Dashboard"))

# ==============================================================================
# EDITAR USUARIOS (ADMIN)
# ==============================================================================

@usuario_controller.get("/editar-usuario/<string:id_usuario>")
@roles_required("ADMINISTRADOR")
def EditarUsuarioGet(id_usuario):
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
def EditarUsuarioPut():
    now_val = datetime.now()
    usuario_service = BuildUsuarioService.build()
    usuario_domain_entity = UsuarioDomainEntity()
    
    if "id_usuario" in request.form:
        usuario_domain_entity.id_usuario = request.form["id_usuario"]
    
    usuario_domain_entity.correo = request.form["correo"]
    usuario_domain_entity.nombre = request.form["nombre"]
    
    password = request.form.get("password")
    if password:
        usuario_domain_entity.password_hash = password
        
    usuario_domain_entity.dni = request.form["dni"]
    usuario_domain_entity.actualizado_en = now_val
    usuario_domain_entity.rol_id = request.form["rol_id"]

    error = usuario_service.EditarUsuario(usuario_domain_entity)

    if error:
        flash("Error al actualizar usuario.", "error")
    else:
        flash("Usuario actualizado con éxito.", "success")
    
    return redirect(url_for("usuario.VerTodosLosUsuarios"))

# ==============================================================================
# CONFIRMAR Y ELIMINAR CUENTA
# ==============================================================================

@usuario_controller.get("/eliminar/confirmar/<string:id_usuario>")
@roles_required("ADMINISTRADOR")
def ConfirmarEliminarGet(id_usuario):
    # Pantalla intermedia de "Estás seguro?"
    usuario_service = BuildUsuarioService.build()
    rol_service = BuildRolService.build()
    
    usuario_a_eliminar = usuario_service.ObtenerUsuarioPorId(id_usuario)
    
    # Obtenemos nombre del rol para mostrar en la advertencia
    rol_obj = rol_service.ObtenerRolPorId(usuario_a_eliminar.rol_id)
    rol_name = rol_obj.nombre if rol_obj else "Sin Rol"
    
    # Inyectamos rol_nombre manualmente al objeto para que la vista lo lea fácil
    # (O lo pasamos como variable separada, como prefieras. Aquí va separado).
    return render_template(
        "module_gestion_usuarios/EliminarUsuario.html", 
        usuario=usuario_a_eliminar,
        rol_name=rol_name
    )

@usuario_controller.post("/eliminar")
@login_required
def EliminarCuenta():
    usuario_service = BuildUsuarioService.build()
    
    # 1. Verificamos si es un Admin borrando a otro (ID viene en form)
    id_usuario_a_eliminar = request.form.get("id_usuario_delete")
    
    rol_actual = getattr(current_user, 'rol_name', 'SIN_ROL')
    
    if id_usuario_a_eliminar and rol_actual == 'ADMINISTRADOR':
        # Caso Admin: Borra y vuelve a la lista
        if usuario_service.EliminarUsuario(id_usuario_a_eliminar):
            flash("Usuario eliminado correctamente.", "success")
        else:
            flash("No se pudo eliminar al usuario.", "error")
        return redirect(url_for("usuario.VerTodosLosUsuarios"))
    
    else:
        # Caso Propio: Borra su propia cuenta y sale
        id_propio = current_user.id_usuario
        logout_user() 
        
        if usuario_service.EliminarUsuario(id_propio):
            flash("Tu cuenta ha sido eliminada.", "info")
        else:
            flash("No se pudo eliminar tu cuenta.", "error")

        return redirect(url_for("usuario.LoginUsuarioGet"))