from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.usuarios import CrudUsuario
from app.crud.clientes import CrudCliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate
from app.schemas.usuario import UsuarioCreate
from app.core.utils import get_user_roles_data
from app.core.security import get_password_hash

class ClienteService:
    @staticmethod
    async def get_all(db: AsyncSession , filtro: str):
        """Obtiene todos los clientes activos."""

        return await CrudCliente.get_all_active(db, filtro)


    @staticmethod
    async def create(db: AsyncSession, data: ClienteCreate):
        """Crea o vincula un cliente a un usuario existente."""
    
        #Verificamos si el usuario ya existe usando la utilidad
        user_data = await get_user_roles_data(db, data.email)
    
        if user_data:
            # El usuario existe. Verificamos si ya es cliente
            if "cliente" in user_data["roles"]:
                raise ValueError("Este usuario ya está registrado como cliente.")
        
            # Recuperamos la instancia del usuario de la DB para poder vincular
            user = await CrudUsuario.get_by_id(db, user_data["usuario_id"])
        else:
            #Si no existe, creamos el usuario desde cero
            user_dict = data.model_dump(include=set(UsuarioCreate.model_fields.keys()))
            user_dict["password"] = get_password_hash(data.password)
            user = await CrudUsuario.create(db, user_dict)
    
        #Creamos el perfil de Cliente vinculado al ID (sea nuevo o existente)
        cliente_dict = data.model_dump(exclude=set(UsuarioCreate.model_fields.keys()))
        cliente_dict["cliente_id"] = user.usuario_id
        new_cliente = await CrudCliente.create(db, cliente_dict)
    
        #Finalizar transacción
        await db.commit()
    
        # Refresh para asegurar que la relación 'usuario' esté cargada para Pydantic
        await db.refresh(new_cliente, attribute_names=['usuario'])
    
        return new_cliente

    @staticmethod
    async def update(db: AsyncSession, user_id: str, data: ClienteUpdate):
        """Actualiza la información del cliente delegando a los CRUDs."""
        print(data )
        user = await CrudUsuario.get_by_id(db, user_id)
        if not user or not user.cliente:
            return None
            
        update_data = data.model_dump(exclude_unset=True)
        print("Datos a actualizar:", update_data)
        # Actualizamos la parte de Usuario (esto hace commit internamente según crud_usuario)
        
        await CrudUsuario.update(db, user, update_data)
        await CrudCliente.update_extra_fields(db, user.cliente, update_data)
        await db.commit() # Aseguramos los cambios del perfil
        
        new_actualizado = await CrudCliente.get_by_id(db, user_id)
        
        return new_actualizado