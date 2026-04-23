from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from app.db.session import get_db
from app.crud.usuarios import CrudUsuario
from app.core.security import verify_password, create_access_token, get_password_hash
from app.core.config import settings
from app.schemas.auth import Token, ForgotPassword, ResetPassword

router = APIRouter()



@router.post("/cliente/login", response_model=Token)
async def login_cliente(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await CrudUsuario.get_with_roles_by_email(db, email=form_data.username)
    
    if not user or user.deleted_at is not None:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas o usuario inactivo")
        
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
        
    if not user.cliente:
        raise HTTPException(status_code=403, detail="Acceso denegado: No tienes perfil de cliente")
        
    access_token = create_access_token(subject=user.usuario_id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/empleado/login", response_model=Token)
async def login_empleado(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await CrudUsuario.get_with_roles_by_email(db, email=form_data.username)
    
    if not user or user.deleted_at is not None:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas o usuario inactivo")
        
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
        
    if not user.empleado:
        raise HTTPException(status_code=403, detail="Acceso denegado: Área restringida para empleados")
        
    access_token = create_access_token(subject=user.usuario_id)
    return {"access_token": access_token, "token_type": "bearer"}



@router.post("/olvide-password", status_code=status.HTTP_200_OK)
async def solicitar_recuperacion(data: ForgotPassword, db: AsyncSession = Depends(get_db)):
    user = await CrudUsuario.get_by_email(db, data.email)
    mensaje_exito = {"message": "Si el correo está registrado, recibirás un enlace de recuperación."}
    
    if not user:
        return mensaje_exito
        
    # Creamos un token que expira en solo 15 minutos por seguridad
    tiempo_expiracion = timedelta(minutes=15)
    reset_token = create_access_token(subject=user.usuario_id, expires_delta=tiempo_expiracion)
    
    # SIMULACIÓN DE ENVÍO DE CORREO
    print(f"\n{'='*50}")
    print(f"EMAIL SIMULADO PARA: {data.email}")
    print(f"Haz clic aquí para recuperar tu contraseña:")
    print(f"http://localhost:8000/resetear?token={reset_token}")
    print(f"{'='*50}\n")
    
    return mensaje_exito


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def resetear_password(data: ResetPassword, db: AsyncSession = Depends(get_db)):
    #Analizamos el Token
    try:
        payload = jwt.decode(data.token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        usuario_id: str = payload.get("sub")
        if usuario_id is None:
            raise HTTPException(status_code=400, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=400, detail="El enlace es inválido o ha expirado")
        
    #Buscamos al usuario revelado por el token
    user = await CrudUsuario.get_by_id(db, usuario_id)
    if not user or user.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o inactivo")
        
    #Encriptamos la clave nueva y la guardamos
    user.password = get_password_hash(data.nueva_password)
    db.add(user)
    await db.commit()
    
    return {"message": "Contraseña actualizada exitosamente. Ya puedes iniciar sesión."}