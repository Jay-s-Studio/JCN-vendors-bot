"""
LogRouting
"""
import time
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute

from app.libs.logger import logger


class LogRouting(APIRoute):
    """LogRouting"""

    def get_route_handler(self) -> Callable:
        """

        :return:
        """
        origin_handler = super().get_route_handler()

        async def route_handler(request: Request) -> Response:
            """

            :param request:
            :return:
            """
            # Before controller, get request body
            start = time.time()
            request_body = await request.body()
            request_message = {
                "http.request.method": request.method,
                "http.request.path": request.url.path,
                "http.request.params": dict(request.query_params)
            }
            if request.method in ("POST", "PUT"):
                try:
                    request_message["http.request.body"] = request_body.decode()
                except Exception as exc:  # noqa
                    logger.warning(exc)
                    request_message["http.request.body"] = ""
            logger.info(request_message)

            # Execute the controller
            response: Response = await origin_handler(request)
            try:
                # After controller process, get response status, body
                try:
                    response_body = response.body.decode()
                except Exception as exc:  # noqa
                    logger.warning(exc)
                    response_body = ""

                response_message = {
                    "response.type": type(response).__name__,
                    "response.status_code": response.status_code,
                    "response.duration": round((time.time() - start) * 1000),
                    "response.body": response_body,
                }
                logger.info(response_message)
                return response
            except Exception as exc:
                logger.warning(exc)
                return response

        return route_handler
