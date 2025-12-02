import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.data_access_layer.session import get_db_session
from src.data_access_layer.repositories.ProductoRepository import ProductoRepository
from src.bussines_layer.mappers.ProductoMapper import ProductoMapper
from src.bussines_layer.services.module_gestion_productos.ProductoService import ProductoService
# Necesitarás esto para cargar categorías en los select
from src.data_access_layer.models.CategoriaModel import CategoriaModel 

from src.front_layer.controllers.AuthByRol import roles_required

from flask_login import current_user

template_dir = os.path.abspath("src/front_layer/templates/module_gestion_productos")
producto_controller = Blueprint('producto', __name__, template_folder=template_dir)

@producto_controller.route("/", methods=['GET'])
def index():
    # Solo capturamos lo que el formulario simplificado envía
    filtros = {
        'q': request.args.get('q'),
        'categoria': request.args.get('categoria')
    }

    with get_db_session() as session:
        repo = ProductoRepository(session)
        mapper = ProductoMapper()
        service = ProductoService(repo, mapper)
        
        # El servicio sigue soportando filtros, si vienen vacíos no pasa nada
        productos = service.obtener_catalogo(filtros)
        
        categorias = session.query(CategoriaModel).all()

        # Variables de sesión para la vista
        rol_name = None
        user_name = None
        authenticated = False
        
        if current_user.is_authenticated:
            rol_name = current_user.rol_name.strip().lower()
            user_name = current_user.nombre
            authenticated = True

        return render_template(
            "module_gestion_productos/list.html", 
            productos=productos, 
            categorias=categorias, 
            filtros=filtros,
            rol_name=rol_name, 
            user_name=user_name, 
            authenticated=authenticated
        )

@producto_controller.route("/create", methods=['GET', 'POST'])
@roles_required("ENCARGADO_DE_TIENDA")
def create():
    with get_db_session() as session:
        repo = ProductoRepository(session)
        mapper = ProductoMapper()
        service = ProductoService(repo, mapper)
        
        if request.method == 'POST':
            data = {
                'nombre': request.form['nombre'],
                'descripcion': request.form['descripcion'],
                'precio': float(request.form['precio']),
                'stock': int(request.form['stock']),
                'categoria_id': request.form['categoria_id']
            }
            service.registrar_producto(data)
            # flash('Producto creado exitosamente', 'success') # Requiere secret_key en app
            return redirect(url_for('producto.index'))
        
        categorias = session.query(CategoriaModel).all()
        return render_template("create.html", categorias=categorias)

@producto_controller.route("/edit/<id>", methods=['GET', 'POST'])
@roles_required("ENCARGADO_DE_TIENDA")
def edit(id):
    with get_db_session() as session:
        repo = ProductoRepository(session)
        mapper = ProductoMapper()
        service = ProductoService(repo, mapper)

        if request.method == 'POST':
            data = {
                'nombre': request.form['nombre'],
                'descripcion': request.form['descripcion'],
                'precio': float(request.form['precio']),
                'stock': int(request.form['stock']),
                # 'categoria_id': ... (si implementas cambio de categoría)
            }
            service.actualizar_producto(id, data)
            return redirect(url_for('producto.index'))

        producto = service.obtener_por_id(id)
        categorias = session.query(CategoriaModel).all()
        return render_template("edit.html", producto=producto, categorias=categorias)

@producto_controller.route("/delete/<id>", methods=['POST'])
def delete(id):
    with get_db_session() as session:
        repo = ProductoRepository(session)
        mapper = ProductoMapper()
        service = ProductoService(repo, mapper)
        service.eliminar_producto(id)
        return redirect(url_for('producto.index'))