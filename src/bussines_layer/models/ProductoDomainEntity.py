class ProductoDomainEntity:
    def __init__(self, id_producto=None, nombre=None, descripcion=None, precio=0.0, stock=0, categoria_id=None):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.categoria_id = categoria_id

    # Puedes agregar lógica de dominio aquí, ej: verificar si hay stock bajo
    def tiene_stock_bajo(self, umbral=5):
        return self.stock <= umbral