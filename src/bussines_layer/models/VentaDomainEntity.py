from decimal import Decimal

class VentaDomainEntity:
    def __init__(
        self,
        id_venta=None,
        subtotal=Decimal("0.00"),
        usuario_id=None,
        estado_venta_id=None,
        items=None
    ):
        self.id_venta = id_venta
        self.subtotal = subtotal
        self.usuario_id = usuario_id
        self.estado_venta_id = estado_venta_id
        self.items = items or []  # Detalle de venta

    # --- REGLA DE NEGOCIO ---
    def calcular_subtotal(self):
        total = Decimal("0.00")
        for item in self.items:
            total += item['precio_unitario'] * item['cantidad']
        self.subtotal = total
        return self.subtotal

    def es_venta_vacia(self) -> bool:
        return len(self.items) == 0
