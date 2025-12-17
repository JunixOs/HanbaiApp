from datetime import datetime

class VentaDomainEntity:
    def __init__(self, id_venta=None, subtotal=0, estado_venta_id=None, usuario_id=None, items=None):
        self.__id_venta = id_venta
        self.__subtotal = subtotal
        self.__estado_venta_id = estado_venta_id
        self.__usuario_id = usuario_id
        self.__items = items if items else []
        
        # PROPIEDADES EXTRA (Relaciones)
        self.__usuario = None
        self.__estado = None       # <--- AQUÍ GUARDAREMOS EL OBJETO ESTADO
        self.__comprobante = None

    # --- Getters y Setters Básicos ---
    @property
    def id_venta(self):
        return self.__id_venta
    @id_venta.setter
    def id_venta(self, value):
        self.__id_venta = value

    @property
    def subtotal(self):
        return self.__subtotal
    @subtotal.setter
    def subtotal(self, value):
        self.__subtotal = value

    @property
    def estado_venta_id(self):
        return self.__estado_venta_id
    @estado_venta_id.setter
    def estado_venta_id(self, value):
        self.__estado_venta_id = value

    @property
    def usuario_id(self):
        return self.__usuario_id
    @usuario_id.setter
    def usuario_id(self, value):
        self.__usuario_id = value

    @property
    def items(self):
        return self.__items
    @items.setter
    def items(self, value):
        self.__items = value

    # --- Getters y Setters de Relaciones (NUEVO) ---
    
    @property
    def usuario(self):
        return self.__usuario
    @usuario.setter
    def usuario(self, value):
        self.__usuario = value

    @property
    def estado(self):   # <--- ESTO ES LO QUE BUSCA EL HTML (v.estado)
        return self.__estado
    @estado.setter
    def estado(self, value):
        self.__estado = value

    @property
    def comprobante(self):
        return self.__comprobante
    @comprobante.setter
    def comprobante(self, value):
        self.__comprobante = value