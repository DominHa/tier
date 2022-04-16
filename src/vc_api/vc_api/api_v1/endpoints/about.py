from fastapi import APIRouter, Request

router = APIRouter()
import logging

logger = logging.getLogger(__name__.split(".")[0])


def get_version():
    try:
        with open("/opt/api/__VERSION_SOURCE__", "r") as fp:
            return fp.read()
    except Exception:
        return "0.0.0+unknown"


@router.get("/about")
def about(request: Request):
    # logger.info("request headers", extra={"headers": request.headers})
    """ """
    return {
        "vendor": {
            "name": "Vehicle Cluster API.",
        },
        "version": get_version(),
    }
