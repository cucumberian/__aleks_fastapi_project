from db.database import DbManager

# импорт моделей для того, чтобы интерпретатор и считал
# и создал через Base.metadata нормально все таблицы в бд
from models.user import UserOrm
from models.role import Role
# from models.cannot_offer import CannotOffer
from models.history import History
# from models.new_apart import NewApart
from models.old_apart import OldApart
from models.offer import Offer
from models.refusal import Refusal

class Dao:
    def __init__(self, db_manager: DbManager):
        self.db_manager = db_manager

    async def create_schema(self):
        await self.db_manager.create_schema()

    async def create_tables(self):
        await self.create_schema()
        await self.db_manager.create_all()
    
    async def drop_tables(self):
        await self.db_manager.drop_all()
            
