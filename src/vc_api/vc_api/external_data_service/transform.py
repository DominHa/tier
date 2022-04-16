from typing import List, Any
from fastapi import HTTPException
from geopy import distance
import pandas as pd
import numpy as np
import logging

from vc_api.models.responses import VehicleData
from vc_api.models.requests import UserLocation


logger = logging.getLogger(__name__.split(".")[0])


def get_distance_m_from_user(user_coords, vehicle_coords) -> int:
    """Calculate the distance in metres between a user and a vehicle."""
    uc_float = [float(x) for x in user_coords]
    distance_m = int(distance.distance(uc_float, vehicle_coords).m)
    return distance_m


def get_price_info(pricing_plan_id: str, pricing_plan: dict, attribute: str) -> Any:
    """Return elements of the pricing plan based on the pricing plan and other attributes."""
    if pricing_plan_id == pricing_plan["plan_id"]:
        if attribute == "per_min_pricing":
            return float(pricing_plan[attribute][0]["rate"])
        if attribute == "price":
            return float(pricing_plan[attribute])
        return pricing_plan[attribute]
    else:
        return np.nan


def transform_vehicle_data(
    vehicles: List[dict],
    user_location: UserLocation,
    maximum_distance_from_user_m: int,
    estimated_journey_distance_m: int,
    vehicle_type: str,
    only_find_available: bool,
    pricing_plans: List[dict],
    limit: int,
) -> List[VehicleData]:
    """Transform and apply any filters to the vehicle data."""

    vehicle_df = pd.DataFrame(vehicles)

    ## FILTER
    if vehicle_type:
        vehicle_df = vehicle_df[(vehicle_df["vehicle_type_id"] == vehicle_type)]

    if only_find_available:
        vehicle_df = vehicle_df[
            (vehicle_df["is_reserved"] == False) & (vehicle_df["is_disabled"] == False)
        ]

    if estimated_journey_distance_m:
        vehicle_df = vehicle_df[
            (vehicle_df["current_range_meters"] >= estimated_journey_distance_m)
        ]

    ## AUGMENT
    vehicle_df["location"] = list(zip(vehicle_df.lat, vehicle_df.lon))

    if user_location:
        vehicle_df["distance_from_user_m"] = vehicle_df["location"].map(
            lambda x: get_distance_m_from_user(
                user_coords=user_location.user_location_coordinates, vehicle_coords=x
            )
        )
        # sort the data so the user gets the nearest ones first
        vehicle_df = vehicle_df.sort_values("distance_from_user_m")

    if maximum_distance_from_user_m:
        # check if user_location is passed, if not throw an error
        if user_location is None:
            raise HTTPException(
                status_code=400,
                detail="maximum distance from user filter has been set but user location wasn't provided!",
            )
        vehicle_df = vehicle_df[
            (vehicle_df["distance_from_user_m"] <= maximum_distance_from_user_m)
        ]

    vehicle_df["unlock_price"] = 0
    vehicle_df["price_per_minute"] = 0
    vehicle_df["currency"] = ""

    for plan in pricing_plans:
        vehicle_df["unlock_price"] = vehicle_df["pricing_plan_id"].map(
            lambda x: get_price_info(
                pricing_plan_id=x, pricing_plan=plan, attribute="price"
            )
        )
        vehicle_df["price_per_minute"] = vehicle_df["pricing_plan_id"].map(
            lambda x: get_price_info(
                pricing_plan_id=x, pricing_plan=plan, attribute="per_min_pricing"
            )
        )
        vehicle_df["currency"] = vehicle_df["pricing_plan_id"].map(
            lambda x: get_price_info(
                pricing_plan_id=x, pricing_plan=plan, attribute="currency"
            )
        )

    ## RENAME COLUMNS
    vehicle_df = vehicle_df.rename(
        columns={"bike_id": "vehicle_id", "current_range_meters": "remaining_range_m"}
    )

    ## DROP UNWANTED COLUMNS
    vehicle_df = vehicle_df.drop(
        columns=[
            "lat",
            "lon",
            "is_reserved",
            "is_disabled",
            "pricing_plan_id",
            "rental_uris",
        ],
        axis=1,
        errors="ignore",
    )

    ## VALIDATE
    if limit:
        vehicle_df = vehicle_df.head(limit)
    vehicles = vehicle_df.to_dict("records")

    return vehicles
