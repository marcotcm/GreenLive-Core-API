import uuid
import enum
from sqlalchemy import Column, String, DateTime, Index, func, text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base

class TipoDocumento(enum.Enum):
    CI = "CI"
    RIF = "RIF"
    PASAPORTE = "PASAPORTE"

class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String, nullable=False)
    
    # Identidad centralizada
    tipo_doc = Column(SQLEnum(TipoDocumento, name="tipo_documento", create_type=False), default=TipoDocumento.CI)
    documento = Column(String(20), unique=True, nullable=False)
    telefono = Column(String(20))
    direccion = Column(String(255))
    
    fecha_registro = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)

    __table_args__ = (
        #esto hare que el email y el documento sean únicos solo entre los usuarios activos (deleted_at is null)
        #pero si un usuario ya desactivo su ceunta entonces el documento en la cuneta bloqueada no contara como unico 
        Index("idx_usuarios_email_unique_active", "email", unique=True, postgresql_where=text("deleted_at IS NULL")),
        
        Index("idx_usuarios_doc_unique_active", "documento", unique=True, postgresql_where=text("deleted_at IS NULL")),
    )

    # Relaciones (Usamos strings para evitar importación circular)
    cliente = relationship("Cliente", back_populates="usuario", uselist=False)
    empleado = relationship("Empleado", back_populates="usuario", uselist=False)

class filtroStatusUsuario(enum.Enum):
    activos = "activos"
    inactivos = "inactivos"
    todos = "todos"