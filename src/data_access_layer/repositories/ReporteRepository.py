from sqlalchemy.orm import Session
from src.data_access_layer.models.ReporteModel import ReporteModel

class ReporteRepository:
    def __init__(self, session: Session):
        self._session = session

    def save(self, reporte: ReporteModel):
        self._session.add(reporte)
        self._session.commit()
        return reporte

    def find_all(self):
        return self._session.query(ReporteModel).all()