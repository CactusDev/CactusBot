import aiohttp

BASE_URL = "https://beam.pro/api/v1/channels/{username}"

async def check_user(username):
    """Check if a Beam username exists."""
    if username.startswith('@'):
        username = username[1:]
    async with aiohttp.get(BASE_URL.format(username=username)) as response:
        if response.status == 404:
            raise NameError
        return (username, (await response.json())["id"])
