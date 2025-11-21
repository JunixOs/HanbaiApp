from src.data_access_layer.models.ReporteModel import ReporteModel
from src.bussines_layer.models.ReporteDomainEntity import ReporteDomainEntity
from uuid import UUID

class ReporteMapper:
    def toORM(self, entity: ReporteDomainEntity) -> ReporteModel:
        return ReporteModel(
            id_reporte=UUID(entity.id_reporte) if entity.id_reporte else None,
            nombre=entity.nombre,
            formato_archivo=entity.formato_archivo,
            url=entity.url,
            formato_reporte_id=UUID(entity.formato_reporte_id) if entity.formato_reporte_id else None
        )
    
    def toDomain(self, model: ReporteModel) -> ReporteDomainEntity:
        return ReporteDomainEntity(
            id_reporte=str(model.id_reporte),
            nombre=model.nombre,
            formato_archivo=model.formato_archivo,
            url=model.url,
            formato_reporte_id=str(model.formato_reporte_id)
        )