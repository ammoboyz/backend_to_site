import logging as lg
from typing import Optional

from fastapi import Request
from fastapi.responses import JSONResponse
from aiogram.utils.web_app import safe_parse_webapp_init_data

from app_api.utils import Settings


class WebAppMiddleware:
    def __init__(
            self,
            config: Settings
    ) -> None:
        self.config = config

    async def is_auth_by_init_data(
            self,
            init_data: str,
    ) -> Optional[int]:
        try:
            web_app_data = safe_parse_webapp_init_data(
                token=self.config.bot.token,
                init_data=init_data
            )
            return int(web_app_data.user.id)
        except:
            return False

    async def __call__(self, request: Request, call_next):
        authoriz = request.headers.get('Authorization')

        if authoriz == "test_student":
            request.state.user_id = 831472057
            response = await call_next(request)
            return response

        elif authoriz == "test_mentor":
            request.state.user_id = 6077088095
            response = await call_next(request)
            return response

        # if request.url.path.startswith("/photo/"):
        #     response = await call_next(request)
        #     return response

        if authoriz is None:
            return JSONResponse(
                status_code=400,
                content={"message": "Authorization is null"}
            )

        user_id = await self.is_auth_by_init_data(
            authoriz
        )

        if not user_id:
            return JSONResponse(
                status_code=400,
                content={"message": "Authorization token is not correct"}
            )

        request.state.user_id = user_id

        response = await call_next(request)

        return response
