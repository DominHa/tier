import asyncio
import logging
import time
from concurrent.futures import ThreadPoolExecutor

import uvicorn

from fastapi import FastAPI, Request

from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from vc_api.api_v1.api import api_router as api_v1_router


TAG_DESCRIPTIONS = []

app = FastAPI(docs_url="/v1/docs", openapi_url="/v1/docs/openapi.json")
app.include_router(api_v1_router, prefix="/v1")


app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https://.*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    try:
        openapi_schema = get_openapi(
            title="Vehicle Cluster Api",
            version="0.0.0",
            description="Get information on Tier vehicles.",
            routes=app.routes,
        )
    except Exception as err:
        pass
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

logger = logging.getLogger(__name__.split(".")[0])


@app.middleware("http")
async def log_requests(request: Request, call_next):
    now = time.perf_counter()

    response = await call_next(request)
    elapsed_ms = round(1000 * (time.perf_counter() - now), 1)
    # ignore calls which are very often. Helps to reduce log file size
    if "/about" or "/status" in request.url.path:
        return response

    logging.getLogger("vc_api").info(
        "http request finished",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": elapsed_ms,
        },
    )
    return response


@app.on_event("startup")
async def startup_event():
    asyncio.get_event_loop().set_default_executor(ThreadPoolExecutor(max_workers=4))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
