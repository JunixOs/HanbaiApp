class DetalleVentaDomainEntity:
    def __init__(self, producto_id, cantidad, precio_unitario, subtotal, nombre_producto=None):
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = subtotal
        self.nombre_producto = nombre_producto # Útil para mostrar en el historial