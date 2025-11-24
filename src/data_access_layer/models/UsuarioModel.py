from src.data_access_layer.base import Base
from src.data_access_layer.models.RolModel import RolModel

import uuid
from sqlalchemy import (
    Column , String , TIMESTAMP , func , CheckConstraint , ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates , relationship

class UsuarioModel(Base):
    __tablename__ = "usuario"

    id_usuario = Column(
        UUID(as_uuid = True) , 
        name="id_usuario",
        primary_key = True , 
        default = uuid.uuid4 , 
        nullable = False
    )

    nombre = Column(
        String(100) , 
        name="nombre",
        nullable=False
    )

    correo = Column(
        String(100) , 
        name="correo",
        nullable = False ,  
        unique = True , 
    )

    password_hash = Column(
        String(255) , 
        name="password_hash",
        nullable = False
    )

    dni = Column(
        String(20) , 
        name="dni",
        nullable=False , 
        unique=True
    )

    creado_en = Column(
        TIMESTAMP(timezone=True) , 
        name="creado_en",
        server_default=func.now()
    )

    actualizado_en = Column(
        TIMESTAMP(timezone=True) , 
        name="actualizado_en",
        server_default=func.now()
    )

    rol_id = Column(
        UUID(as_uuid=True) , 
        ForeignKey("rol.id_rol") , 
        name="rol_id" , 
    )

    # Atributo python para obtener RolModel asociado
    # print(usuario.rol) = SELECT * FROM rol WHERE rol.id_rol = usuario.rol_id;
    rol = relationship(
        "RolModel" , 
        back_populates="usuario"
    )

    # Atributo python para obtener VentaModel asociado
    venta = relationship(
        "VentaModel" , 
        back_populates="usuario"
    )

    __table_args__ = (
        CheckConstraint("length(dni) >= 8" , name="dni_min_len"),
    )

    @validates("correo")
    def validate_correo(self , key , email):
        import re
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron, email):
            raise ValueError("Email inválido")
        return email