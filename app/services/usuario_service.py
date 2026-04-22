from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.usuarios import CrudUsuario
from fastapi import HTTPException, status

class UsuarioService:
    @staticmethod
    async def deactivate(db: AsyncSession, user_id: str):
        user = await CrudUsuario.get_by_id(db, user_id)
        if not user:
            raise HTTPException(404, "Usuario no encontrado")
        if user.deleted_at:
            raise HTTPException(400, "El usuario ya está desactivado")
            
        return await CrudUsuario.soft_delete(db, user, active=False)

    @staticmethod
    async def activate(db: AsyncSession, user_id: str):
        user = await CrudUsuario.get_by_id(db, user_id)
        if not user:
            raise HTTPException(404, "Usuario no encontrado")
        if not user.deleted_at:
            raise HTTPException(400, "El usuario ya está activo")

        # VALIDACIONES DE INTEGRIDAD 
        await UsuarioService._validate_unique_fields(db, user)

        return await CrudUsuario.soft_delete(db, user, active=True)

    @staticmethod
    async def _validate_unique_fields(db: AsyncSession, user):
        """Valida que los datos del usuario no estén en uso por otro usuario ACTIVO."""
        # Validar Email
        existing_email = await CrudUsuario.get_by_email(db, user.email)
        if existing_email and existing_email.usuario_id != user.usuario_id:
            raise HTTPException(409, "El email ya está ocupado por otra cuenta activa")

        # Validar Documento
        existing_doc = await CrudUsuario.get_by_document(db, user.documento, user.tipo_doc)
        if existing_doc and existing_doc.usuario_id != user.usuario_id:
            raise HTTPException(409, "El documento ya está registrado en otra cuenta activa")
        
    
    