import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.data_access_layer.session import get_db_session
from src.data_access_layer.repositories.ProductoRepository import ProductoRepository
from src.bussines_layer.mappers.ProductoMapper import ProductoMapper
from src.bussines_layer.services.module_gestion_productos.ProductoService import ProductoService
from src.data_access_layer.models.CategoriaModel import CategoriaModel 

template_dir = os.path.abspath("src/front_layer/templates/module_gestion_productos")
products_controller = Blueprint('producto', __name__, template_folder=template_dir)

@products_controller.route("/", methods=['GET'])
def index():
    busqueda = request.args.get('q') # Para la barra de búsqueda
    with get_db_session() as session:
        repo = ProductoRepository(session)
        mapper = ProductoMapper()
        service = ProductoService(repo, mapper)
        
        productos = service.obtener_todos(busqueda)
        return render_template("list.html", productos=productos)

@products_controller.route("/create", methods=['GET', 'POST'])
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

@products_controller.route("/edit/<id>", methods=['GET', 'POST'])
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

@products_controller.route("/delete/<id>", methods=['POST'])
def delete(id):
    with get_db_session() as session:
        repo = ProductoRepository(session)
        mapper = ProductoMapper()
        service = ProductoService(repo, mapper)
        service.eliminar_producto(id)
        return redirect(url_for('producto.index'))