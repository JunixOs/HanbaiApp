class ProductoDomainEntity:
    def __init__(self, id_producto=None, nombre=None, descripcion=None, precio=0.0, stock=0, descuento_producto=0.0, categoria_id=None):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.descuento_producto = descuento_producto
        self.categoria_id = categoria_id

    def calcular_precio_final(self):
        if self.descuento_producto:
            return self.precio * (1 - (self.descuento_producto / 100))
        return self.precio

    # --- REGLAS DE NEGOCIO PARA ALERTAS (HU18) ---
    def es_stock_critico(self) -> bool:
        return self.stock <= 5

    def es_stock_bajo(self) -> bool:
        return 5 < self.stock <= 20