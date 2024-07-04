

import discord, asyncio, random, subprocess
from discord.ext import commands

BOT_TOKEN = ""
GUILD_ID = 0
VOICE_CHANNEL_ID = 0

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='disk')
async def disk(ctx):
    d = subprocess.run(['df', '-h'], capture_output=True, text=True)
    await ctx.send(f'```\n{d.stdout}\n```')

@bot.command(name='end')
async def end(ctx, time_in_seconds: int):
    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        await ctx.send('Guild not found.')
        return

    voice_channel = guild.get_channel(VOICE_CHANNEL_ID)
    if voice_channel is None or not isinstance(voice_channel, discord.VoiceChannel):
        await ctx.send('Voice channel not found.')
        return

    if time_in_seconds <= 0:
        time_in_seconds = random.randint(30, 120)

    countdown_message = await ctx.send(f"Time left: {time_in_seconds} seconds.")
    
    while time_in_seconds > 0:
        await asyncio.sleep(1)
        time_in_seconds -= 1
        await countdown_message.edit(content=f"Time left: {time_in_seconds} seconds.")
    
    for member in voice_channel.members:
        try:
            await member.move_to(None)
            print(f'Kicked {member.name} from the voice channel.')
        except discord.Forbidden:
            await ctx.send(f"Bot doesn't have permission to kick {member.name}.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

bot.run(BOT_TOKEN)
