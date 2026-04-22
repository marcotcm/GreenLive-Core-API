# GreenLive - Core API

Este repositorio contiene el núcleo lógico (Core Backend) del ecosistema GreenLive. Se trata de una API RESTful de alto rendimiento diseñada para centralizar la gestión de inventarios, usuarios, autenticación y transacciones para las plataformas de Cliente y Administración.

## Estado del Proyecto: Desarrollo Activo
El backend se encuentra en una fase avanzada de implementación del núcleo de seguridad y gestión de identidad. Hemos adoptado una arquitectura limpia y modular para garantizar la integridad de los datos y la facilidad de mantenimiento.

**Funcionalidades Clave Implementadas:**
* **Autenticación Dual:** Rutas de login independientes para Clientes y Empleados bajo el estándar OAuth2.
* **Seguridad Robusta:** Encriptación de contraseñas mediante `Bcrypt` y gestión de sesiones con `JSON Web Tokens (JWT)`.
* **RBAC (Role-Based Access Control):** Sistema de dependencias ("Porteros") para restringir el acceso a rutas según el perfil del usuario.
* **Gestión de Identidad:** CRUD completo de usuarios con soporte para borrado lógico y recuperación de contraseñas mediante tokens temporales.

## Tecnologías Utilizadas
* **Python 3.10+**: Lenguaje base por su versatilidad y ecosistema.
* **FastAPI**: Framework moderno para la construcción de APIs rápidas y seguras.
* **PostgreSQL**: Base de datos relacional robusta para garantizar la integridad de la información.
* **SQLAlchemy (Async)**: ORM para la gestión asíncrona de la base de datos.
* **Pydantic**: Validación de esquemas de datos y tipado estricto.
* **PyJWT & Passlib**: Implementación de seguridad y hashing de grado industrial.

## Instalación y Configuración Local
Para ejecutar este servidor en su entorno local:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/marcotcm/GreenLive-Core-API.git](https://github.com/marcotcm/GreenLive-Core-API.git)
   cd GreenLive-Core-API
   ```

2. **Configurar el entorno virtual:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # En Windows
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Variables de Entorno:**
   Cree un archivo `.env` en la raíz basado en `.env.example` con sus credenciales de base de datos y `SECRET_KEY`.

5. **Iniciar el servidor de desarrollo:**
   ```bash
   uvicorn app.main:app --reload --port 8030
   ```

La documentación interactiva estará disponible en http://localhost:8030/docs.

## Arquitectura del Sistema
El backend está estructurado siguiendo principios de **Clean Architecture**:
* `app/models`: Definición de tablas de base de datos.
* `app/schemas`: Modelos de validación de entrada/salida (Pydantic).
* `app/crud`: Operaciones atómicas de base de datos.
* `app/services`: Lógica de negocio y validaciones complejas.
* `app/api`: Definición de endpoints y controladores de ruta.

## Ecosistema GreenLive
1. **GreenLive-Delivery-Front**: Interfaz para el cliente final (React).
2. **GreenLive-Admin-Dashboard**: Panel administrativo (En desarrollo).
3. **GreenLive-Core-API**: (Este repositorio) El motor central que alimenta todo el sistema.

---
Desarrollado por Marco Concho | Estudiante de Ingeniería Informática.
