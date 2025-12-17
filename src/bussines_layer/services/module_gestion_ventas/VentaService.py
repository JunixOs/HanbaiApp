from decimal import Decimal
from uuid import UUID

from src.bussines_layer.models.VentaDomainEntity import VentaDomainEntity
# Si usas interfaz, descomenta:
from src.bussines_layer.services.module_gestion_ventas.interfaces.IVentaService import IVentaService
from src.data_access_layer.models.ProductoModel import ProductoModel
from src.data_access_layer.models.EstadoVentaModel import EstadoVentaModel
from src.data_access_layer.models.ComprobanteModel import ComprobanteModel

class VentaService:

    def __init__(self, venta_repository, venta_mapper, session):
        self._venta_repository = venta_repository
        self._venta_mapper = venta_mapper
        self._session = session

    # -------------------------------------------------
    # LISTADOS
    # -------------------------------------------------
    def ListarTodas(self):
        ventas = self._venta_repository.findAll()
        return [self._venta_mapper.toDomain(v) for v in ventas]

    def ListarPorUsuario(self, usuario_id):
        ventas = self._venta_repository.findByUsuario(usuario_id)
        return [self._venta_mapper.toDomain(v) for v in ventas]

    # -------------------------------------------------
    # REGISTRAR VENTA
    # -------------------------------------------------
    def RegistrarVenta(self, venta_dto: dict):
        if not venta_dto.get("items"):
            raise Exception("Debe seleccionar al menos un producto")

        try:
            subtotal = Decimal("0.00")
            items_procesados = [] 

            # Buscar estado PENDIENTE
            estado_pendiente = (
                self._session.query(EstadoVentaModel)
                .filter(EstadoVentaModel.nombre == "PENDIENTE")
                .first()
            )
            # Fallback por si no existe o difiere mayúsculas
            if not estado_pendiente:
                estado_pendiente = self._session.query(EstadoVentaModel).first()

            if not estado_pendiente:
                raise Exception("Estado 'PENDIENTE' no configurado en BD")

            # Procesar items
            for item in venta_dto["items"]:
                producto = self._session.get(ProductoModel, UUID(item["producto_id"]))

                if not producto:
                    raise Exception("Producto no encontrado")

                if producto.stock < item["cantidad"]:
                    raise Exception(f"Stock insuficiente para {producto.nombre}")

                # Descontar stock
                producto.stock -= item["cantidad"]

                precio_unitario = Decimal(producto.precio)
                subtotal += precio_unitario * item["cantidad"]

                # Agregar a lista para relacionar con comprobante
                for _ in range(item["cantidad"]):
                    items_procesados.append(producto)

            # Crear Venta
            venta_domain = VentaDomainEntity(
                usuario_id=venta_dto["usuario_id"],
                estado_venta_id=str(estado_pendiente.id_estado_venta),
                subtotal=subtotal
            )
            venta_model = self._venta_mapper.toORM(venta_domain)

            self._session.add(venta_model)
            self._session.flush() # Obtener ID

            # Crear Comprobante
            if items_procesados:
                comprobante = ComprobanteModel(
                    venta_id=venta_model.id_venta,
                    total=subtotal,
                    lugar_venta="Web"
                )
                for prod in items_procesados:
                    comprobante.producto.append(prod)
                
                self._session.add(comprobante)

            self._session.commit()
            return venta_model

        except Exception as e:
            self._session.rollback()
            raise e

    # -------------------------------------------------
    # PAGAR VENTA (Simulación)
    # -------------------------------------------------
    def PagarVenta(self, id_venta, id_usuario):
        venta = self._venta_repository.findById(id_venta)
        if not venta:
            raise Exception("Venta no encontrada")
        
        # Validar que sea del usuario (si aplica lógica de seguridad aquí)
        # if str(venta.usuario_id) != id_usuario: raise Exception("No autorizado")

        if venta.estado_venta.nombre != 'PENDIENTE':
            raise Exception("Solo se pueden pagar pedidos pendientes.")

        try:
            # Buscar estado COMPLETADA
            estado_ok = (
                self._session.query(EstadoVentaModel)
                .filter(EstadoVentaModel.nombre == "COMPLETADA")
                .first()
            )
            if not estado_ok:
                raise Exception("Estado 'COMPLETADA' no configurado en BD")

            # Actualizar estado
            venta.estado_venta_id = estado_ok.id_estado_venta
            self._session.commit()
            return True

        except Exception as e:
            self._session.rollback()
            raise e

    # -------------------------------------------------
    # MODIFICAR VENTA (Editar Pedido)
    # -------------------------------------------------
    def ModificarVenta(self, id_venta, nuevos_items, id_usuario):
        venta = self._venta_repository.findById(id_venta)
        if not venta:
            raise Exception("Venta no encontrada")
        
        if venta.estado_venta.nombre != 'PENDIENTE':
            raise Exception("Solo se pueden editar pedidos pendientes.")

        try:
            # 1. RESTAURAR STOCK ANTIGUO
            # Devolvemos al inventario todo lo que tenía el pedido antes
            if venta.comprobante and venta.comprobante.producto:
                for prod in venta.comprobante.producto:
                    prod.stock += 1
                
                # Limpiamos la lista de productos del comprobante actual
                venta.comprobante.producto = []
            
            # 2. PROCESAR NUEVOS ITEMS
            subtotal = Decimal("0.00")
            items_procesados = []

            for item in nuevos_items:
                producto = self._session.get(ProductoModel, UUID(item["producto_id"]))
                
                if not producto:
                    raise Exception(f"Producto {item['producto_id']} no encontrado")

                # Validar stock (ahora el stock incluye lo que acabamos de restaurar)
                if producto.stock < item["cantidad"]:
                    raise Exception(f"Stock insuficiente para {producto.nombre} (Disp: {producto.stock})")

                # Descontar nuevo stock
                producto.stock -= item["cantidad"]
                
                precio_unitario = Decimal(producto.precio)
                subtotal += precio_unitario * item["cantidad"]

                for _ in range(item["cantidad"]):
                    items_procesados.append(producto)

            # 3. ACTUALIZAR VENTA Y COMPROBANTE
            venta.subtotal = subtotal
            
            # Actualizamos el comprobante existente
            if venta.comprobante:
                venta.comprobante.total = subtotal
                for p in items_procesados:
                    venta.comprobante.producto.append(p)
            else:
                # Si por error no tenía comprobante, creamos uno
                nuevo_comp = ComprobanteModel(
                    venta_id=venta.id_venta,
                    total=subtotal,
                    lugar_venta="Web - Editado"
                )
                for p in items_procesados:
                    nuevo_comp.producto.append(p)
                self._session.add(nuevo_comp)

            self._session.commit()
            return True

        except Exception as e:
            self._session.rollback()
            raise e

    # -------------------------------------------------
    # CANCELAR VENTA
    # -------------------------------------------------
    def CancelarVenta(self, id_venta, id_usuario_solicitante):
        venta = self._venta_repository.findById(id_venta)
        
        if not venta:
            raise Exception("Venta no encontrada.")
        
        if not venta.estado_venta or venta.estado_venta.nombre.upper() != 'PENDIENTE':
            raise Exception("Solo se pueden cancelar ventas PENDIENTES.")

        try:
            # Buscar Estado CANCELADO
            estado_cancelado = (
                self._session.query(EstadoVentaModel)
                .filter(EstadoVentaModel.nombre.ilike("CANCELADO"))
                .first()
            )
            if not estado_cancelado:
                raise Exception("Estado 'CANCELADO' no configurado.")

            # RESTAURAR STOCK
            if venta.comprobante and venta.comprobante.producto:
                for producto in venta.comprobante.producto:
                    producto.stock += 1

            # Cambiar estado
            venta.estado_venta_id = estado_cancelado.id_estado_venta
            
            self._session.commit()
            return True

        except Exception as e:
            self._session.rollback()
            raise e