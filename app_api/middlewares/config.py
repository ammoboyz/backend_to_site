from fastapi import Request

from app_api.utils import Settings


class ConfigMiddleware:
    def __init__(
            self,
            config: Settings
    ) -> None:
        self.config = config

    async def __call__(self, request: Request, call_next):
        request.state.config = self.config
        response = await call_next(request)

        return response