"""
Main entrypoint for Discord bot

The main() function pulls in the config from arguments, then
asynchronously starts the bot client.
"""

import asyncio
import os

import asyncpg
from dotenv import load_dotenv

from .client import MovieBotClient


async def start():
    """
    Asynchronously start the bot client after connecting to the database
    to load the bot's token
    """

    # connect to database
    pool = await asyncpg.create_pool(
        host=os.environ["DATABASE_ADDRESS"],
        port=os.environ["DATABASE_PORT"],
        user=os.environ["DATABASE_USER"],
        password=os.environ["DATABASE_PASSWORD"],
        database=os.environ["DATABASE_NAME"],
    )

    # create bot
    client = MovieBotClient(pool)

    # run forever
    await client.start(os.environ["BOT_TOKEN"])


def main():
    """
    Main entrypoint for bot application
    """

    load_dotenv()

    asyncio.run(start())


if __name__ == "__main__":
    main()
