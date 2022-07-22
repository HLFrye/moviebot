"""
Discord bot client implementation
"""

import random
import discord
from .db import (
    CREATE_MEMBER_SQL,
    #     CREATE_SHOW_SQL,
    #     ADD_VOTE_SQL,
    CHOOSE_SHOW_SQL,
    SAVE_RECOMMENDATION_SQL,
    GET_RECOMMENDATION_SQL,
    CHOOSE_SHOW_SQL_WITH_EXCLUDES,
    SET_REJECTED_SQL,
    GET_PARENT_SQL,
)


class MovieBotClient(discord.Client):
    """
    The bot's discord client class. Must be initialized with
    an asyncpg connection pool
    """

    def __init__(self, pool):
        """Initializes the bot client, including setting intents"""
        intents = discord.Intents.default()

        # Note: The following two intents have to be manually set,
        # as they are considered privileged intents
        # pylint: disable=assigning-non-slot
        intents.members = True
        # pylint: disable=assigning-non-slot
        intents.reactions = True

        super().__init__(intents=intents)
        self.pool = pool

    async def get_recommendation_for_users(self, user_ids, reject_ids=None):
        """
        Finds recommendation for users given a set of user_ids and
        optionally a set of already rejected recommendations to ignore

        Returns None if no recommendations found, otherwise returns an array
        of possible recommendations
        """

        if reject_ids is None:
            reject_ids = []

        print(f"Looking for {user_ids} recommendations")
        async with self.pool.acquire() as conn:
            if len(reject_ids) > 0:
                shows = await conn.fetch(
                    CHOOSE_SHOW_SQL_WITH_EXCLUDES, user_ids, reject_ids
                )
            else:
                shows = await conn.fetch(CHOOSE_SHOW_SQL, user_ids)
            if len(shows) == 0:
                return None
            choice = random.randint(0, len(shows) - 1)
            return shows[choice]

    async def on_message(self, message):
        """Handles receipt of messages from Discord"""

        if message.channel.id == 738255420388278347:
            if message.content.startswith("!watchwith"):
                user_ids = [u.id for u in message.mentions] + [message.author.id]
                choice = await self.get_recommendation_for_users(user_ids)
                sent = await message.channel.send(
                    content=f"You should watch {choice['name']}"
                )
                async with self.pool.acquire() as conn:
                    await conn.execute(
                        SAVE_RECOMMENDATION_SQL,
                        sent.id,
                        user_ids,
                        choice["show_id"],
                        None,
                    )

    async def on_ready(self):
        """Called when the bot is connected to Discord"""

        async def save_member_info(conn, member):
            """Helper func to save user info to the database"""
            print(f"Storing info for member {member.display_name}")
            await conn.execute(
                CREATE_MEMBER_SQL,
                member.id,
                member.display_name,
                member.guild.name,
                member.name,
                member.nick,
            )

        print(f"{self.user.name} has connected to Discord")

        # Get the guilds the bot is in (should be just 1)
        guild = self.guilds[0]
        print(guild.members)
        async with self.pool.acquire() as conn:
            async for member in guild.fetch_members():
                await save_member_info(conn, member)

            # channel = guild.get_channel(981962732913950781)
            # async for message in channel.history():
            #     if len(message.reactions) > 0:
            #         print(f"Movie: {message.content}")
            #         show_id = await conn.fetchval(CREATE_SHOW_SQL, message.content)
            #         print(f"Suggestor: {message.author.id}")
            #         await conn.execute(ADD_VOTE_SQL, message.author.id, show_id, True)
            #         for reaction in message.reactions:
            #             if reaction.emoji == '👍':
            #                 async for user in reaction.users():
            #                     await conn.execute(ADD_VOTE_SQL, user.id, show_id, True)
            #             if reaction.emoji == '👎':
            #                 async for user in reaction.users():
            #                     await conn.execute(ADD_VOTE_SQL, user.id, show_id, False)

    async def on_raw_reaction_add(self, payload):
        """
        Handles receiving a reaction. This method just examines the info
        and calls the correct method based on the emoji and channel
        """

        print(f"Received raw reaction {payload.emoji}")
        print(payload)
        if payload.channel_id == 738255420388278347:
            if payload.emoji.name == "👎":
                channel = self.get_channel(payload.channel_id)
                # user = self.get_user(payload.user_id)
                message = await channel.fetch_message(payload.message_id)
                await self.handle_recommendation_rejection(message)

    async def handle_recommendation_rejection(self, message):
        """Used to find a new recommendation when a previous one is rejected"""
        print("Handling rejection")
        async with self.pool.acquire() as conn:
            rejected_rec = await conn.fetchrow(GET_RECOMMENDATION_SQL, message.id)
            if rejected_rec is None:
                print(f"Found no rec with ID {message.id}")
                return

            print(f"Found last recommendation {rejected_rec['show_id']}")

            print(f"Processing thumbs down for {rejected_rec['show_id']}")

            rejects = []
            user_ids = []

            # Mark this as not interested
            await conn.execute(SET_REJECTED_SQL, message.id)
            print("Ok, marked not interested")
            # Get all previous recommendations for sequence
            parent_id = message.id
            while parent_id is not None:
                parent_rec = await conn.fetchrow(GET_PARENT_SQL, parent_id)
                if parent_rec is None:
                    break
                rejects.append(parent_rec["show_id"])
                parent_id = parent_rec["parent_message_id"]
                user_ids = parent_rec["user_ids"]

            print(f"Found pre-rejections {rejects} for users {user_ids}")

            # Get new recommendation
            next_choice = await self.get_recommendation_for_users(user_ids, rejects)
            if next_choice is None:
                print("No next choice found")
                await message.channel.send(
                    content="I couldn't find anything else to suggest, "
                    + "you should add more movies to the watch list! :)"
                )
                return

            print("Sending new recommendation")
            # Share new recommendation
            sent = await message.channel.send(
                content=f"You should watch {next_choice['name']}"
            )

            # Store new recommendation
            await conn.execute(
                SAVE_RECOMMENDATION_SQL,
                sent.id,
                user_ids,
                next_choice["show_id"],
                message.id,
            )
            print("Done")
