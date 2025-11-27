from typing import List
from src.bussines_layer.models.CategoriaDomainEntity import CategoriaDomainEntity
from src.bussines_layer.services.module_gestion_productos.interfaces.ICategoriaService import ICategoriaService
from src.bussines_layer.mappers.CategoriaMapper import CategoriaMapper
from src.data_access_layer.repositories.interfaces.ICategoriaRepository import ICategoriaRepository

class CategoriaService(ICategoriaService):

    __categoria_repository: ICategoriaRepository

    def __init__(self , categoria_repository: ICategoriaRepository) -> None:
        self.__categoria_repository = categoria_repository

    def ObtenerTodo(self) -> List[CategoriaDomainEntity]:
        return [CategoriaMapper.toDomain(categoria_model) for categoria_model in self.__categoria_repository.findAll()]
    
    def ObtenerPorId(self , id_categoria) -> CategoriaDomainEntity | None:
        return CategoriaMapper.toDomain(
            self.__categoria_repository.findById(id_categoria)
        )
    
    def RegistrarCategoria(self, categoria_domain_entity) -> None:
        self.__categoria_repository.save(
            CategoriaMapper.toORM(categoria_domain_entity)
        )