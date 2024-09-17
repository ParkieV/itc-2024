from fastapi import APIRouter

from src.repositories.cruds.road_crud import RoadCRUD
from src.repositories.mongo_context import MongoDatabaseContext
from src.schemas.road import AddRoadRequest

router = APIRouter()

@router.post('/road')
async def add_road_info(road_info: AddRoadRequest):
    """Эндпоинт добавления информации о дороге"""
    db_context = MongoDatabaseContext[RoadCRUD]()
    db_context.crud = RoadCRUD(collection=db_context.db['roads'])
    print('a')
    await db_context.crud.add_object(road_info)