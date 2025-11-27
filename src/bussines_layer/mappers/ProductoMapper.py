from uuid import UUID
from src.bussines_layer.mappers.interfaces.IProductoMapper import IProductoMapper
from src.data_access_layer.models.ProductoModel import ProductoModel
from src.bussines_layer.models.ProductoDomainEntity import ProductoDomainEntity

class ProductoMapper(IProductoMapper):
    def toORM(self, domain_entity: ProductoDomainEntity) -> ProductoModel:
        return ProductoModel(
            id_producto=UUID(domain_entity.id_producto) if domain_entity.id_producto else None,
            nombre=domain_entity.nombre,
            descripcion=domain_entity.descripcion,
            precio=domain_entity.precio,
            stock=domain_entity.stock,
            descuento_producto=domain_entity.descuento_producto,
            categoria_id=UUID(domain_entity.categoria_id) if domain_entity.categoria_id else None
        )

    def toDomain(self, model: ProductoModel) -> ProductoDomainEntity:
        return ProductoDomainEntity(
            id_producto=str(model.id_producto),
            nombre=model.nombre,
            descripcion=model.descripcion,
            precio=float(model.precio),
            stock=model.stock,
            descuento_producto=float(model.descuento_producto) if model.descuento_producto else 0.0,
            categoria_id=str(model.categoria_id)
        )