from datetime import datetime

class UsuarioDomainEntity:
    # Definimos las variables privadas para que existan desde el inicio
    def __init__(self):
        self.__id_usuario = None
        self.__nombre = ""
        self.__correo = ""
        self.__password_hash = ""
        self.__dni = ""
        self.__rol_id = None
        self.__creado_en = None
        self.__actualizado_en = None

    # ==========================
    # GETTERS Y SETTERS
    # ==========================

    @property
    def id_usuario(self):
        return self.__id_usuario
    
    @id_usuario.setter
    def id_usuario(self, value):
        self.__id_usuario = value

    @property
    def nombre(self):
        return self.__nombre
    
    @nombre.setter
    def nombre(self, value):
        self.__nombre = value

    @property
    def correo(self):
        return self.__correo
    
    @correo.setter
    def correo(self, value):
        self.__correo = value

    @property
    def password_hash(self):
        return self.__password_hash
    
    @password_hash.setter
    def password_hash(self, value):
        self.__password_hash = value

    @property
    def dni(self):
        return self.__dni
    
    @dni.setter
    def dni(self, value):
        self.__dni = value

    @property
    def rol_id(self):
        return self.__rol_id
    
    @rol_id.setter
    def rol_id(self, value):
        self.__rol_id = value

    @property
    def creado_en(self):
        return self.__creado_en
    
    @creado_en.setter
    def creado_en(self, value):
        self.__creado_en = value

    @property
    def actualizado_en(self):
        return self.__actualizado_en
    
    @actualizado_en.setter
    def actualizado_en(self, value):
        self.__actualizado_en = value