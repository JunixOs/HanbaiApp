class RolDomainEntity:
    
    __id_rol: str
    __nombre: str
    __descripcion: str
    __creado_en: float
    __actualizado_en: float

    @property
    def id_rol(self) -> str:
        return self.__id_rol
    @id_rol.setter
    def id_rol(self , id_rol: str) -> None:
        self.__id_rol = id_rol
    
    @property
    def nombre(self) -> str:
        return self.__nombre
    @nombre.setter
    def nombre(self , nombre: str) -> None:
        self.__nombre = nombre

    @property
    def descripcion(self) -> str:
        return self.__descripcion
    @descripcion.setter
    def descripcion(self, descripcion: str) -> None:
        self.__descripcion = descripcion

    @property
    def creado_en(self) -> float:
        return self.__creado_en
    @creado_en.setter
    def creado_en(self , creado_en: float) -> None:
        self.__creado_en = creado_en

    @property
    def actualizado_en(self) -> float:
        return self.__actualizado_en
    @actualizado_en.setter
    def actualizado_en(self , actualizado_en: float) -> None:
        self.__actualizado_en = actualizado_en