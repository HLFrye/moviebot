"""
Main entrypoint for Discord bot

The main() function pulls in the config from arguments, then
asynchronously starts the bot client.
"""

import asyncio
import argparse

import asyncpg
import yaml

from .client import MovieBotClient


async def start(config):
    """
    Asynchronously start the bot client after connecting to the database
    to load the bot's token
    """

    # connect to database
    pool = await asyncpg.create_pool(**config["database"])

    # create bot
    client = MovieBotClient(pool)

    # look up client token from DB
    async with pool.acquire() as conn:
        token = await conn.fetchval("SELECT token FROM Token")

    # run forever
    await client.start(token)


def main():
    """
    Main entrypoint for bot application
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    args = parser.parse_args()

    with open(args.config, encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)

    asyncio.run(start(config))


if __name__ == "__main__":
    main()
