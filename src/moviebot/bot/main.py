import yaml
import argparse
import asyncpg
import asyncio

from .client import MovieBotClient

async def start(config):
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
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.load(f, Loader=yaml.Loader)
    
    asyncio.run(start(config))    

if __name__ == "__main__":
    main()