from src.bussines_layer.models.VentaDomainEntity import VentaDomainEntity
from src.data_access_layer.models.VentaModel import VentaModel

class VentaMapper:
    
    def toDomain(self, model: VentaModel) -> VentaDomainEntity:
        if not model:
            return None

        # Creamos la entidad básica
        entity = VentaDomainEntity(
            id_venta=model.id_venta,
            subtotal=model.subtotal,
            estado_venta_id=model.estado_venta_id,
            usuario_id=model.usuario_id
        )

        # --- MAPEO DE RELACIONES ---
        # Asignamos los objetos completos para usarlos en el HTML
        
        # 1. Estado (v.estado.nombre)
        # SQLAlchemy suele llamar a la relación igual que la tabla o definido en el modelo
        if hasattr(model, 'estado_venta'): 
            entity.estado = model.estado_venta
        
        # 2. Usuario (v.usuario.nombre)
        if hasattr(model, 'usuario'):
            entity.usuario = model.usuario

        # 3. Comprobante (v.comprobante.fecha_venta)
        # VentaModel tiene una relación 'comprobante' (usualmente uselist=False)
        if hasattr(model, 'comprobante'):
            entity.comprobante = model.comprobante

        return entity

    def toORM(self, domain: VentaDomainEntity) -> VentaModel:
        if not domain:
            return None
            
        return VentaModel(
            id_venta=domain.id_venta,
            subtotal=domain.subtotal,
            estado_venta_id=domain.estado_venta_id,
            usuario_id=domain.usuario_id
        )