from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from app.models.cliente import Cliente
from app.models.usuario import Usuario

class CrudCliente:
    @staticmethod
    async def get_all_active(db: AsyncSession, filtro: str):
        """Consulta clientes con sus usuarios relacionados."""
        # Base query con eager loading para evitar el problema N+1
        query = select(Cliente).join(Cliente.usuario).options(selectinload(Cliente.usuario))

        # Aplicar filtro solo si es necesario
        if filtro == "activos":
            query = query.where(Usuario.deleted_at == None)
        elif filtro == "inactivos":
            query = query.where(Usuario.deleted_at != None)
    
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, cliente_id: str):
        """Busca un cliente por ID (activo o inactivo)."""
        result = await db.execute(
            select(Cliente)
            .filter(Cliente.cliente_id == cliente_id)
            .options(selectinload(Cliente.usuario))
            )
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, obj_in_data: dict):
        """Crea el registro en la tabla Cliente."""
        db_obj = Cliente(**obj_in_data)
        db.add(db_obj)
        # No hacemos commit aquí porque suele ser parte de una transacción mayor (con Usuario)
        return db_obj

    @staticmethod
    async def update_extra_fields(db: AsyncSession, cliente_obj: Cliente, update_data: dict):
        """Actualiza campos específicos de la tabla Cliente (documento, telefono, etc)."""
        for field, value in update_data.items():
            if hasattr(cliente_obj, field):
                setattr(cliente_obj, field, value)
        db.add(cliente_obj)
        # El commit lo manejará el Service o el método que coordine la operación
        return cliente_obj