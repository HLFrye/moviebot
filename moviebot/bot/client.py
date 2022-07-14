import discord

CREATE_MEMBER_SQL = """
INSERT INTO Users (
    user_id, 
    display_name, 
    guild, 
    name, 
    nick
)
VALUES (
    $1, 
    $2, 
    $3, 
    $4, 
    $5
)
ON CONFLICT(user_id) DO UPDATE
SET
    user_id = EXCLUDED.user_id,
    display_name = EXCLUDED.display_name,
    guild = EXCLUDED.guild,
    name = EXCLUDED.name,
    nick = EXCLUDED.nick
"""    

class MovieBotClient(discord.Client):
    def __init__(self, pool):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents)
        self.pool = pool

    async def on_ready(self):
        print(f"{self.user.name} has connected to Discord")

        # Get the guilds the bot is in (should be just 1)
        guild = self.guilds[0]
        print(f"Found {guild.member_count} members in {guild.name}")
        print(guild.members)
        async with self.pool.acquire() as conn:        
            async for member in guild.fetch_members():
                print(f"Storing info for member {member.display_name}")
                await conn.execute(CREATE_MEMBER_SQL,
                    member.id, 
                    member.display_name, 
                    member.guild.name, 
                    member.name, 
                    member.nick                
                )
