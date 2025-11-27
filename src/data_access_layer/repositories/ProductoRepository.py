from uuid import UUID
from sqlalchemy.orm import Session
from typing import List
from src.data_access_layer.repositories.interfaces.IProductoRepository import IProductoRepository
from src.data_access_layer.models.ProductoModel import ProductoModel

class ProductoRepository(IProductoRepository):
    def __init__(self, session: Session):
        self.session = session

    def findAll(self) -> List[ProductoModel]:
        return self.session.query(ProductoModel).all()

    def findById(self, id_producto: str) -> ProductoModel:
        # Manejo de error si el ID no es válido
        try:
            uuid_obj = UUID(id_producto)
            return self.session.query(ProductoModel).filter_by(id_producto=uuid_obj).first()
        except ValueError:
            return None

    # Nuevo: Método para buscar por nombre (HU05)
    def search(self, query: str) -> List[ProductoModel]:
        return self.session.query(ProductoModel).filter(
            ProductoModel.nombre.ilike(f"%{query}%")
        ).all()

    def save(self, producto: ProductoModel) -> None:
        self.session.add(producto)
        self.session.commit()
    
    # Actualizado para recibir el modelo a borrar
    def delete(self, producto: ProductoModel) -> None:
        self.session.delete(producto)
        self.session.commit()