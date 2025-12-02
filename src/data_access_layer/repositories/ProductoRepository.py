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
        try:
            uuid_obj = UUID(id_producto)
            return self.session.query(ProductoModel).filter_by(id_producto=uuid_obj).first()
        except ValueError:
            return None

    def save(self, producto: ProductoModel) -> None:
        self.session.add(producto)
        self.session.commit()
    
    def delete(self, producto: ProductoModel) -> None:
        self.session.delete(producto)
        self.session.commit()

    # --- NUEVO MÉTODO PARA FILTRADO (HU05) ---
    def find_with_filters(self, nombre: str = None, categoria_id: str = None) -> List[ProductoModel]:
        query = self.session.query(ProductoModel)

        if nombre:
            # ilike para búsqueda insensible a mayúsculas
            query = query.filter(ProductoModel.nombre.ilike(f"%{nombre}%"))
        
        if categoria_id:
            try:
                uuid_cat = UUID(categoria_id)
                query = query.filter(ProductoModel.categoria_id == uuid_cat)
            except ValueError:
                pass # Ignoramos ID inválido (ej: cadena vacía)
        
        # Eliminada la lógica de precios que ya no se usa
        return query.all()