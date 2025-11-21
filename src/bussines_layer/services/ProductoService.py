from src.data_access_layer.session import get_db_session
from src.data_access_layer.repositories.ProductoRepository import ProductoRepository
from src.bussines_layer.mappers.ProductoMapper import ProductoMapper
from src.bussines_layer.models.ProductoDomainEntity import ProductoDomainEntity

class ProductoService:
    def __init__(self):
        self.mapper = ProductoMapper()

    def obtener_todos(self):
        with get_db_session() as session:
            repo = ProductoRepository(session)
            productos = repo.find_all()
            return [self.mapper.toDomain(p) for p in productos]

    def obtener_por_id(self, id_producto: str):
        with get_db_session() as session:
            repo = ProductoRepository(session)
            producto = repo.find_by_id(id_producto)
            if not producto:
                return None
            return self.mapper.toDomain(producto)

    def crear_producto(self, producto_dto: ProductoDomainEntity):
        if producto_dto.precio < 0:
            raise ValueError("El precio no puede ser negativo")
        
        with get_db_session() as session:
            repo = ProductoRepository(session)
            repo.save(self.mapper.toORM(producto_dto))
            return True

    def actualizar_producto(self, producto_dto: ProductoDomainEntity):
        with get_db_session() as session:
            repo = ProductoRepository(session)
            # Convertimos a ORM para que SQLAlchemy maneje la actualización
            producto_orm = self.mapper.toORM(producto_dto)
            repo.update(producto_orm)
            return True

    def eliminar_producto(self, id_producto: str):
        with get_db_session() as session:
            repo = ProductoRepository(session)
            producto = repo.find_by_id(id_producto)
            if producto:
                repo.delete(producto)
                return True
            return False