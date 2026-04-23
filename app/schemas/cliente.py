from pydantic import BaseModel,ConfigDict ,Field
from typing import Optional
from uuid import UUID
from .usuario import UsuarioCreate, UsuarioOut, UsuarioUpdate

class ClienteCreate(UsuarioCreate):
    puntos_lealtad: Optional[int] = 0
    tipo_cliente: Optional[str] = "nuevo"# 'nuevo', 'regular', 'vip'
    total_compras: Optional[int] = 0

class ClienteUpdate(UsuarioUpdate):
    puntos_lealtad: Optional[int] = None
    tipo_cliente: Optional[str] = None # 'nuevo', 'regular', 'vip'
    total_compras: Optional[int] = None


class ClienteOut(BaseModel):
    cliente_id: UUID
    puntos_lealtad: int
    total_compras: int
    tipo_cliente: str
    usuario: UsuarioOut 

    model_config = ConfigDict(from_attributes=True)
   