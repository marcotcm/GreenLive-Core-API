from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from app.models.empleado import Empleado
from app.models.usuario import Usuario

class CrudEmpleado:
    @staticmethod
    async def get_all_active(db: AsyncSession, filtro: str):
        """Consulta empleados con sus usuarios relacionados."""
        # Base query con eager loading para evitar el problema N+1
        query = select(Empleado).join(Empleado.usuario).options(selectinload(Empleado.usuario))

        # Aplicar filtro basado en el estado del usuario (deleted_at)
        if filtro == "activos":
            query = query.where(Usuario.deleted_at == None)
        elif filtro == "inactivos":
            query = query.where(Usuario.deleted_at != None)
    
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, empleado_id: str):
        """Busca un empleado por ID (activo o inactivo)."""
        result = await db.execute(
            select(Empleado)
            .filter(Empleado.empleado_id == empleado_id)
            .options(selectinload(Empleado.usuario))
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, obj_in_data: dict):
        """Crea el registro en la tabla Empleado."""
        db_obj = Empleado(**obj_in_data)
        db.add(db_obj)
        # No hacemos commit aquí porque suele ser parte de una transacción mayor (con Usuario)
        return db_obj

    @staticmethod
    async def update_extra_fields(db: AsyncSession, empleado_obj: Empleado, update_data: dict):
        """Actualiza campos específicos de la tabla Empleado (puesto, salario, etc)."""
        for field, value in update_data.items():
            if hasattr(empleado_obj, field):
                setattr(empleado_obj, field, value)
        db.add(empleado_obj)
        # El commit lo manejará el Service o el método que coordine la operación
        return empleado_obj