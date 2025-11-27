class CategoriaDomainEntity:

    __id_categoria: str
    __nombre: str
    __descuento_categoria: float
    __descripcion: str

    @property
    def id_categoria(self):
        return self.__id_categoria
    
    @property
    def nombre(self) -> str:
        return self.__nombre
    @nombre.setter
    def nombre(self , nombre: str) -> None:
        self.__nombre = nombre

    @property
    def descuento_categoria(self) -> float:
        return self.__descuento_categoria
    @descuento_categoria.setter
    def descuento_categoria(self , descuento_categoria: float) -> None:
        self.__descuento_categoria = descuento_categoria

    @property
    def descripcion(self) -> str:
        return self.__descripcion
    @descripcion.setter
    def descripcion(self , descripcion) -> None:
        self.__descripcion = descripcion