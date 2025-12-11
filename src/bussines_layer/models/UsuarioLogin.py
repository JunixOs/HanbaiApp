from flask_login import UserMixin

class UsuarioLogin(UserMixin):
    def __init__(self):
        self.id_usuario = None
        self.nombre = None
        self.correo = None
        self.dni = None
        self.rol_id = None
        # ESTE ES EL CAMPO IMPORTANTE:
        self.rol_name = None 

    def get_id(self):
        return str(self.id_usuario)
    
    # Este método ayuda a verificar roles fácilmente
    def has_role(self, role_name):
        return self.rol_name == role_name