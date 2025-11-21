from src.data_access_layer.models.VentaModel import VentaModel
from src.bussines_layer.models.VentaDomainEntity import VentaDomainEntity
from src.bussines_layer.models.DetalleVentaDomainEntity import DetalleVentaDomainEntity
from uuid import UUID

class VentaMapper:
    def toORM(self, entity: VentaDomainEntity) -> VentaModel:
        # Nota: No mapeamos detalles aquí para guardar, se hace manualmente en el servicio por seguridad
        return VentaModel(
            id_venta=UUID(entity.id_venta) if entity.id_venta else None,
            subtotal=entity.subtotal,
            estado_venta_id=UUID(entity.estado_venta_id) if entity.estado_venta_id else None,
            usuario_id=UUID(entity.usuario_id) if entity.usuario_id else None
        )

    def toDomain(self, model: VentaModel) -> VentaDomainEntity:
        detalles_domain = []
        if model.detalles:
            for d in model.detalles:
                detalles_domain.append(DetalleVentaDomainEntity(
                    producto_id=str(d.producto_id),
                    cantidad=d.cantidad,
                    precio_unitario=float(d.precio_unitario),
                    subtotal=float(d.subtotal),
                    nombre_producto=d.producto.nombre if d.producto else "Producto Desconocido"
                ))

        return VentaDomainEntity(
            id_venta=str(model.id_venta),
            subtotal=float(model.subtotal),
            estado_venta_id=str(model.estado_venta_id),
            usuario_id=str(model.usuario_id),
            fecha=model.fecha if hasattr(model, 'fecha') else None, # Asumiendo que agregaste fecha al modelo
            detalles=detalles_domain
        )