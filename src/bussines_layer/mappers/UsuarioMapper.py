from src.bussines_layer.mappers.interfaces.IUsuarioMapper import IUsuarioMapper
from src.data_access_layer.models.UsuarioModel import UsuarioModel
from src.bussines_layer.models.UsuarioDomainEntity import UsuarioDomainEntity

from uuid import UUID

class UsuarioMapper(IUsuarioMapper):

    def toORM(self, usuario_domain_entity: UsuarioDomainEntity) -> UsuarioModel:
        return UsuarioModel(
            nombre=usuario_domain_entity.nombre , 
            correo=usuario_domain_entity.correo,
            password_hash=usuario_domain_entity.password_hash , 
            dni=usuario_domain_entity.dni,
            creado_en=usuario_domain_entity.creado_en,
            actualizado_en=usuario_domain_entity.actualizado_en,
            rol_id=UUID(usuario_domain_entity.rol_id)
        )
    
    def toDomain(self, usuario_model: UsuarioModel) -> UsuarioDomainEntity:
        usuario_domain_entity: UsuarioDomainEntity = UsuarioDomainEntity()

        usuario_domain_entity.id_usuario = str(usuario_model.id_usuario)
        usuario_domain_entity.nombre = usuario_model.nombre # type: ignore
        usuario_domain_entity.correo = usuario_model.correo # type: ignore
        usuario_domain_entity.password_hash = usuario_model.password_hash # type: ignore
        usuario_domain_entity.dni = usuario_model.dni # type: ignore
        usuario_domain_entity.creado_en = usuario_model.creado_en.timestamp() # type: ignore
        usuario_domain_entity.actualizado_en = usuario_model.actualizado_en.timestamp()
        usuario_domain_entity.rol_id = str(usuario_model.rol_id)

        return usuario_domain_entity