import enum
from sqlalchemy import Column, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
import app.models.configuracion 


class TipoClienteEnum(enum.Enum):
    nuevo = "nuevo"
    regular = "regular"
    vip = "vip"

class Cliente(Base):
    __tablename__ = "clientes"

    cliente_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.usuario_id"), primary_key=True)
    puntos_lealtad = Column(Integer, default=0)
    total_compras = Column(Integer, default=0)
    
    # FK a la tabla de configuración
    tipo_cliente = Column(
        SQLEnum(TipoClienteEnum, name="tipo_cliente_enum", create_type=False),
        ForeignKey("config_categorias.tipo_cliente"),
        default=TipoClienteEnum.nuevo
    )

    usuario = relationship("Usuario", back_populates="cliente")
    config = relationship("ConfigCategoria") # Relación con la tabla maestra de descuentos

   