from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func
from app.models.usuario import Usuario
from fastapi import HTTPException, status
from app.core.utils import validar_y_convertir_uuid

class CrudUsuario:
    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: str):
        """Busca un usuario por ID (activo o inactivo)."""
        validar_y_convertir_uuid(user_id)  # Validamos el formato del ID antes de devolver resultados

        result = await db.execute(select(Usuario).filter(Usuario.usuario_id == user_id).options(selectinload(Usuario.cliente)))

        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_email(db: AsyncSession, user_email: str):
        """Busca un usuario por correo electrónico (activo)."""
        
        result = await db.execute(select(Usuario).where(Usuario.email == user_email,
                                                         Usuario.deleted_at == None))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_document(db: AsyncSession, user_document: str, user_type_document: str):
        """Busca un usuario por documento (activo)."""
        result = await db.execute(select(Usuario).where(Usuario.documento == user_document,
                                                        Usuario.tipo_doc == user_type_document,
                                                         Usuario.deleted_at == None))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, obj_in_data: dict):
        """Crea la instancia de Usuario y la agrega a la sesión."""
        db_obj = Usuario(**obj_in_data)
        db.add(db_obj)
        await db.flush() # Sincroniza para obtener el ID sin terminar la transacción
        return db_obj

    @staticmethod
    async def update(db: AsyncSession, db_obj: Usuario, update_data: dict):
        """Actualiza campos del objeto Usuario y guarda cambios."""
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
       
        return db_obj

    @staticmethod
    async def soft_delete(db: AsyncSession, db_obj: Usuario, active: bool):
        """Marca al usuario como inactivo (Borrado lógico)."""

        db_obj.deleted_at = None if active else func.now()
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    @staticmethod
    async def get_with_roles_by_email(db: AsyncSession, email: str):
        """obtener un usuario por email con sus roles relacionados (cliente o empleado) para validaciones de negocio."""
        query = select(Usuario).filter(Usuario.email == email).filter(Usuario.deleted_at == None).options(
            selectinload(Usuario.cliente),
            selectinload(Usuario.empleado)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()