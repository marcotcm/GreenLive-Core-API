from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
import os
from app.core.config import settings



# Motor asíncrono para PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,   # <--- Verifica la conexión antes de usarla
    pool_recycle=3600,    # <--- Refresca las conexiones cada hora
    pool_size=10,         # (Opcional) Número de conexiones base
    max_overflow=20       # (Opcional) Conexiones extra permitidas
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

# Inyección de dependencia para las rutas
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session