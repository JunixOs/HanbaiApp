from src.data_access_layer.base import Base
from src.data_access_layer.models.RolReporteModel import rol_reporte
from src.data_access_layer.models.ReporteModel import ReporteModel

import uuid
from sqlalchemy import (
    Column , String , TIMESTAMP , func , Text , UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

class RolModel(Base):
    __tablename__ = "rol"

    id_rol = Column(
        UUID(as_uuid=True) ,
        name="id_rol", 
        primary_key= True , 
        nullable= False , 
        default=uuid.uuid4
    )

    nombre = Column(
        String(100) , 
        name="nombre",
        nullable=False , 
        unique=True
    )

    descripcion = Column(
        Text , 
        name="descripcion",
        nullable=True
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

    usuario = relationship("UsuarioModel" , back_populates="rol" , uselist=False)

    reporte = relationship(
        "ReporteModel" , 
        secondary=rol_reporte , 
        back_populates="rol"
    )

    __table_args__ = (
        UniqueConstraint("id_rol" , "nombre" , name="Rol_UQ"),
    )