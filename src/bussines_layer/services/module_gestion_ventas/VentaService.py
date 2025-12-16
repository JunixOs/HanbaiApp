from decimal import Decimal
from uuid import UUID

from src.bussines_layer.models.VentaDomainEntity import VentaDomainEntity
from src.bussines_layer.services.module_gestion_ventas.interfaces.IVentaService import IVentaService
from src.data_access_layer.models.ProductoModel import ProductoModel
from src.data_access_layer.models.EstadoVentaModel import EstadoVentaModel


class VentaService(IVentaService):

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
        """
        venta_dto = {
            'usuario_id': str,
            'items': [
                {
                    'producto_id': str,
                    'cantidad': int
                }
            ]
        }
        """

        if not venta_dto.get("items"):
            raise Exception("Debe seleccionar al menos un producto")

        try:
            subtotal = Decimal("0.00")
            items_domain = []

            # Estado inicial (PENDIENTE)
            estado_pendiente = (
                self._session
                .query(EstadoVentaModel)
                .filter(EstadoVentaModel.nombre == "Pendiente")
                .first()
            )

            if not estado_pendiente:
                raise Exception("Estado 'Pendiente' no configurado")

            # Procesar items
            for item in venta_dto["items"]:
                producto = self._session.get(
                    ProductoModel,
                    UUID(item["producto_id"])
                )

                if not producto:
                    raise Exception("Producto no encontrado")

                if producto.stock < item["cantidad"]:
                    raise Exception(
                        f"Stock insuficiente para {producto.nombre}"
                    )

                # Descontar stock
                producto.stock -= item["cantidad"]

                precio_unitario = Decimal(producto.precio)
                total_item = precio_unitario * item["cantidad"]
                subtotal += total_item

                items_domain.append({
                    "producto_id": str(producto.id_producto),
                    "cantidad": item["cantidad"],
                    "precio_unitario": precio_unitario
                })

            # Crear dominio
            venta_domain = VentaDomainEntity(
                usuario_id=venta_dto["usuario_id"],
                estado_venta_id=str(estado_pendiente.id_estado_venta),
                items=items_domain,
                subtotal=subtotal
            )

            venta_model = self._venta_mapper.toORM(venta_domain)

            self._session.add(venta_model)
            self._session.flush()   # asegura IDs
            self._session.commit()

            return venta_model

        except Exception as e:
            self._session.rollback()
            raise e
