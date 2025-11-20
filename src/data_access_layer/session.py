from dotenv import load_dotenv
import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL , # type: ignore
    echo=False
)

# Aquí Session no es una sesión concreta, sino una factoría de sesiones.
# Cada vez que haces session = Session(), obtienes una instancia de sqlalchemy.orm.Session que puedes usar para .query(), .add(), .commit(), etc.
LocalSession = sessionmaker(
    autoflush=False,
    bind=engine
)
# Crear sesión

@contextmanager
def get_db_session():
    session: Session = LocalSession()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

# Ejemplo: consulta
# from src.models import UsuarioModel  # ejemplo

# with get_db_session() as db:
#     usuario = db.query(UsuarioModel).first()
#     print(usuario.nombre)