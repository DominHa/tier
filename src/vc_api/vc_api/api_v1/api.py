from fastapi import APIRouter

from vc_api.api_v1.endpoints import about, vehicles

api_router = APIRouter()

api_router.include_router(about.router, prefix="", tags=[""])
api_router.include_router(vehicles.router, prefix="", tags=["Vehicles"])
