from sqlalchemy import Column, Numeric, Integer, Enum as SQLEnum
from app.db.session import Base
import enum

class TipoClienteEnum(enum.Enum):
    nuevo = "nuevo"
    regular = "regular"
    vip = "vip"

class ConfigCategoria(Base):
    __tablename__ = "config_categorias"
    
    tipo_cliente = Column(SQLEnum(TipoClienteEnum, name="tipo_cliente_enum", create_type=False), primary_key=True)
    descuento_porcentaje = Column(Numeric(5, 2), nullable=False, default=0)
    min_compras_requeridas = Column(Integer, default=0)