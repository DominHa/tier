import pytest
from vc_api.external_data_service.transform import (
    get_distance_m_from_user,
    get_price_info,
)


@pytest.fixture()
def sample_user_coords():
    return ("48.8584", "2.2945")


@pytest.fixture()
def sample_vehicle_coords():
    return ("48.89", "2.3945")


@pytest.fixture()
def sample_pricing_plan_id():
    return "96608a7f-e2b7-4a8c-aeb7-19524c93b4c3"


@pytest.fixture()
def sample_pricing_plan():
    return {
        "plan_id": "96608a7f-e2b7-4a8c-aeb7-19524c93b4c3",
        "name": "scooter-standard-pricing-paris",
        "currency": "EUR",
        "price": 1,
        "is_taxable": False,
        "description": "Standard pricing for scooters, 1.00 EUR to unlock, 0.22 EUR per minute to rent",
        "per_min_pricing": [{"start": 0, "rate": 0.22, "interval": 1}],
    }


def test_get_distance_m_from_user(sample_user_coords, sample_vehicle_coords):
    distance_from_user_m = get_distance_m_from_user(
        sample_user_coords, sample_vehicle_coords
    )
    assert isinstance(distance_from_user_m, int)
    assert distance_from_user_m == 8133


def test_get_price_info(sample_pricing_plan, sample_pricing_plan_id):
    currency = get_price_info(
        pricing_plan_id=sample_pricing_plan_id,
        pricing_plan=sample_pricing_plan,
        attribute="currency",
    )
    unlock_price = get_price_info(
        pricing_plan_id=sample_pricing_plan_id,
        pricing_plan=sample_pricing_plan,
        attribute="price",
    )
    price_per_minute = get_price_info(
        pricing_plan_id=sample_pricing_plan_id,
        pricing_plan=sample_pricing_plan,
        attribute="per_min_pricing",
    )

    assert currency == "EUR"
    assert unlock_price == 1
    assert price_per_minute == 0.22
