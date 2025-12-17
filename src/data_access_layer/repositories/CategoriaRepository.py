from sqlalchemy.orm import Session
from src.data_access_layer.models.CategoriaModel import CategoriaModel
import uuid

class CategoriaRepository:
    def __init__(self, session: Session):
        self.session = session

    def findAll(self):
        return self.session.query(CategoriaModel).all()

    def findById(self, id_categoria):
        return self.session.query(CategoriaModel).get(id_categoria)

    # --- NUEVOS MÉTODOS NECESARIOS ---
    def findByNombre(self, nombre: str):
        """Busca una categoría por su nombre exacto (case insensitive si quieres)"""
        return self.session.query(CategoriaModel).filter(CategoriaModel.nombre.ilike(nombre)).first()

    def save(self, categoria: CategoriaModel):
        self.session.add(categoria)
        self.session.commit()
        # Refrescamos para tener el ID disponible inmediatamente
        self.session.refresh(categoria)
        return categoria