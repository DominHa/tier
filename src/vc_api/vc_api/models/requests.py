from typing import Tuple
from pydantic import BaseModel


class UserLocation(BaseModel):
    """Model the format of user co-ordinates to be passed to the /vehicles endpoint."""

    user_location_coordinates: Tuple[float, float]
