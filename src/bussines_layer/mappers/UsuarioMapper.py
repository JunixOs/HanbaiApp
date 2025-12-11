from src.bussines_layer.mappers.interfaces.IUsuarioMapper import IUsuarioMapper
from src.data_access_layer.models.UsuarioModel import UsuarioModel
from src.bussines_layer.models.UsuarioDomainEntity import UsuarioDomainEntity

from uuid import UUID

class UsuarioMapper(IUsuarioMapper):

    @staticmethod
    def toORM(usuario_domain_entity: UsuarioDomainEntity) -> UsuarioModel:
        model = UsuarioModel(
            nombre=usuario_domain_entity.nombre, 
            correo=usuario_domain_entity.correo,
            password_hash=usuario_domain_entity.password_hash, 
            dni=usuario_domain_entity.dni,
            # Aseguramos compatibilidad con timestamps o datetime
            creado_en=usuario_domain_entity.creado_en,
            actualizado_en=usuario_domain_entity.actualizado_en,
            rol_id=UUID(usuario_domain_entity.rol_id) if usuario_domain_entity.rol_id else None
        )
        
        # Si tienes el ID en el dominio, lo asignamos al modelo
        if usuario_domain_entity.id_usuario:
            model.id_usuario = UUID(usuario_domain_entity.id_usuario)
            
        return model
    
    @staticmethod
    def toDomain(usuario_model: UsuarioModel) -> UsuarioDomainEntity:
        usuario_domain_entity: UsuarioDomainEntity = UsuarioDomainEntity()

        usuario_domain_entity.id_usuario = str(usuario_model.id_usuario)
        usuario_domain_entity.nombre = usuario_model.nombre
        usuario_domain_entity.correo = usuario_model.correo
        usuario_domain_entity.password_hash = usuario_model.password_hash
        usuario_domain_entity.dni = usuario_model.dni
        
        # Manejo robusto de fechas (si vienen como datetime o float)
        if hasattr(usuario_model.creado_en, 'timestamp'):
            usuario_domain_entity.creado_en = usuario_model.creado_en.timestamp()
        else:
            usuario_domain_entity.creado_en = usuario_model.creado_en

        if hasattr(usuario_model.actualizado_en, 'timestamp'):
            usuario_domain_entity.actualizado_en = usuario_model.actualizado_en.timestamp()
        else:
            usuario_domain_entity.actualizado_en = usuario_model.actualizado_en
            
        usuario_domain_entity.rol_id = str(usuario_model.rol_id)

        # --- CORRECCIÓN CLAVE ---
        # Aquí extraemos el nombre del rol desde la relación en el modelo
        if usuario_model.rol:
            usuario_domain_entity.rol_nombre = usuario_model.rol.nombre
        else:
            usuario_domain_entity.rol_nombre = "Sin Rol Asignado"

        return usuario_domain_entity