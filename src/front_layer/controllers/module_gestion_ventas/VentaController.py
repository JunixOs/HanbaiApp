from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from src.data_access_layer.session import get_db_session

# Repositorios
from src.data_access_layer.repositories.VentaRepository import VentaRepository
from src.data_access_layer.repositories.ProductoRepository import ProductoRepository
from src.data_access_layer.models.EstadoVentaModel import EstadoVentaModel

# Servicios y Mappers
from src.bussines_layer.mappers.VentaMapper import VentaMapper
from src.bussines_layer.mappers.ProductoMapper import ProductoMapper
from src.bussines_layer.services.module_gestion_ventas.VentaService import VentaService

venta_controller = Blueprint("venta", __name__, template_folder="templates")

# -------------------------------------------------
# LISTAR VENTAS (MIS COMPRAS / GESTIÓN GLOBAL)
# -------------------------------------------------
@venta_controller.route("/", methods=["GET"])
@login_required
def index():
    with get_db_session() as session:
        venta_repo = VentaRepository(session)
        venta_mapper = VentaMapper()
        service = VentaService(venta_repo, venta_mapper, session)

        rol_name = getattr(current_user, 'rol_name', 'CLIENTE')
        
        # Filtros (para Admin)
        cliente_busqueda = request.args.get('cliente', '').strip()
        estado_busqueda = request.args.get('estado', '')

        if rol_name in ["ADMINISTRADOR", "ENCARGADO_DE_TIENDA"]:
            # Admin ve todas (podrías conectar aquí el find_with_filters si lo tienes en el repo)
            ventas = service.ListarTodas() 
        else:
            # Cliente solo ve sus compras
            ventas = service.ListarPorUsuario(str(current_user.id_usuario))

        estados = session.query(EstadoVentaModel).all()

        return render_template(
            "module_gestion_ventas/VerVentas.html",
            ventas=ventas,
            estados=estados,
            rol_name=rol_name
        )

# -------------------------------------------------
# DETALLE DE VENTA
# -------------------------------------------------
@venta_controller.route("/detalle/<string:id>", methods=["GET"])
@login_required
def detalle(id):
    with get_db_session() as session:
        venta_repo = VentaRepository(session)
        venta_model = venta_repo.findById(id)
        
        if not venta_model:
            flash("Venta no encontrada", "error")
            return redirect(url_for("venta.index"))
        
        # Mapper manual para asegurar carga de datos
        venta_mapper = VentaMapper()
        venta_domain = venta_mapper.toDomain(venta_model)
        
        # Cargar productos desde el comprobante para mostrarlos en la vista
        if venta_model.comprobante and hasattr(venta_model.comprobante, 'producto'):
             venta_domain.items = venta_model.comprobante.producto

        return render_template(
            "module_gestion_ventas/DetalleVenta.html",
            venta=venta_domain,
            rol_name=getattr(current_user, 'rol_name', 'CLIENTE')
        )

# -------------------------------------------------
# NUEVA VENTA (CATÁLOGO DE COMPRA)
# -------------------------------------------------
@venta_controller.route("/create", methods=["GET", "POST"])
@login_required
def create():
    with get_db_session() as session:
        producto_repo = ProductoRepository(session)
        producto_mapper = ProductoMapper()
        # Cargar todos los productos disponibles
        productos = [producto_mapper.toDomain(p) for p in producto_repo.findAll()]

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
                     raise Exception("Tu carrito está vacío. Selecciona al menos un producto.")

                venta_dto = {
                    "usuario_id": str(current_user.id_usuario),
                    "items": items
                }

                service.RegistrarVenta(venta_dto)
                
                flash("Pedido generado correctamente. Ve a 'Mis Compras' para gestionar el pago.", "success")
                return redirect(url_for("venta.index"))

            except Exception as e:
                flash(str(e), "error")

        return render_template(
            "module_gestion_ventas/NuevaVenta.html",
            productos=productos,
            rol_name=current_user.rol_name,
            is_edit=False,
            cantidades_actuales={}
        )

# -------------------------------------------------
# PAGAR VENTA
# -------------------------------------------------
@venta_controller.route("/pagar/<string:id>", methods=["POST"])
@login_required
def pagar(id):
    with get_db_session() as session:
        try:
            venta_repo = VentaRepository(session)
            venta_mapper = VentaMapper()
            service = VentaService(venta_repo, venta_mapper, session)
            
            service.PagarVenta(id, str(current_user.id_usuario))
            flash("¡Pago realizado con éxito! Tu pedido ha sido completado.", "success")
        except Exception as e:
            flash(f"Error al pagar: {str(e)}", "error")
            
    return redirect(url_for("venta.index"))

# -------------------------------------------------
# EDITAR PEDIDO (MODIFICAR CARRITO)
# -------------------------------------------------
@venta_controller.route("/editar/<string:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    with get_db_session() as session:
        venta_repo = VentaRepository(session)
        service = VentaService(venta_repo, VentaMapper(), session)
        producto_repo = ProductoRepository(session)
        
        # Obtener productos para mostrar el catálogo nuevamente
        productos = [ProductoMapper().toDomain(p) for p in producto_repo.findAll()]

        if request.method == "GET":
            # 1. Buscar la venta original
            venta = venta_repo.findById(id)
            if not venta or venta.estado_venta.nombre != 'PENDIENTE':
                flash("No se puede editar este pedido (ya fue pagado o cancelado).", "error")
                return redirect(url_for("venta.index"))

            # 2. Pre-llenar cantidades actuales
            # Creamos un diccionario { 'ID_PRODUCTO': CANTIDAD }
            cantidades = {}
            if venta.comprobante and venta.comprobante.producto:
                for prod in venta.comprobante.producto:
                    pid = str(prod.id_producto)
                    cantidades[pid] = cantidades.get(pid, 0) + 1
            
            # 3. Renderizar la misma vista de NuevaVenta pero en modo edición
            return render_template(
                "module_gestion_ventas/NuevaVenta.html",
                productos=productos,
                rol_name=current_user.rol_name,
                is_edit=True, 
                cantidades_actuales=cantidades
            )

        if request.method == "POST":
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
                     raise Exception("El pedido no puede quedar vacío (cancélalo si deseas).")

                # Llamar al servicio de Modificación
                service.ModificarVenta(id, items, str(current_user.id_usuario))
                
                flash("Pedido actualizado correctamente.", "success")
                return redirect(url_for("venta.index"))

            except Exception as e:
                flash(f"Error al editar: {str(e)}", "error")
                return redirect(url_for("venta.editar", id=id))

# -------------------------------------------------
# CANCELAR VENTA
# -------------------------------------------------
@venta_controller.route("/cancelar/<string:id>", methods=["POST"])
@login_required
def cancelar(id):
    with get_db_session() as session:
        try:
            venta_repo = VentaRepository(session)
            venta_mapper = VentaMapper()
            service = VentaService(venta_repo, venta_mapper, session)
            
            service.CancelarVenta(id, str(current_user.id_usuario))
            
            flash("Pedido cancelado exitosamente.", "success")
        except Exception as e:
            flash(f"Error al cancelar: {str(e)}", "error")

    return redirect(url_for("venta.index"))