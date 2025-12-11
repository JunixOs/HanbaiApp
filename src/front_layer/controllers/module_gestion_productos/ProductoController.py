from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from src.data_access_layer.session import get_db_session
from src.front_layer.controllers.AuthByRol import roles_required 

# Repositorios y Servicios
from src.data_access_layer.repositories.ProductoRepository import ProductoRepository
from src.data_access_layer.models.CategoriaModel import CategoriaModel
from src.bussines_layer.mappers.ProductoMapper import ProductoMapper
from src.bussines_layer.services.module_gestion_productos.ProductoService import ProductoService

producto_controller = Blueprint('producto', __name__, template_folder='templates')

@producto_controller.route("/", methods=['GET'])
@login_required
def index():
    filtros = {
        'q': request.args.get('q'),
        'categoria': request.args.get('categoria')
    }

    with get_db_session() as session:
        repo = ProductoRepository(session)
        mapper = ProductoMapper()
        service = ProductoService(repo, mapper)
        
        productos = service.obtener_catalogo(filtros)
        categorias = session.query(CategoriaModel).all()

        # DATOS DE SESIÓN PARA LA VISTA
        rol_name = current_user.rol_name if current_user.is_authenticated else None
        user_name = current_user.nombre if current_user.is_authenticated else "Usuario" # <--- CORRECCIÓN

        return render_template(
            "module_gestion_productos/VerProductos.html", 
            productos=productos,
            categorias=categorias, 
            filtros=filtros,
            rol_name=rol_name,
            user_name=user_name # <--- PASAMOS EL NOMBRE A LA VISTA
        )

# ... (El resto de funciones create, edit, delete se mantienen igual que la versión anterior) ...
@producto_controller.route("/create", methods=['GET', 'POST'])
@roles_required("ADMINISTRADOR", "ENCARGADO_DE_TIENDA")
def create():
    with get_db_session() as session:
        if request.method == 'POST':
            repo = ProductoRepository(session)
            mapper = ProductoMapper()
            service = ProductoService(repo, mapper)
            
            data = {
                'nombre': request.form.get('nombre'),
                'descripcion': request.form.get('descripcion'),
                'precio': float(request.form.get('precio')),
                'stock': int(request.form.get('stock')),
                'categoria_id': request.form.get('categoria_id')
            }
            
            try:
                service.registrar_producto(data)
                flash('Producto creado exitosamente.', 'success')
                return redirect(url_for('producto.index'))
            except Exception as e:
                flash(f'Error al crear: {str(e)}', 'error')

        categorias = session.query(CategoriaModel).all()
        return render_template("module_gestion_productos/RegistrarProducto.html", categorias=categorias)

@producto_controller.route("/edit/<id>", methods=['GET', 'POST'])
@roles_required("ADMINISTRADOR", "ENCARGADO_DE_TIENDA")
def edit(id):
    with get_db_session() as session:
        repo = ProductoRepository(session)
        mapper = ProductoMapper()
        service = ProductoService(repo, mapper)

        if request.method == 'POST':
            data = {
                'nombre': request.form.get('nombre'),
                'descripcion': request.form.get('descripcion'),
                'precio': float(request.form.get('precio')),
                'stock': int(request.form.get('stock')),
                'categoria_id': request.form.get('categoria_id')
            }
            if service.actualizar_producto(id, data):
                flash('Producto actualizado.', 'success')
                return redirect(url_for('producto.index'))
            
        producto = service.obtener_por_id(id)
        categorias = session.query(CategoriaModel).all()
        
        return render_template("module_gestion_productos/EditarProducto.html", producto=producto, categorias=categorias)

@producto_controller.route("/delete/<id>", methods=['POST'])
@roles_required("ADMINISTRADOR", "ENCARGADO_DE_TIENDA")
def delete(id):
    with get_db_session() as session:
        repo = ProductoRepository(session)
        mapper = ProductoMapper()
        service = ProductoService(repo, mapper)
        
        if service.eliminar_producto(id):
            flash('Producto eliminado.', 'success')
        else:
            flash('Error al eliminar.', 'error')
            
        return redirect(url_for('producto.index'))