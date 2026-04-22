from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    # --- Nuevos campos agregados ---
    tipo_doc: Optional[str] = "CI"
    documento: str = Field(..., min_length=5, max_length=20)
    telefono: Optional[str] = Field(None, pattern=r'^\+?[0-9]{7,15}$')
    direccion: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    # --- Nuevos campos para permitir actualizaciones ---
    tipo_doc: Optional[str] = "CI"
    documento: Optional[str] = Field(None, min_length=5, max_length=20)
    telefono: Optional[str] = Field(None, pattern=r'^\+?[0-9]{7,15}$')
    direccion: Optional[str] = None

class UsuarioOut(UsuarioBase):
    usuario_id: UUID
    deleted_at: Optional[datetime] = None
    fecha_registro: datetime
    
    class Config: 
        from_attributes = True

