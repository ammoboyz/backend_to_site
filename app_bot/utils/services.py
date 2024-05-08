import aiofiles


async def get_photo(pic_name: str) -> bytes:
    async def aiofile_request(path: str) -> bytes:
        async with aiofiles.open(path, "rb") as file:
            photo = await file.read()

        return photo

    try:
        photo_bytes = await aiofile_request(
            f"app_general/images/{pic_name}.jpg"
        )
    except FileNotFoundError:
        photo_bytes = await aiofile_request(
            f"app_general/images/main.jpg"
        )

    return photo_bytes
