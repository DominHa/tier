import logging
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, Query

from vc_api.external_data_service.extract import (
    get_available_vehicles,
    get_pricing_plans,
)
from vc_api.external_data_service.transform import (
    transform_vehicle_data,
)

from vc_api.models.responses import VehicleData
from vc_api.models.requests import UserLocation


# logging and exceptions?

logger = logging.getLogger(__name__.split(".")[0])
router = APIRouter()


@router.post(
    "/vehicles",
    summary="Retrieves vehicle data",
    response_model=List[VehicleData],
)
async def get_vehicles(
    user_location: Optional[UserLocation] = None,
    maximum_distance_from_user_m: Optional[int] = Query(None, lt=5000),
    estimated_journey_distance_m: Optional[int] = Query(None, ge=1, lt=20000),
    vehicle_type: Optional[str] = None,
    only_find_available: Optional[bool] = None,
    limit: Optional[int] = 50,
):
    """Call the external data source and transform the result based on filters."""
    vehicles = await get_available_vehicles()
    pricing_plans = await get_pricing_plans()
    formatted_vehicles_response = transform_vehicle_data(
        vehicles,
        user_location,
        maximum_distance_from_user_m,
        estimated_journey_distance_m,
        vehicle_type,
        only_find_available,
        pricing_plans,
        limit,
    )
    return formatted_vehicles_response
