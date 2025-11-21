from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.bussines_layer.services.ProductoService import ProductoService
from src.bussines_layer.models.ProductoDomainEntity import ProductoDomainEntity

products = Blueprint('products', __name__, template_folder='../templates')
service = ProductoService()

# --- LISTAR (HU04) ---
@products.route('/')
def index():
    lista_productos = service.obtener_todos()
    return render_template('products/index.html', products=lista_productos)

# --- CREAR (HU01) ---
@products.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            nuevo_producto = ProductoDomainEntity(
                nombre=request.form['nombre'],
                descripcion=request.form['descripcion'],
                precio=float(request.form['precio']),
                stock=int(request.form['stock']),
                categoria_id=request.form['categoria_id']
            )
            service.crear_producto(nuevo_producto)
            flash('Producto creado exitosamente', 'success')
            return redirect(url_for('products.index'))
        except Exception as e:
            flash(f'Error al crear: {str(e)}', 'danger')
            
    return render_template('products/create.html')

# --- EDITAR (HU02) ---
@products.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        try:
            producto_actualizado = ProductoDomainEntity(
                id_producto=id,
                nombre=request.form['nombre'],
                descripcion=request.form['descripcion'],
                precio=float(request.form['precio']),
                stock=int(request.form['stock']),
                categoria_id=request.form['categoria_id']
            )
            service.actualizar_producto(producto_actualizado)
            flash('Producto actualizado correctamente', 'success')
            return redirect(url_for('products.index'))
        except Exception as e:
            flash(f'Error al actualizar: {str(e)}', 'danger')

    # Si es GET, buscamos el producto para llenar el formulario
    producto = service.obtener_por_id(id)
    if not producto:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('products.index'))
        
    return render_template('products/edit.html', product=producto)

# --- ELIMINAR (HU03) ---
@products.route('/delete/<string:id>', methods=['POST'])
def delete(id):
    if service.eliminar_producto(id):
        flash('Producto eliminado', 'success')
    else:
        flash('No se pudo eliminar el producto', 'danger')
    return redirect(url_for('products.index'))