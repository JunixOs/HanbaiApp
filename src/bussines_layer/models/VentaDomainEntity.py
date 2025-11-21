from typing import List
from src.bussines_layer.models.DetalleVentaDomainEntity import DetalleVentaDomainEntity

class VentaDomainEntity:
    def __init__(self, id_venta=None, subtotal=0.0, estado_venta_id=None, usuario_id=None, fecha=None, detalles: List[DetalleVentaDomainEntity] = None):
        self.id_venta = id_venta
        self.subtotal = subtotal
        self.estado_venta_id = estado_venta_id
        self.usuario_id = usuario_id
        self.fecha = fecha
        self.detalles = detalles if detalles is not None else []