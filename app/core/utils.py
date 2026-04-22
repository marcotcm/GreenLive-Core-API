import uuid
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from app.models.usuario import Usuario

async def validar_y_convertir_uuid(id_verificar: str) -> UUID:
    try:
        # Esto devuelve un OBJETO uuid.UUID, no un string
        return uuid.UUID(id_verificar)
    except (ValueError, AttributeError):
        raise HTTPException(
            status_code=400, 
            detail="El formato del ID es inválido (debe ser un UUID completo)"
        )


async def get_user_roles_data(db: AsyncSession, email: str):
    """
    Utilidad reutilizable para obtener usuario con sus relaciones de roles.
    """
    query = select(Usuario).filter(Usuario.email == email).filter(Usuario.deleted_at == None).options(
        selectinload(Usuario.cliente),
        selectinload(Usuario.empleado)
    )
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        return None
        
    return {
        "usuario_id": user.usuario_id,
        "email": user.email,
        "roles": [
            "cliente" if user.cliente else None, 
            "empleado" if user.empleado else None
        ]
    }