from src.bussines_layer.models.RolDomainEntity import RolDomainEntity
from src.data_access_layer.models.RolModel import RolModel
from src.bussines_layer.mappers.interfaces.IRolMapper import IRolMapper


class RolMapper(IRolMapper):
    @staticmethod
    def toORM(rol_domain_entity: RolDomainEntity) -> RolModel:
        return RolModel(
            id_rol = rol_domain_entity.id_rol , 
            nombre = rol_domain_entity.nombre , 
            descripcion = rol_domain_entity.descripcion , 
            creado_en = rol_domain_entity.creado_en , 
            actualizado_en = rol_domain_entity.actualizado_en
        )

    @staticmethod
    def toDomain(rol_model: RolModel) -> RolDomainEntity:
        rol_domain_entity: RolDomainEntity = RolDomainEntity()

        rol_domain_entity.id_rol = str(rol_model.id_rol)
        rol_domain_entity.nombre = rol_model.nombre # type: ignore
        rol_domain_entity.descripcion = rol_model.descripcion # type: ignore
        rol_domain_entity.creado_en = rol_model.creado_en.timestamp()
        rol_domain_entity.actualizado_en = rol_model.actualizado_en.timestamp()

        return rol_domain_entity