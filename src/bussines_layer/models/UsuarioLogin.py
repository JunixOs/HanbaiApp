from flask_login import UserMixin

class UsuarioLogin(UserMixin):
    def __init__(self):
        # tus atributos actuales
        self.id_usuario = None
        self.nombre = None
        self.correo = None
        self.rol_id = None
        self.rol_name = None

    def get_id(self):
        return str(self.id_usuario)
    
    def has_role(self , role_name):
        return True if self.rol_name == role_name.strip() else False 