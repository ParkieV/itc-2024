from fastapi import APIRouter

# from src.routers.v1.auth.router import router as auth_router
from src.routers.v1.road_router import router as road_router
from src.routers.v1.stage_router import router as stage_router
from src.routers.v1.event_router import router as event_router


router = APIRouter(prefix='/v1')

# router.include_router(auth_router, tags=['Получение доступа в систему'])\
router.include_router(road_router, tags=['Работа с дорогами'])
router.include_router(stage_router, tags=['Работа с этапами'])
router.include_router(event_router, tags=['Работа с процессами'])
