from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from src.data_access_layer.session import get_db_session
from src.front_layer.controllers.AuthByRol import roles_required 
import uuid

# Repositorios y Servicios
from src.data_access_layer.repositories.ProductoRepository import ProductoRepository
from src.data_access_layer.repositories.CategoriaRepository import CategoriaRepository
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

        rol_name = current_user.rol_name if current_user.is_authenticated else None
        user_name = current_user.nombre if current_user.is_authenticated else "Usuario"

        return render_template(
            "module_gestion_productos/VerProductos.html", 
            productos=productos,
            categorias=categorias, 
            filtros=filtros,
            rol_name=rol_name,
            user_name=user_name
        )

# --------------------------------------------------------------------------
# CREAR PRODUCTO (CORREGIDO)
# --------------------------------------------------------------------------
@producto_controller.route("/create", methods=['GET', 'POST'])
@roles_required("ADMINISTRADOR", "ENCARGADO_DE_TIENDA")
def create():
    with get_db_session() as session:
        categoria_repo = CategoriaRepository(session)

        if request.method == 'POST':
            prod_repo = ProductoRepository(session)
            mapper = ProductoMapper()
            service = ProductoService(prod_repo, mapper)
            
            # 1. DETECTAR SI ES NUEVA CATEGORÍA
            nueva_categoria_nombre = request.form.get("nueva_categoria_input", "").strip()
            categoria_id_final = None

            if nueva_categoria_nombre:
                # El usuario escribió una nueva
                cat_existente = categoria_repo.findByNombre(nueva_categoria_nombre)
                
                if cat_existente:
                    # Si ya existe, usamos su ID (convertido a string)
                    categoria_id_final = str(cat_existente.id_categoria)
                else:
                    # Crear nueva categoría
                    nueva_cat = CategoriaModel(
                        id_categoria=uuid.uuid4(),
                        nombre=nueva_categoria_nombre,
                        descripcion="Creada desde gestión de productos"
                    )
                    categoria_repo.save(nueva_cat)
                    
                    # CORRECCIÓN AQUÍ: Convertimos el objeto UUID a string
                    categoria_id_final = str(nueva_cat.id_categoria)
                    
                    flash(f"Categoría '{nueva_categoria_nombre}' creada correctamente.", "info")
            else:
                # El usuario seleccionó una existente (Ya viene como string del HTML)
                categoria_id_final = request.form.get('categoria_id')

            # 2. PREPARAR DATOS DEL PRODUCTO
            try:
                if not categoria_id_final:
                    raise Exception("Debes seleccionar o crear una categoría.")

                data = {
                    'nombre': request.form.get('nombre'),
                    'descripcion': request.form.get('descripcion'),
                    'precio': float(request.form.get('precio')),
                    'stock': int(request.form.get('stock')),
                    'categoria_id': categoria_id_final # Ahora siempre es string
                }
            
                service.registrar_producto(data)
                flash('Producto creado exitosamente.', 'success')
                return redirect(url_for('producto.index'))

            except Exception as e:
                flash(f'Error al crear: {str(e)}', 'error')

        # Si es GET o hubo error, recargamos las categorías
        categorias = categoria_repo.findAll()
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