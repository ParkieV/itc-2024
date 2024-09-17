from fastapi import APIRouter

# from src.routers.v1.auth.router import router as auth_router
from src.routers.v1.roads.router import router as road_router

router = APIRouter(prefix='/v1')

# router.include_router(auth_router, tags=['Получение доступа в систему'])\
router.include_router(road_router, tags=['Работа с дорогами'])