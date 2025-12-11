from functools import wraps
from flask import abort, redirect, url_for, flash
from flask_login import current_user

def roles_required(*roles_permitidos):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            # 1. Verificar Login
            if not current_user.is_authenticated:
                return redirect(url_for('usuario.LoginUsuarioGet'))
            
            # 2. Verificar Rol (CORRECCIÓN AQUÍ)
            # Usamos .rol_name, NO .rol.nombre
            rol_actual = getattr(current_user, 'rol_name', 'SIN_ROL')
            
            if rol_actual not in roles_permitidos:
                flash("No tienes permisos para acceder a esta sección.", "error")
                return redirect(url_for('producto.index'))
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper