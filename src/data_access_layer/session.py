from dotenv import load_dotenv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL , # type: ignore
    echo=False
)

Session = sessionmaker(
    autocommit = False , 
    autoflush=False,
    bind=engine
)
# Crear sesión
session_local_hanbai_db = Session()

# Ejemplo: consulta
# from session import session_local_hanbai_db

# Ejemplo: consulta
# productos = session_local_hanbai_db.query(ProductoModel).all()
# session_local_hanbai_db.close()
# productos = session_local_hanbai_db.query(ProductoModel).all()
# session_local_hanbai_db.close()