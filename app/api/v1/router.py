from fastapi import APIRouter
from app.api.v1.endpoints import clientes, empleados, auth

api_router = APIRouter()

# Unificamos todas las rutas de la versión 1
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
api_router.include_router(empleados.router, prefix="/empleados", tags=["Empleados"])