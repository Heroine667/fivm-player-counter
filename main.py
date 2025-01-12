import discord
from discord.ext import commands, tasks
import requests

TOKEN = '' # discord bot token
FIVEM_SERVER_ENDPOINT = 'http://IP:PORT/players.json' # remplace by ur ip:port

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    update_player_count.start()

@tasks.loop(seconds=60)  # Update every 60 seconds
async def update_player_count():
    try:
        response = requests.get(FIVEM_SERVER_ENDPOINT)
        response.raise_for_status()
        players_data = response.json()
        player_count = len(players_data)
        await bot.change_presence(activity=discord.Game(name=f"{player_count} players online"))
    except requests.RequestException:
        print("Error fetching player count")

@bot.command(name='players')
async def players(ctx):
    try:
        response = requests.get(FIVEM_SERVER_ENDPOINT)
        response.raise_for_status()
        players_data = response.json()
        player_count = len(players_data)
        await ctx.send(f"There are currently **{player_count}** players online on the FiveM server.")
    except requests.RequestException:
        await ctx.send("Sorry, I couldn't fetch the player count at this time.")

bot.run(TOKEN)