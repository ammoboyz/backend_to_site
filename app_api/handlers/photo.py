from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import aiofiles

from app_api.database import get_db


async def get_photo(
        request: Request
):
    user_id: int = request.state.user_id

    if user_id == "main.jpg":
        file_path = "app_general/images/main.jpg"
    else:
        file_path = f"app_general/images/{user_id}.jpg"

    try:
        async with aiofiles.open(file_path, "rb") as file:
            content = await file.read()
    except FileNotFoundError:
        return FileResponse(
            status_code=200,
            path="app_general/images/main.jpg"
        )

    return FileResponse(
        status_code=200,
        path=file_path
    )

def register(app: FastAPI):
    app.add_api_route("/photo", get_photo, methods=["GET"])
