from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from src.api import api_router


async def not_found(request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": [{"msg": "Not Found."}]},
    )


exception_handlers = {404: not_found}

app = FastAPI(
    exception_handlers=exception_handlers,
    title="App",
    description="TRX",
    version="1.0.0",
)
app.include_router(api_router, prefix="/api/v1")
