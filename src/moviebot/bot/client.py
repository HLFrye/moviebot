import random
import discord
from .db import (
    CREATE_MEMBER_SQL, 
    CREATE_SHOW_SQL, 
    ADD_VOTE_SQL,
    CHOOSE_SHOW_SQL,
)

class MovieBotClient(discord.Client):
    def __init__(self, pool):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents)
        self.pool = pool

    async def on_message(self, message):
        if message.channel.id == 738255420388278347:
            if message.content.startswith("!watchwith"):
                print("***")
                user_ids = [u.id for u in message.mentions]
                print(user_ids)
                async with self.pool.acquire() as conn:
                    shows = await conn.fetch(CHOOSE_SHOW_SQL, user_ids)
                    print(f"Found {len(shows)} shows")
                    print(shows)
                    choice = random.randint(0, len(shows) - 1)
                    print(f"Choosing {shows[choice]}")
                    await message.channel.send(content=f"You should watch {shows[choice]['name']}")
        print(message)
        print("---")
        print(message.content)
        print("---")
        print(message.mentions)
        print("***")

    async def on_ready(self):
        async def save_member_info(conn, member):
            print(f"Storing info for member {member.display_name}")
            await conn.execute(CREATE_MEMBER_SQL,
                member.id, 
                member.display_name, 
                member.guild.name, 
                member.name, 
                member.nick                
            )


        print(f"{self.user.name} has connected to Discord")

        # Get the guilds the bot is in (should be just 1)
        guild = self.guilds[0]
        print(f"Found {guild.member_count} members in {guild.name}")
        print(guild.members)
        async with self.pool.acquire() as conn:        
            async for member in guild.fetch_members():
                await save_member_info(conn, member)
            channels = await guild.fetch_channels()
            for channel in channels:
                print(f"{channel} {channel.id}")

                if channel.id == 981962732913950781:
                    async for message in channel.history():
                        if len(message.reactions) > 0:
                            print(f"Movie: {message.content}")
                            show_id = await conn.fetchval(CREATE_SHOW_SQL, message.content)
                            print(f"Suggestor: {message.author.id}")
                            await conn.execute(ADD_VOTE_SQL, message.author.id, show_id, True)
                            yays = []
                            nays = []
                            for reaction in message.reactions:
                                if reaction.emoji == '👍':
                                    async for user in reaction.users():
                                        await conn.execute(ADD_VOTE_SQL, user.id, show_id, True)
                                        yays.append(str(user.id))
                                if reaction.emoji == '👎':
                                    async for user in reaction.users():
                                        await conn.execute(ADD_VOTE_SQL, user.id, show_id, False)
                                        nays.append(str(user.id))
                            if len(yays) > 0:
                                print(f"Yays: {', '.join(yays)}")
                            if len(nays) > 0:
                                print(f"Nays: {', '.join(nays)}")
        