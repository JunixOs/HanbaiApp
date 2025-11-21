class ReporteDomainEntity:
    def __init__(self, id_reporte=None, nombre=None, formato_archivo=None, url=None, formato_reporte_id=None):
        self.id_reporte = id_reporte
        self.nombre = nombre
        self.formato_archivo = formato_archivo
        self.url = url
        self.formato_reporte_id = formato_reporte_id