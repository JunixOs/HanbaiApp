# Importaciones corregidas (rutas absolutas desde src)
from src.data_access_layer.base import Base
from src.data_access_layer.session import engine

# IMPORTANTE: Importar TODOS los modelos aquí. 
# Si no los importas, SQLAlchemy no sabrá que existen y no creará las tablas.
from src.data_access_layer.models.UsuarioModel import UsuarioModel
from src.data_access_layer.models.RolModel import RolModel
from src.data_access_layer.models.ProductoModel import ProductoModel
from src.data_access_layer.models.CategoriaModel import CategoriaModel
from src.data_access_layer.models.VentaModel import VentaModel
from src.data_access_layer.models.ComprobanteModel import ComprobanteModel
from src.data_access_layer.models.ComprobanteProductoModel import comprobante_producto
# Agrega aquí cualquier otro modelo nuevo que crees en el futuro

def init_db():
    print("--- Inicializando Base de Datos ---")
    print("Conectando con PostgreSQL...")
    try:
        # Esto crea todas las tablas definidas en los modelos importados
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas exitosamente.")
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")

if __name__ == "__main__":
    init_db()