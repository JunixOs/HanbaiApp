import uuid
from src.data_access_layer.session import get_db_session

# Importamos tus Modelos
from src.data_access_layer.models.RolModel import RolModel
from src.data_access_layer.models.UsuarioModel import UsuarioModel
from src.data_access_layer.models.CategoriaModel import CategoriaModel
from src.data_access_layer.models.ProductoModel import ProductoModel
from src.data_access_layer.models.EstadoVentaModel import EstadoVentaModel

# Importamos TU servicio de encriptación real
from src.bussines_layer.services.module_gestion_usuarios.BcryptService import BcryptService

def cargar_datos_reales():
    print("🔄 Iniciando inserción de datos en la Base de Datos...")
    
    # CORRECCIÓN IMPORTANTE: Usamos 'with' para manejar la sesión
    with get_db_session() as session:
        try:
            # ---------------------------------------------------------
            # 1. ROLES
            # ---------------------------------------------------------
            roles_data = {
                "ADMINISTRADOR": "Acceso total al sistema",
                "ENCARGADO_DE_TIENDA": "Gestión de ventas y productos",
                "CLIENTE": "Usuario comprador"
            }
            roles_db = {} 

            for nombre, desc in roles_data.items():
                rol = session.query(RolModel).filter_by(nombre=nombre).first()
                if not rol:
                    rol = RolModel(id_rol=uuid.uuid4(), nombre=nombre, descripcion=desc)
                    session.add(rol)
                    print(f"✅ Rol creado: {nombre}")
                else:
                    print(f"ℹ️ Rol ya existe: {nombre}")
                roles_db[nombre] = rol

            # ---------------------------------------------------------
            # 2. USUARIO ADMINISTRADOR (Seguro)
            # ---------------------------------------------------------
            correo_admin = "admin@hanbai.com"
            pass_texto = "12345678"
            pass_hash = BcryptService.HashPassword(pass_texto)

            admin = session.query(UsuarioModel).filter_by(correo=correo_admin).first()
            if not admin:
                admin = UsuarioModel(
                    id_usuario=uuid.uuid4(),
                    nombre="Administrador Principal",
                    correo=correo_admin,
                    password_hash=pass_hash,
                    dni="00000001",
                    rol_id=roles_db["ADMINISTRADOR"].id_rol
                )
                session.add(admin)
                print(f"👤 Usuario Admin creado: {correo_admin}")
            else:
                # Actualizar contraseña para asegurar acceso
                admin.password_hash = pass_hash
                print(f"🔄 Usuario Admin actualizado.")

            # ---------------------------------------------------------
            # 3. CATEGORÍAS
            # ---------------------------------------------------------
            cats_nombres = ["Tecnología", "Ropa", "Hogar"]
            cats_db = {}

            for nombre in cats_nombres:
                cat = session.query(CategoriaModel).filter_by(nombre=nombre).first()
                if not cat:
                    cat = CategoriaModel(id_categoria=uuid.uuid4(), nombre=nombre, descripcion=f"Productos de {nombre}")
                    session.add(cat)
                    print(f"📦 Categoría creada: {nombre}")
                else:
                    print(f"ℹ️ Categoría ya existe: {nombre}")
                cats_db[nombre] = cat

            # ---------------------------------------------------------
            # 4. PRODUCTOS (Reales)
            # ---------------------------------------------------------
            productos_lista = [
                {"nom": "Laptop Gamer HP", "pre": 3500.00, "cat": "Tecnología", "desc": "16GB RAM, tarjeta gráfica NVIDIA"},
                {"nom": "Smartphone Samsung", "pre": 1200.00, "cat": "Tecnología", "desc": "Pantalla AMOLED 120Hz"},
                {"nom": "Casaca Impermeable", "pre": 150.00, "cat": "Ropa", "desc": "Ideal para lluvia y frío"},
                {"nom": "Sofá 2 Cuerpos", "pre": 850.00, "cat": "Hogar", "desc": "Color gris, tela lavable"}
            ]

            for p in productos_lista:
                prod = session.query(ProductoModel).filter_by(nombre=p["nom"]).first()
                if not prod:
                    # Verificar que la categoría exista antes de asignar
                    cat_obj = cats_db.get(p["cat"])
                    if cat_obj:
                        nuevo_prod = ProductoModel(
                            id_producto=uuid.uuid4(),
                            nombre=p["nom"],
                            descripcion=p["desc"],
                            precio=p["pre"],
                            stock=20, 
                            descuento_producto=0,
                            categoria_id=cat_obj.id_categoria
                        )
                        session.add(nuevo_prod)
                        print(f"🛒 Producto insertado: {p['nom']}")
                else:
                    print(f"ℹ️ Producto ya existe: {p['nom']}")
            
            # 5. ESTADOS DE VENTA
            estados = ["PENDIENTE", "PAGADO", "CANCELADO"]
            for est in estados:
                e = session.query(EstadoVentaModel).filter_by(nombre=est).first()
                if not e:
                    session.add(EstadoVentaModel(id_estado_venta=uuid.uuid4(), nombre=est, descripcion="Estado del proceso"))

            session.commit()
            print("\n✨ ¡Base de Datos cargada exitosamente! ✨")
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error durante la inserción: {e}")
            raise # Re-lanzamos el error para ver el detalle si falla

if __name__ == "__main__":
    cargar_datos_reales()