from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from .usuario import UsuarioCreate, UsuarioOut, UsuarioUpdate

class EmpleadoCreate(UsuarioCreate):
    puesto: str
    salario: float = Field(gt=0)

class EmpleadoUpdate(UsuarioUpdate):
    puesto: Optional[str] = None
    salario: Optional[float] = Field(None, gt=0)

class EmpleadoOut(BaseModel):
    empleado_id: UUID  
    puesto: str
    salario: float
    fecha_ingreso: datetime 
    usuario: UsuarioOut # Composición para cargar datos del usuario

    model_config = ConfigDict(from_attributes=True)