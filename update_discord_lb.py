import json
import discord
from datetime import datetime, timedelta

from config import DISCORD_BOT_TOKEN

TOKEN = DISCORD_BOT_TOKEN
GUILD_ID = 123456789012345678  # Заменить на ID твоего сервера
DAYS = 7

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Бот {client.user} подключён.')
    guild = client.get_guild(GUILD_ID)

    leaderboard = []

    for member in guild.members:
        if member.bot:
            continue

        messages = 0
        reactions = 0

        for channel in guild.text_channels:
            try:
                async for msg in channel.history(limit=500, after=datetime.now() - timedelta(days=DAYS)):
                    if msg.author == member:
                        messages += 1
                        reactions += len(msg.reactions)
            except:
                continue

        user_data = {
            "discord_id": str(member.id),
            "username": str(member),  # sery2013#1234
            "display_name": member.display_name,
            "messages": messages,
            "reactions_given": reactions,
            "joined_at": str(member.joined_at),
            "roles": [r.name for r in member.roles if not r.is_default()]
        }

        leaderboard.append(user_data)

    leaderboard.sort(key=lambda x: x['messages'], reverse=True)

    with open('discord_leaderboard.json', 'w', encoding='utf-8') as f:
        json.dump(leaderboard, f, indent=2, ensure_ascii=False)

    print("Discord leaderboard обновлён.")
    await client.close()

client.run(TOKEN)
