import httpx
import logging
from typing import List
from fastapi import HTTPException

logger = logging.getLogger(__name__.split(".")[0])


BASE_URL = "https://data-sharing.tier-services.io/tier_paris/gbfs/2.2"


async def make_request(client, endpoint):
    """Make an ansync request to the external data source."""
    response = await client.get(endpoint)
    return response.json()


async def get_available_vehicles() -> List[dict]:
    """Get list of available vehicles."""
    async with httpx.AsyncClient() as client:
        vehicles = await make_request(
            client=client, endpoint=BASE_URL + "/free-bike-status"
        )
    try:
        vehicle_data = vehicles["data"]["bikes"]
        return vehicle_data
    except KeyError:
        logger.error(
            "Unable to get vehicle data from external source",
            extra={"endpoint": BASE_URL + "/free-bike-status"},
        )
        raise HTTPException(
            status_code=503, detail="Failed to obtain data from external source"
        )


async def get_pricing_plans() -> List[dict]:
    """Get pricing plans from external data source."""
    async with httpx.AsyncClient() as client:
        result = await make_request(
            client=client, endpoint=BASE_URL + "/system-pricing-plans"
        )
    try:
        pricing_plans = result["data"]["plans"]
        return pricing_plans
    except KeyError:
        logger.error(
            "Unable to get pricing plan data from external source",
            extra={"endpoint": BASE_URL + "/system-pricing-plans"},
        )
        raise HTTPException(
            status_code=503, detail="Failed to obtain data from external source"
        )
