import json
import logging
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.concurrency import iterate_in_threadpool

from src.configs.database.database import engine
from src.configs.logging.error_handlers import log_error, log_request
from src.configs.logging.log_config import LOGGING_CONFIG
from src.posts import models
from src.posts.router import ItemsAPI

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
logging.config.dictConfig(LOGGING_CONFIG)


async def log_middleware(request: Request, call_next):
    req_id = str(uuid.uuid4())
    try:
        #### request ####
        request.state.req_id = req_id
        request.state.body = json.loads(await request.body() or "{}")
        log_request(request)

        #### response ####
        response = await call_next(request)
        response_body = ""
        if response.headers.get("content-type") == "application/json":
            response_body = [chunk async for chunk in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))
        return response
    except Exception:
        # Unexpected error handling
        log_error(req_id, {"error_message": "ERR_UNEXPECTED"})
        raise HTTPException(status_code=500, detail="ERR_UNEXPECTED")


app.middleware("http")(log_middleware)
app.include_router(ItemsAPI.routes())
