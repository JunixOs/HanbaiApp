from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from src.data_access_layer.session import get_db_session
from src.front_layer.controllers.AuthByRol import roles_required

# Repositorios
from src.data_access_layer.repositories.VentaRepository import VentaRepository
from src.data_access_layer.repositories.ProductoRepository import ProductoRepository
from src.data_access_layer.models.EstadoVentaModel import EstadoVentaModel

# Servicios y Mappers
from src.bussines_layer.mappers.VentaMapper import VentaMapper
from src.bussines_layer.mappers.ProductoMapper import ProductoMapper
from src.bussines_layer.services.module_gestion_ventas.VentaService import VentaService

venta_controller = Blueprint(
    "venta",
    __name__,
    template_folder="templates"
)

# -------------------------------------------------
# LISTAR VENTAS
# -------------------------------------------------
@venta_controller.route("/", methods=["GET"])
@login_required
def index():

    with get_db_session() as session:
        venta_repo = VentaRepository(session)
        venta_mapper = VentaMapper()
        service = VentaService(venta_repo, venta_mapper, session)

        # ADMIN ve todo
        if current_user.rol_name == "ADMINISTRADOR":
            ventas = service.ListarTodas()
        else:
            ventas = service.ListarPorUsuario(str(current_user.id_usuario))

        estados = session.query(EstadoVentaModel).all()

        return render_template(
            "module_gestion_ventas/VerVentas.html",
            ventas=ventas,
            estados=estados,
            rol_name=current_user.rol_name,
            user_name=current_user.nombre
        )

# -------------------------------------------------
# REGISTRAR VENTA
# -------------------------------------------------
@venta_controller.route("/create", methods=["GET", "POST"])
@login_required
@roles_required("CLIENTE", "ENCARGADO_DE_TIENDA")
def create():

    with get_db_session() as session:

        producto_repo = ProductoRepository(session)
        producto_mapper = ProductoMapper()
        productos = [
            producto_mapper.toDomain(p)
            for p in producto_repo.findAll()
        ]

        if request.method == "POST":
            venta_repo = VentaRepository(session)
            venta_mapper = VentaMapper()
            service = VentaService(venta_repo, venta_mapper, session)

            try:
                items = []

                for p in productos:
                    cantidad = request.form.get(f"cantidad_{p.id_producto}")
                    if cantidad and int(cantidad) > 0:
                        items.append({
                            "producto_id": p.id_producto,
                            "cantidad": int(cantidad)
                        })

                if not items:
                    raise Exception("Debe seleccionar al menos un producto")

                venta_dto = {
                    "usuario_id": str(current_user.id_usuario),
                    "items": items
                }

                service.RegistrarVenta(venta_dto)

                flash("Venta registrada correctamente", "success")
                return redirect(url_for("venta.index"))

            except Exception as e:
                flash(str(e), "error")

        return render_template(
            "module_gestion_ventas/NuevaVenta.html",
            productos=productos,
            rol_name=current_user.rol_name,
            user_name=current_user.nombre
        )
