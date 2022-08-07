"""
Tools to get info about a show
"""

import asyncio
from aioimdb import Imdb


async def get_show_info(name):
    """
    Downloads show info from IMDB for a given search string
    """

    async with Imdb() as imdb:
        title = await imdb.search_for_title(name)
        info = await imdb.get_title(title[0]["imdb_id"])
        img_url = info["base"]["image"]["url"]
        outline = info["plot"]["outline"]["text"]
        return {
            "img_url": img_url,
            "outline": outline,
        }


async def start():
    """Async Entrypoint"""

    page = await get_show_info("Stranger Things")  # gets page objects by search
    print(page)
    page = await get_show_info("Jumanji")
    print(page)
    page = await get_show_info("The Gray Man")
    print(page)


def main():
    """Entrypoint for testing"""

    asyncio.run(start())
