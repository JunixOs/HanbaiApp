from src.bussines_layer.services.module_gestion_usuarios.interfaces.IUsuarioService import IUsuarioService
from src.bussines_layer.mappers.UsuarioMapper import UsuarioMapper
from src.bussines_layer.models.UsuarioDomainEntity import UsuarioDomainEntity
from src.bussines_layer.services.module_gestion_usuarios.BcryptService import BcryptService
from src.bussines_layer.models.UsuarioLogin import UsuarioLogin

from src.data_access_layer.repositories.interfaces.IUsuarioRepository import IUsuarioRepository

from typing import List, Tuple
from flask_login import login_user

class UsuarioService(IUsuarioService):

    __usuario_repository: IUsuarioRepository

    def __init__(
            self , 
            usuario_repository: IUsuarioRepository , 
        ):
        self.__usuario_repository = usuario_repository

    def RegistrarUsuario(self, usuario_domain_entity: UsuarioDomainEntity) -> None:
        usuario_domain_entity.password_hash = BcryptService.HashPassword(usuario_domain_entity.password_hash)

        self.__usuario_repository.save(
            UsuarioMapper.toORM(usuario_domain_entity)
        )

    def IniciarSesion(self , password: str , correo: str) -> Tuple[str , bool]:
        usuario_model = self.__usuario_repository.findByCorreo(correo)

        if(usuario_model is None):
            return "Credenciales incorrectas" , False
        
        usuario_domain_entity = UsuarioMapper.toDomain(usuario_model)

        if(not BcryptService.CheckPassword(password , usuario_domain_entity.password_hash)):
            return "Credenciales incorrectas" , False


        usuario_login = UsuarioLogin()

        usuario_login.id_usuario = str(usuario_model.id_usuario) # type: ignore
        usuario_login.nombre = usuario_model.nombre # type: ignore
        usuario_login.correo = usuario_model.correo # type: ignore
        usuario_login.rol_id = str(usuario_model.rol_id) # type: ignore
        usuario_login.rol_name = usuario_model.rol.nombre

        print(usuario_login.rol_name)

        login_user(
            usuario_login
        )

        return "Sesion iniciada con exito" , True


    def EliminarUsuario(self , id_usuario: str) -> bool:
        try:
            self.__usuario_repository.deleteById(id_usuario)
        except Exception:
            return False
        else:
            return True

    def EditarUsuario(self , usuario_domain_entity_mod: UsuarioDomainEntity) -> bool:
        try:
            usuario_model_in_db = self.__usuario_repository.findByCorreo(usuario_domain_entity_mod.correo)

            if(not usuario_model_in_db):
                return False

            if usuario_model_in_db.nombre != usuario_domain_entity_mod.nombre: # type: ignore
                usuario_model_in_db.nombre = usuario_domain_entity_mod.nombre # type: ignore
            
            if usuario_model_in_db.correo != usuario_domain_entity_mod.correo: # type: ignore
                usuario_model_in_db.correo = usuario_domain_entity_mod.correo # type: ignore

            if not BcryptService.CheckPassword(usuario_domain_entity_mod.password_hash, usuario_model_in_db.password_hash): 
                usuario_model_in_db.password_hash = BcryptService.HashPassword(usuario_domain_entity_mod.password_hash)
            
            if usuario_model_in_db.dni != usuario_domain_entity_mod.dni: # type: ignore
                usuario_model_in_db.dni = usuario_domain_entity_mod.dni # type: ignore

            if usuario_model_in_db.actualizado_en != usuario_domain_entity_mod.actualizado_en: # type: ignore
                usuario_model_in_db.actualizado_en = usuario_domain_entity_mod.actualizado_en # type: ignore

            self.__usuario_repository.save(usuario_model_in_db)

        except Exception:
            return False
        else:
            return True

    def VerTodosLosUsuarios(self) -> List[UsuarioDomainEntity]:
        return [UsuarioMapper.toDomain(usuario_model_in_db) for usuario_model_in_db in self.__usuario_repository.findAll()]
    
    def ObtenerUsuarioPorId(self, id_usuario: str) -> UsuarioDomainEntity:
        return UsuarioMapper.toDomain(
            self.__usuario_repository.findById(id_usuario)
        )