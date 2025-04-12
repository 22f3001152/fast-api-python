import logging
import traceback

from fastapi import Request
from pydantic import BaseModel


class RequestInfo:
    def __init__(self, request) -> None:
        self.request = request

    @property
    def method(self) -> str:
        return str(self.request.method)

    @property
    def route(self) -> str:
        return self.request["path"]

    @property
    def ip(self) -> str:
        return str(self.request.client.host)

    @property
    def url(self) -> str:
        return str(self.request.url)

    @property
    def host(self) -> str:
        return str(self.request.url.hostname)

    @property
    def headers(self) -> dict:
        return {key: value for key, value in self.request.headers.items()}

    @property
    def body(self) -> dict:
        return self.request.state.body


class RequestLog(BaseModel):
    req_id: str
    method: str
    route: str
    ip: str
    url: str
    host: str
    body: dict
    headers: dict


class ErrorLog(BaseModel):
    req_id: str
    error_message: str


logger = logging.getLogger("fastapi-logger")


def log_request(request: Request):
    request_info = RequestInfo(request)
    request_log = RequestLog(
        req_id=request.state.req_id,
        method=request_info.method,
        route=request_info.route,
        ip=request_info.ip,
        url=request_info.url,
        host=request_info.host,
        body=request_info.body,
        headers=request_info.headers,
    )
    logger.info(request_log.dict())


def log_error(uuid: str, response_body: dict):
    error_log = ErrorLog(
        req_id=uuid,
        error_message=response_body["error_message"],
    )
    logger.error(error_log.dict())
    logger.error(traceback.format_exc())
