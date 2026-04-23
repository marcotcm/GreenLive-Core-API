from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.usuarios import CrudUsuario
from app.crud.empleado import CrudEmpleado
from app.schemas.empleado import EmpleadoCreate, EmpleadoUpdate
from app.core.utils import get_user_roles_data
from app.schemas.usuario import UsuarioCreate
from app.core.security import get_password_hash

class EmpleadoService:
    @staticmethod
    async def get_all(db: AsyncSession, filtro: str):
        """Obtiene todos los empleados según el filtro de estado del usuario."""
        return await CrudEmpleado.get_all_active(db, filtro)


    @staticmethod
    async def create(db: AsyncSession, data: EmpleadoCreate):
        """Crea o vincula un empleado a un usuario existente."""
    
        # Verificamos si el usuario ya existe
        user_data = await get_user_roles_data(db, data.email)
    
        if user_data:
            # El usuario existe. Validamos que no sea ya un empleado
            if "empleado" in user_data["roles"]:
                raise ValueError("Este usuario ya está registrado como empleado.")
        
            # Recuperamos la instancia del usuario para vincular
            user = await CrudUsuario.get_by_id(db, user_data["usuario_id"])
        else:
            #Si no existe, creamos el usuario desde cero
            user_dict = data.model_dump(include=set(UsuarioCreate.model_fields.keys()))
            user_dict["password"] = get_password_hash(data.password)
            user = await CrudUsuario.create(db, user_dict)
    
        #Creamos el perfil de Empleado vinculado al ID (sea nuevo o existente)
        empleado_dict = data.model_dump(exclude=set(UsuarioCreate.model_fields.keys()))
        empleado_dict["empleado_id"] = user.usuario_id
        new_empleado = await CrudEmpleado.create(db, empleado_dict)
    
        # Finalizar transacción
        await db.commit()
    
        # Refresh para asegurar que la relación 'usuario' esté cargada
        await db.refresh(new_empleado, attribute_names=['usuario'])
    
        return new_empleado

    @staticmethod
    async def update(db: AsyncSession, user_id: str, data: EmpleadoUpdate):
        """Actualiza la información del empleado delegando a los CRUDs."""
        empleado = await CrudEmpleado.get_by_id(db, user_id)
        
        # Verificamos que el usuario exista y tenga perfil de empleado
        if not empleado:
            return None
            
        update_data = data.model_dump(exclude_unset=True)
        
        # Actualizamos datos compartidos (Usuario) y específicos (Empleado)
        await CrudUsuario.update(db, empleado.usuario, update_data)
        await CrudEmpleado.update_extra_fields(db, empleado, update_data)
        
        # Aseguramos los cambios en una sola transacción
        await db.commit()
        
        # Recargamos la relación usuario para que la respuesta de la API sea completa
        new_empleado = await CrudEmpleado.get_by_id(db, user_id)
        
        return new_empleado