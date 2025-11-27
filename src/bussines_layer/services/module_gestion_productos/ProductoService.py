from src.data_access_layer.repositories.interfaces.IProductoRepository import IProductoRepository
from src.bussines_layer.mappers.interfaces.IProductoMapper import IProductoMapper
from src.bussines_layer.models.ProductoDomainEntity import ProductoDomainEntity

class ProductoService:
    def __init__(self, repository: IProductoRepository, mapper: IProductoMapper):
        self.repository = repository
        self.mapper = mapper

    def obtener_todos(self, busqueda=None):
        models = self.repository.findAll()
        
        return [self.mapper.toDomain(m) for m in models]

    def obtener_por_id(self, id_producto):
        model = self.repository.findById(id_producto)
        if not model:
            return None
        return self.mapper.toDomain(model)

    def registrar_producto(self, producto_dto):
        nuevo_producto = ProductoDomainEntity(
            nombre=producto_dto['nombre'],
            descripcion=producto_dto['descripcion'],
            precio=producto_dto['precio'],
            stock=producto_dto['stock'],
            categoria_id=producto_dto['categoria_id']
        )
        model = self.mapper.toORM(nuevo_producto)
        self.repository.save(model)

    def actualizar_producto(self, id_producto, producto_dto):
        # 1. Recuperamos el producto existente de la BD
        producto_actual = self.repository.findById(id_producto)
        if not producto_actual:
            return False
        
        # 2. Actualizamos sus campos
        producto_actual.nombre = producto_dto['nombre']
        producto_actual.descripcion = producto_dto['descripcion']
        producto_actual.precio = producto_dto['precio']
        producto_actual.stock = producto_dto['stock']
        # Nota: Si cambias la categoría, recuerda convertir a UUID si es necesario en el repo
        # producto_actual.categoria_id = UUID(producto_dto['categoria_id']) 

        # 3. Guardamos (SQLAlchemy detecta cambios automáticamente al hacer commit)
        self.repository.save(producto_actual)
        return True

    def eliminar_producto(self, id_producto):
        producto = self.repository.findById(id_producto)
        if producto:
            self.repository.delete(producto)
            return True
        return False