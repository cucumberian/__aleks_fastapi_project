from dao.new_apart_dao import NewApartDao

class NewApartService:
    def __init__(self, new_apart_dao: NewApartDao):
        self.new_apart_dao = new_apart_dao
    
    async def get_districts(self):
        districts = await self.new_apart_dao.get_districts()
        return districts