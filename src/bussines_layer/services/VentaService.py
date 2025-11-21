from src.data_access_layer.session import get_db_session
from src.data_access_layer.repositories.VentaRepository import VentaRepository
from src.data_access_layer.repositories.ProductoRepository import ProductoRepository
from src.data_access_layer.models.VentaModel import VentaModel
from src.data_access_layer.models.DetalleVentaModel import DetalleVentaModel
from src.data_access_layer.models.EstadoVentaModel import EstadoVentaModel
from src.bussines_layer.mappers.VentaMapper import VentaMapper

class VentaService:
    def __init__(self):
        self.mapper = VentaMapper()

    def registrar_venta_compleja(self, usuario_id: str, items_carrito: list):
        """
        items_carrito: [{'producto_id': 'uuid', 'cantidad': int}, ...]
        """
        with get_db_session() as session:
            venta_repo = VentaRepository(session)
            producto_repo = ProductoRepository(session)
            
            nuevo_detalle_venta = []
            total_venta = 0.0
            
            # 1. Validaciones y Cálculos
            for item in items_carrito:
                producto = producto_repo.find_by_id(item['producto_id'])
                
                if not producto:
                    raise Exception(f"Producto con ID {item['producto_id']} no encontrado.")
                
                if producto.stock < int(item['cantidad']):
                    raise Exception(f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}")
                
                precio_real = float(producto.precio)
                cantidad = int(item['cantidad'])
                subtotal_item = precio_real * cantidad
                total_venta += subtotal_item
                
                # RESTAR Stock
                producto.stock -= cantidad
                
                # Crear detalle
                detalle = DetalleVentaModel(
                    producto_id=producto.id_producto,
                    cantidad=cantidad,
                    precio_unitario=precio_real,
                    subtotal=subtotal_item
                )
                nuevo_detalle_venta.append(detalle)

            # 2. Obtener estado 'Completado'
            # Asegúrate de tener este estado en tu BD o cámbialo por uno existente
            estado = session.query(EstadoVentaModel).first() 
            if not estado:
                 raise Exception("No hay estados de venta configurados en el sistema.")

            # 3. Crear Venta Maestra
            nueva_venta = VentaModel(
                usuario_id=usuario_id,
                subtotal=total_venta,
                estado_venta_id=estado.id_estado_venta
            )
            nueva_venta.detalles = nuevo_detalle_venta
            
            venta_repo.save(nueva_venta)
            return nueva_venta.id_venta

    def obtener_historial(self):
        with get_db_session() as session:
            repo = VentaRepository(session)
            ventas = repo.find_all()
            return [self.mapper.toDomain(v) for v in ventas]