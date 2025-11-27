from dotenv import load_dotenv
import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

# --- CORRECCIÓN DE RUTA .ENV ---
# Calculamos la ruta absoluta a la raíz del proyecto
# Estructura: raiz/src/data_access_layer/session.py
# Necesitamos subir 3 niveles para llegar a la raiz
basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_file = os.path.join(basedir, '.env_db')

# Cargamos explícitamente esa ruta
load_dotenv(env_file)

DATABASE_URL = os.getenv("DATABASE_URL")

# Validación de seguridad
if not DATABASE_URL:
    raise ValueError(f"❌ ERROR CRÍTICO: No se encontró la variable DATABASE_URL.\n   Se buscó el archivo .env en: {env_file}")
# -------------------------------

engine = create_engine(
    DATABASE_URL , # type: ignore
    echo=False
)

# Aquí Session no es una sesión concreta, sino una factoría de sesiones.
LocalSession = sessionmaker(
    autoflush=False,
    bind=engine
)

@contextmanager
def get_db_session():
    session: Session = LocalSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()