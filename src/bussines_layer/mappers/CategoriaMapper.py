from src.bussines_layer.mappers.interfaces.ICategoriaMapper import ICategoriaMapper
from src.data_access_layer.models.CategoriaModel import CategoriaModel
from src.bussines_layer.models.CategoriaDomainEntity import CategoriaDomainEntity

class CategoriaMapper(ICategoriaMapper):

    @staticmethod
    def toORM(categoria_domain_entity: CategoriaDomainEntity) -> CategoriaModel:
        return CategoriaModel(
            nombre=categoria_domain_entity.nombre , 
            descuento_categoria=categoria_domain_entity.descuento_categoria , 
            descripcion=categoria_domain_entity.descripcion
        )
    
    @staticmethod
    def toDomain(categoria_model: CategoriaModel) -> CategoriaDomainEntity:
        categoria_domain_entity: CategoriaDomainEntity = CategoriaDomainEntity()

        categoria_domain_entity.id_categoria = str(categoria_model.id_categoria) # type: ignore
        categoria_domain_entity.nombre = categoria_model.nombre # type: ignore
        categoria_domain_entity.descuento_categoria = float(categoria_model.descuento_categoria) # type: ignore
        categoria_domain_entity.descripcion = categoria_model.descripcion

        return categoria_domain_entity