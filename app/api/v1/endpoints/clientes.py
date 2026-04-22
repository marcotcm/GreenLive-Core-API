from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.cliente import ClienteCreate, ClienteOut, ClienteUpdate
from app.models.usuario import filtroStatusUsuario
from app.services.cliente_service import ClienteService
from app.services.usuario_service import UsuarioService
from app.crud.clientes import CrudCliente
from app.core.security import get_current_user


router = APIRouter()

@router.get("/", response_model=list[ClienteOut], status_code=200, )
async def list_clientes(filtro: filtroStatusUsuario = filtroStatusUsuario.todos, db: AsyncSession = Depends(get_db),
 #usuario_actual: str = Depends(get_current_user)
 ):
    return await ClienteService.get_all(db, filtro.value)

@router.get("/{id}", response_model=ClienteOut, status_code=200)
async def get_cliente(id: str, db: AsyncSession = Depends(get_db)):
    c = await CrudCliente.get_by_id(db, id)
    if not c: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return c


@router.post("/", response_model=ClienteOut, status_code=201)
async def create_cliente(data: ClienteCreate, db: AsyncSession = Depends(get_db)):
     try:
        c= await ClienteService.create(db, data)
        return c
     except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{id}", response_model=ClienteOut, status_code=200)
async def update_cliente(id: str, data: ClienteUpdate, db: AsyncSession = Depends(get_db)):
    
    c = await ClienteService.update(db, id, data)
    if not c: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return c

@router.patch("/activate/{id}/{active}", response_model=dict, status_code=200)
async def activate_cliente(id: str, active: bool,db: AsyncSession = Depends(get_db)):
    if active not in [True, False]:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="El parámetro 'active' debe ser true o false")
    if active:
        c = await UsuarioService.activate(db, id)
    else:
        c = await UsuarioService.deactivate(db, id)

    return {"message": "Cliente reactivado "} if active else {"message": "Cliente desactivado"} 