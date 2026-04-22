from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base

class Empleado(Base):
    __tablename__ = "empleados"

    empleado_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.usuario_id"), primary_key=True)
    puesto = Column(String(50), nullable=False)
    salario = Column(Numeric(12, 2), nullable=False)
    fecha_ingreso = Column(DateTime, server_default=func.now(), nullable=False)

    # Relación simple, sin lógica de "atajos"
    usuario = relationship("Usuario", back_populates="empleado")