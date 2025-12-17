from src.data_access_layer.repositories.ProductoRepository import ProductoRepository
from src.bussines_layer.services.module_gestion_productos.ProductoService import ProductoService

class BuildProductoService:
    @staticmethod
    def build():
        # Inyectamos el repositorio al servicio
        producto_repository = ProductoRepository()
        producto_service = ProductoService(producto_repository)
        return producto_service