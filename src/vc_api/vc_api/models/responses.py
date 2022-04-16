from typing import Any, Dict, List, Optional, Tuple
from decimal import Decimal

from pydantic import BaseModel


class VehicleData(BaseModel):
    """Model data that can be returned in the response to the vehicles endpoint."""

    vehicle_id: str
    vehicle_type_id: str
    distance_from_user_m: Optional[float]
    location: Tuple[Decimal, Decimal]
    remaining_range_m: Optional[float]
    unlock_price: Optional[float]
    price_per_minute: Optional[float]
    currency: Optional[str]
