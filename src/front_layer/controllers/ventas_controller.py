from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from src.bussines_layer.services.VentaService import VentaService
from src.bussines_layer.services.ProductoService import ProductoService

ventas = Blueprint('ventas', __name__, template_folder='../templates')
venta_service = VentaService()
producto_service = ProductoService()

# --- VISTA: Catálogo para Comprar ---
@ventas.route('/catalogo')
def catalogo():
    # Reutilizamos el servicio de productos para mostrar qué comprar
    productos = producto_service.obtener_todos()
    return render_template('ventas/catalogo.html', products=productos)

# --- VISTA: Carrito de Compras ---
@ventas.route('/carrito')
def carrito():
    return render_template('ventas/carrito.html')

# --- VISTA: Historial de Ventas ---
@ventas.route('/')
def index():
    historial = venta_service.obtener_historial()
    return render_template('ventas/index.html', ventas=historial)

# --- ACCIÓN: Procesar Compra (AJAX) ---
@ventas.route('/procesar_compra', methods=['POST'])
def procesar_compra():
    try:
        # TODO: Usar ID real del usuario en sesión
        usuario_actual_id = "d4bc91d0-066a-4da3-b1c1-431612345678" # ID Temporal (reemplazar por real)
        
        datos = request.get_json()
        carrito = datos.get('carrito')
        
        if not carrito:
            return jsonify({'status': 'error', 'message': 'Carrito vacío'}), 400

        venta_id = venta_service.registrar_venta_compleja(usuario_actual_id, carrito)
        
        # Mensaje flash para la siguiente recarga
        flash('¡Compra realizada con éxito!', 'success')
        
        return jsonify({
            'status': 'success', 
            'redirect_url': url_for('ventas.index')
        }), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400