from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.empleado import EmpleadoCreate, EmpleadoOut, EmpleadoUpdate
from app.models.usuario import filtroStatusUsuario
from app.services.empleado_service import EmpleadoService
from app.services.usuario_service import UsuarioService
from app.crud.empleado import CrudEmpleado

router = APIRouter()

@router.get("/", response_model=list[EmpleadoOut], status_code=200)
async def list_empleados(filtro: filtroStatusUsuario = filtroStatusUsuario.todos, db: AsyncSession = Depends(get_db)):
    return await EmpleadoService.get_all(db, filtro.value)

@router.get("/{id}", response_model=EmpleadoOut, status_code=200)
async def get_empleado(id: str, db: AsyncSession = Depends(get_db)):
    e = await CrudEmpleado.get_by_id(db, id)
    if not e: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado")
    return e

@router.post("/", response_model=EmpleadoOut, status_code=201)
async def create_empleado(data: EmpleadoCreate, db: AsyncSession = Depends(get_db)):
     try:
        e = await EmpleadoService.create(db, data)
        return e
     except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{id}", response_model=EmpleadoOut, status_code=200)
async def update_empleado(id: str, data: EmpleadoUpdate, db: AsyncSession = Depends(get_db)):
    e = await EmpleadoService.update(db, id, data)
    if not e: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado")
    return e

@router.patch("/activate/{id}/{active}", response_model=dict, status_code=200)
async def activate_empleado(id: str, active: bool, db: AsyncSession = Depends(get_db)):
   
    if active:
        e = await UsuarioService.activate(db, id)
    else:
        e = await UsuarioService.deactivate(db, id)

    return {"message": "Empleado reactivado"} if active else {"message": "Empleado desactivado"}