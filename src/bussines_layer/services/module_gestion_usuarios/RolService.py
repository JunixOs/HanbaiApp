from src.bussines_layer.services.module_gestion_usuarios.interfaces.IRolService import IRolService
from src.bussines_layer.models.RolDomainEntity import RolDomainEntity
from src.bussines_layer.mappers.interfaces.IRolMapper import IRolMapper

from src.data_access_layer.repositories.interfaces.IRolRepository import IRolRepository


from typing import List

class RolService(IRolService):

    __rol_repository: IRolRepository

    def __init__(self , rol_repository) -> None:
        self.__rol_repository = rol_repository

    def CrearRol(self , rol_domain_entity: RolDomainEntity) -> None:
        self.__rol_repository.save(
            IRolMapper.toORM(rol_domain_entity)
        )

    def EliminarRol(self , id_rol: str) -> bool:
        try:
            self.__rol_repository.deleteById(id_rol)
        except Exception:
            return False
        else:
            return True

    def EditarRol(self , rol_domain_entity: RolDomainEntity) -> bool:
        try:
            self.__rol_repository.save(
                IRolMapper.toORM(rol_domain_entity)
            )
        except Exception:
            return False
        else:
            return True

    def VerTodosLosRoles(self) -> List[RolDomainEntity]:
        return [IRolMapper.toDomain(rol_orm) for rol_orm in self.__rol_repository.findAll()]
    
    def ObtenerRolPorId(self, id_rol: str) -> RolDomainEntity:
        return IRolMapper.toDomain(
            self.__rol_repository.findById(id_rol)
        )