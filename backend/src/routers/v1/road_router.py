from collections.abc import Sequence

from fastapi import APIRouter

from src.repositories.cruds.road_crud import RoadCRUD
from src.repositories.mongo_context import MongoDatabaseContext
from src.schemas.road import AddRoadRequest, GetGeometriesResponse, GetRoadResponse

router = APIRouter()

@router.post('/road')
async def add_road_info(road_info: AddRoadRequest | Sequence[AddRoadRequest]):
    """Эндпоинт добавления информации о дороге"""
    db_context = MongoDatabaseContext[RoadCRUD]()
    db_context.crud = RoadCRUD(collection=db_context.db['roads'])
    if isinstance(road_info, AddRoadRequest):
        await db_context.crud.add_road(road_info)
    else:
        await db_context.crud.add_roads(road_info)

@router.get('/get-geometries')
async def get_geometries() -> Sequence[GetGeometriesResponse]:
    """Эндпоинт для получения информации о объектах"""
    db_context = MongoDatabaseContext[RoadCRUD]()
    db_context.crud = RoadCRUD(collection=db_context.db['roads'])
    return await db_context.crud.get_road_geometries(out_schema=GetGeometriesResponse)

@router.get('/road')
async def get_road(id: str):
    db_context = MongoDatabaseContext[RoadCRUD]()
    db_context.crud = RoadCRUD(collection=db_context.db['roads'])
    return await db_context.crud.get_road_by_id(id, out_schema=GetRoadResponse)