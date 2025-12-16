from uuid import UUID
from src.bussines_layer.mappers.interfaces.IVentaMapper import IVentaMapper
from src.data_access_layer.models.VentaModel import VentaModel
from src.bussines_layer.models.VentaDomainEntity import VentaDomainEntity

class VentaMapper(IVentaMapper):

    def toORM(self, domain: VentaDomainEntity) -> VentaModel:
        return VentaModel(
            id_venta=UUID(domain.id_venta) if domain.id_venta else None,
            subtotal=domain.subtotal,
            usuario_id=UUID(domain.usuario_id),
            estado_venta_id=UUID(domain.estado_venta_id)
        )

    def toDomain(self, model: VentaModel) -> VentaDomainEntity:
        return VentaDomainEntity(
            id_venta=str(model.id_venta),
            subtotal=model.subtotal,
            usuario_id=str(model.usuario_id),
            estado_venta_id=str(model.estado_venta_id)
        )
