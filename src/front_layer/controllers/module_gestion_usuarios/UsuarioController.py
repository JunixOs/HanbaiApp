from src.builders.BuildUsuarioService import BuildUsuarioService
from src.builders.BuildRolService import BuildRolService
from src.front_layer.controllers.AuthByRol import roles_required
from src.bussines_layer.models.UsuarioDomainEntity import UsuarioDomainEntity

import os
from datetime import datetime

from flask import (
    render_template , Blueprint , request , redirect , url_for , flash
)
from flask_login import login_required , current_user , logout_user

template_dir = os.path.abspath("src/front_layer/templates")
usuario_controller = Blueprint('usuario' , __name__ , template_folder=template_dir)

# ########################### AUTENTICACION ###########################
@usuario_controller.route("/logout")
@login_required
def LogoutUsuario():
    logout_user()
    return render_template("home.html")

@usuario_controller.post("/login")
def LoginUsuario():
    correo = request.form["correo"]
    password = request.form["password"]

    usuario_service = BuildUsuarioService.build()

    usuario_login_message = usuario_service.IniciarSesion(password , correo)

    if(usuario_login_message is not None):
        return redirect("/login")
    else:
        flash(usuario_login_message , "message")
        return redirect(url_for("Dashboard"))
    
# ########################### AUTENTICACION ###########################

# ########################### CARGA DE PAGINAS ###########################
@usuario_controller.get("/contactar-soporte")
def ContactarSoporte():
    return render_template("ContactarSoporte.html")

@usuario_controller.get("/sobre-nosotros")
def SobreNosotros():
    return render_template("SobreNosotros.html")

# ########################### INFORMACION PARA CARGAR PAGINAS ###########################
@usuario_controller.get("/dashboard")
@login_required
def Dashboard():
    if(current_user.is_authenticated):

        nombre = current_user.nombre
        correo = current_user.correo
        rol = current_user.rol.nombre if current_user.rol else None

        return render_template(
            "Dashboard.html" , 
            nombre=nombre ,
            correo=correo,
            rol=rol
        )
    else:
        return render_template("module_gestion_usuarios/login.html")
    
@usuario_controller.get("/usuarios")
@roles_required("ADMINISTRADOR")
def VerTodosLosUsuarios():
    if(current_user.is_authenticated):
        usuario_service = BuildUsuarioService.build()

        list_usuarios = usuario_service.VerTodosLosUsuarios()

        return render_template(
            "module_gestion_usuarios/VerUsuarios.html" , 
            usuarios=list_usuarios
        )
    else:
        return render_template("module_gestion_usuarios/login.html")
    
# ########################### INFORMACION PARA CARGAR PAGINAS ###########################

# ########################### REGISTRAR USUARIO (ADMIN) ###########################
@usuario_controller.get("/registrar")
@roles_required("ADMINISTRADOR")
def RegistrarUsuarioGet():
    if(current_user.is_authenticated):

        rol_service = BuildRolService.build()

        list_roles = rol_service.VerTodosLosRoles()

        return render_template(
            "module_gestion_usuarios/RegistrarUsuarios.html" , 
            roles = list_roles
        )
    else:
        return render_template("module_gestion_usuarios/login.html")

@usuario_controller.post("/registrar")
@roles_required("ADMINISTRADOR")
def RegistrarUsuarioPost():
    if(current_user.is_authenticated):
        usuario_service = BuildUsuarioService.build()

        now_timestamp = datetime.now().timestamp()

        usuario_domain_entity = UsuarioDomainEntity()

        usuario_domain_entity.correo = request.form["correo"]
        usuario_domain_entity.nombre = request.form["nombre"]
        usuario_domain_entity.password_hash = request.form["password"]
        usuario_domain_entity.dni = request.form["dni"]
        usuario_domain_entity.creado_en = now_timestamp
        usuario_domain_entity.actualizado_en = now_timestamp
        usuario_domain_entity.rol_id = request.form["rol_id"]

        try:
            usuario_service.RegistrarUsuario(
                usuario_domain_entity
            )
        except Exception:
            flash("Algo salio mal en el registro" , "message")
        else:
            flash("Usuario registrado con exito" , "message")
        
        return redirect("module_gestion_usuarios/VerUsuarios.html")        

    else:
        return redirect("module_gestion_usuarios/login.html")
# ########################### REGISTRAR USUARIO (ADMIN) ###########################

# ########################### EDITAR INFORMACION DE CUENTA ###########################
@usuario_controller.get("/editar")
@login_required
def EditarInformacionGet():
    if(current_user.is_authenticated):
        id_usuario = current_user.id_usuario

        if(id_usuario is None):
            return render_template("module_gestion_usuarios/login.html")

        usuario_service = BuildUsuarioService.build()
        rol_service = BuildRolService.build()

        usuario_domain = usuario_service.ObtenerUsuarioPorId(id_usuario)

        usuario_domain.password_hash = ""
        usuario_domain.id_usuario = ""
        
        rol_name = rol_service.ObtenerRolPorId(usuario_domain.rol_id).nombre

        usuario_domain.rol_id = ""

        return render_template(
            "module_gestion_usuarios/EditarUsuario.html" , 
            usuario=usuario_domain , 
            rol_name = rol_name
        )

    else:
        return render_template("module_gestion_usuarios/login.html")
    
@usuario_controller.post("/editar")
@login_required
def EditarInformacionPost():
    if(current_user.is_authenticated):

        now_timestamp = datetime.now().timestamp()
        usuario_service = BuildUsuarioService.build()

        usuario_domain_entity = UsuarioDomainEntity()

        usuario_domain_entity.correo = request.form["correo"]
        usuario_domain_entity.nombre = request.form["nombre"]
        usuario_domain_entity.password_hash = request.form["password"]
        usuario_domain_entity.dni = request.form["dni"]
        usuario_domain_entity.actualizado_en = now_timestamp

        resultado_editar = usuario_service.EditarUsuario(usuario_domain_entity)

        if(resultado_editar):
            message = "No se pudo editar la informacion."
        else:
            message = "Informacion actualizada con exito."
        
        return render_template(
            "module_gestion_usuarios/Dashboard.html" , 
            message=message
        )
    else:
        return render_template("module_gestion_usuarios/login.html")
    
# ########################### EDITAR INFORMACION DE CUENTA ###########################

# ########################### EDITAR USUARIOS (ADMIN) ###########################
@usuario_controller.get("/editar-usuario/<str:id_usuario>")
@roles_required("ADMINISTRADOR")
def EditarUsuarioGet(id_usuario):
    if(current_user.is_authenticated):
        usuario_service = BuildUsuarioService.build()
        rol_service = BuildRolService.build()

        if(id_usuario is None):
            return render_template("module_gestion_usuarios/VerUsuarios.html")
        

        usuario_domain = usuario_service.ObtenerUsuarioPorId(id_usuario)

        usuario_domain.password_hash = ""
        usuario_domain.id_usuario = ""

        list_roles = rol_service.VerTodosLosRoles()

        return render_template(
            "module_gestion_usuarios/EditarUsuario.html" , 
            usuario = usuario_domain , 
            roles = list_roles
        )

    else:
        return render_template("module_gestion_usuarios/login.html")
    
@usuario_controller.post("/editar-usuario")
@roles_required("ADMINISTRADOR")
def EditarUsuarioPost():
    if(current_user.is_authenticated):

        now_timestamp = datetime.now().timestamp()
        usuario_service = BuildUsuarioService.build()

        usuario_domain_entity = UsuarioDomainEntity()

        usuario_domain_entity.correo = request.form["correo"]
        usuario_domain_entity.nombre = request.form["nombre"]
        usuario_domain_entity.password_hash = request.form["password"]
        usuario_domain_entity.dni = request.form["dni"]
        usuario_domain_entity.actualizado_en = now_timestamp
        usuario_domain_entity.rol_id = request.form["rol_id"]

        resultado_editar = usuario_service.EditarUsuario(usuario_domain_entity)

        if(resultado_editar):
            message = "No se pudo editar la informacion."
        else:
            message = "Informacion actualizada con exito."
        
        return render_template(
            "module_gestion_usuarios/VerUsuarios.html" , 
            message=message
        )

    else:
        return render_template("module_gestion_usuarios/login.html")
    
# ########################### EDITAR USUARIOS (ADMIN) ###########################

# ########################### ELIMINAR CUENTA ###########################
@usuario_controller.delete("/eliminar")
@login_required
def EliminarCuenta():
    usuario_service = BuildUsuarioService.build()

    id_usuario = current_user.id_usuario

    logout_user()

    resultado_eliminacion = usuario_service.EliminarUsuario(id_usuario)

    if(resultado_eliminacion):
        message = "Eliminacion correcta"
    else:
        message = "Eliminacion fallida"

    return render_template(
        "home.html" , 
        message=message
    )
# ########################### ELIMINAR CUENTA ###########################
