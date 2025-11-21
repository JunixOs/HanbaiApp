from src.data_access_layer.session import get_db_session
from src.data_access_layer.repositories.ReporteRepository import ReporteRepository
from src.bussines_layer.mappers.ReporteMapper import ReporteMapper
from src.bussines_layer.models.ReporteDomainEntity import ReporteDomainEntity
import datetime

class ReporteService:
    def __init__(self):
        self.mapper = ReporteMapper()

    def generar_reporte_ventas(self, formato="PDF"):
        # Lógica simulada de generación de archivo
        nombre_archivo = f"Reporte_Ventas_{datetime.date.today()}.{formato.lower()}"
        url_ficticia = f"/static/reports/{nombre_archivo}"
        
        reporte_dto = ReporteDomainEntity(
            nombre=nombre_archivo,
            formato_archivo=formato,
            url=url_ficticia,
            formato_reporte_id="UUID-DEL-FORMATO-GENERAL" # Debería venir de una constante o búsqueda
        )
        
        with get_db_session() as session:
            repo = ReporteRepository(session)
            repo.save(self.mapper.toORM(reporte_dto))
            return url_ficticia