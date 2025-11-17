from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "postgresql+psycopg2://hanbai_user:arch_2023@localhost:5432/hanbai_db" ,
    echo=False
)

Session = sessionmaker(bind=engine)
session_hanbai_db = Session()