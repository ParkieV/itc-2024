from fastapi import APIRouter

from src.repositories.cruds.stage_crud import StageCRUD
from src.repositories.mongo_context import MongoDatabaseContext
from src.schemas.stage import StageResponse

router = APIRouter()


@router.post('/stage')
async def add_event(stage_info: StageResponse):
    db_context = MongoDatabaseContext[StageCRUD]()
    db_context.crud = StageCRUD(collection=db_context.db['stages'])
    await db_context.crud.add_stage(stage_info)