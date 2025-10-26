from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from server.config.logging import structlog_configure
from server.config.settings import get_settings


settings = get_settings()
structlog_configure(
    service_instance_id=settings.service_instance_id,
    service_name=settings.service_name,
    service_namespace=settings.service_namespace,
    service_version=settings.service_version,
    environment=settings.env,
    log_level="notset" if settings.debug else "error",
)
app = FastAPI(
    debug=settings.debug,
    openapi_url="/api/openapi.json" if settings.debug else None,
    docs_url="/api/docs" if settings.debug else None,
    redoc_url="/api/redoc" if settings.debug else None,
)


@app.middleware("http")
async def set_auth_token_type_header_middleware(request: Request, call_next):
    response: Response = await call_next(request)

    if response.status_code == 401:
        response.headers["WWW-Authenticate"] = "Bearer"

    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.project_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from server.config import routes

# Routers
app.include_router(routes.router)


@app.get("/api/health/")
def _health():
    return JSONResponse("ok")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="server.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        proxy_headers=True,
        forwarded_allow_ips="*",
        log_level="debug" if settings.debug else "error",
    )
