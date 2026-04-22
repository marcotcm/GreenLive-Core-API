from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

# 1. Configuración del esquema de seguridad y contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/cliente/login")

# ==========================================
# FUNCIONES DE CONTRASEÑA
# ==========================================

def get_password_hash(password: str) -> str:
    """Encripta la contraseña para guardarla en la base de datos."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara la contraseña ingresada con la encriptada."""
    return pwd_context.verify(plain_password, hashed_password)

# ==========================================
# FUNCIONES DE TOKEN
# ==========================================

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """Genera el JSON Web Token (JWT) con expiración configurable."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# ==========================================
# VALIDADOR DE RUTAS PROTEGIDAS
# ==========================================

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Úsalo en tus rutas así: async def mi_ruta(user_id: str = Depends(get_current_user))
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token. Inicia sesión nuevamente.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        usuario_id: str = payload.get("sub")
        
        if usuario_id is None:
            raise credentials_exception
            
        return usuario_id
        
    except JWTError:
        raise credentials_exception
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud.usuarios import CrudUsuario
from app.core.security import get_current_user

# --- PORTERO PARA CLIENTES ---
async def get_current_cliente(
    usuario_id: str = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    # Buscamos al usuario en la BD para ver sus roles
    user = await CrudUsuario.get_with_roles_by_id(db, usuario_id)
    
    if not user or not user.cliente:
        raise HTTPException(status_code=403, detail="Acceso denegado: Requiere permisos de Cliente")
    
    return user

# --- PORTERO PARA EMPLEADOS (ADMIN) ---
async def get_current_empleado(
    usuario_id: str = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db)
):
    user = await CrudUsuario.get_with_roles_by_id(db, usuario_id)
    
    if not user or not user.empleado:
        raise HTTPException(status_code=403, detail="Acceso denegado: Requiere permisos de Empleado")
    
    return user