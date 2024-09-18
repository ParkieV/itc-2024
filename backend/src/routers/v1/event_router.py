from collections.abc import Sequence

from fastapi import APIRouter

from src.repositories.cruds.event_crud import EventCRUD
from src.repositories.cruds.stage_crud import StageCRUD
from src.repositories.mongo_context import MongoDatabaseContext
from src.schemas.event import GetEventResponse, BaseEvent, AddEventRequest
from src.schemas.stage import StageResponse

router = APIRouter()

@router.get('/event')
async def get_event(id: str):
    db_context = MongoDatabaseContext[EventCRUD]()
    db_context.crud = EventCRUD(collection=db_context.db['events'])
    event = (await db_context.crud.get_event_by_id(id, out_schema=BaseEvent)).model_dump()
    db_context_2 = MongoDatabaseContext[StageCRUD]()
    db_context_2.crud = StageCRUD(collection=db_context.db['stages'])
    print('a')
    stages = await db_context_2.crud.get_stages_by_event_id(id, out_schema=StageResponse)
    print('b')
    event['stages'] = stages

    return GetEventResponse.model_validate(event)

@router.post('/event')
async def add_event(event_info: AddEventRequest):

    db_context = MongoDatabaseContext[EventCRUD]()
    db_context.crud = EventCRUD(collection=db_context.db['events'])
    await db_context.crud.add_event(event_info)

@router.get('/events')
async def get_events() -> Sequence[BaseEvent]:
    db_context = MongoDatabaseContext[EventCRUD]()
    db_context.crud = EventCRUD(collection=db_context.db['events'])
    return await db_context.crud.get_events(out_schema=BaseEvent)
