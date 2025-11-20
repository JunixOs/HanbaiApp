from datetime import datetime

class UsuarioDomainEntity:

    __id_usuario: str
    __nombre: str
    __correo: str
    __password_hash: str
    __dni: str
    __creado_en: float
    __actualizado_en: float
    __rol_id: str

    @property
    def id_usuario(self) -> str:
        return self.__id_usuario
    @id_usuario.setter
    def id_usuario(self , id_usuario: str) -> None:
        self.__id_usuario = id_usuario

    @property
    def nombre(self) -> str:
        return self.__nombre
    @nombre.setter
    def nombre(self , nombre: str) -> None:
        self.__nombre = nombre

    @property
    def correo(self) -> str:
        return self.__correo
    @correo.setter
    def correo(self , correo: str) -> None:
        self.__correo = correo

    @property
    def password_hash(self) -> str:
        return self.__password_hash
    @password_hash.setter
    def password_hash(self , password_hash: str) -> None:
        self.__password_hash = password_hash

    @property
    def dni(self) -> str:
        return self.__dni
    @dni.setter
    def dni(self , dni: str) -> None:
        self.__dni = dni

    @property
    def creado_en(self) -> float:
        return self.__creado_en
    @creado_en.setter
    def creado_en(self, creado_en: float) -> None:
        self.__creado_en = creado_en

    @property
    def actualizado_en(self) -> float:
        return self.__actualizado_en
    @actualizado_en.setter
    def actualizado_en(self, actualizado_en: float) -> None:
        self.__actualizado_en = actualizado_en
    
    @property
    def rol_id(self) -> str:
        return self.__rol_id
    @rol_id.setter
    def rol_id(self , rol_id) -> None:
        self.__rol_id = rol_id


    def DiasDeCuentaActiva(self):
        difference = datetime.now() - datetime.fromtimestamp(self.__creado_en)

        return difference.days
    
    def DiasDesdeUltimaActualizacion(self):
        difference = datetime.now() - datetime.fromtimestamp(self.__actualizado_en)

        return difference.days