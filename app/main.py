from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.v1.router import api_router
from app.core.config import settings


# Instancia de la App con metadatos profesionales
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="API robusta para la gestión de Green Live con arquitectura limpia."
)

# 1. Configuración de CORS
# Permite que tu frontend se comunique con el backend sin bloqueos del navegador
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )



# 3. Manejador Global de Excepciones (Evita que la API muera)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc) if not settings.PROJECT_NAME == "Green Live API" else "Error interno en el servidor."
        }
    )

# 4. Inclusión de Rutas Unificadas
app.include_router(api_router, prefix=settings.API_V1_STR)

# 5. Endpoint de salud (Healthcheck)
@app.get("/", tags=["Health"])
async def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online"
    }