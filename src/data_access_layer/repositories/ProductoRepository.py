from sqlalchemy.orm import Session
from src.data_access_layer.models.ProductoModel import ProductoModel
from src.data_access_layer.repositories.interfaces.IProductoRepository import IProductoRepository
from uuid import UUID

class ProductoRepository(IProductoRepository):
    def __init__(self, session: Session):
        self._session = session

    def find_all(self):
        return self._session.query(ProductoModel).all()

    def find_by_id(self, id_producto: str):
        # Aseguramos que sea UUID válido
        return self._session.query(ProductoModel).filter_by(id_producto=UUID(id_producto)).first()

    def save(self, producto: ProductoModel):
        self._session.add(producto)
        self._session.commit()
        self._session.refresh(producto)
        return producto
    
    def update(self, producto: ProductoModel):
        # En SQLAlchemy, si el objeto ya está en la sesión, los cambios se guardan al hacer commit
        self._session.merge(producto)
        self._session.commit()
        return producto

    def delete(self, producto: ProductoModel):
        self._session.delete(producto)
        self._session.commit()