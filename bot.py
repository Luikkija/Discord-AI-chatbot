"""
Chatgpt discord bot
"""

from openai import OpenAI
from discord.ext import commands
import discord
from dotenv import load_dotenv
import os

load_dotenv()
discord_token = os.getenv('BOT_TOKEN')
openai_key = os.getenv('OPENAI_API_KEY')
channel_id = os.getenv('CHANNEL_ID')

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key = openai_key,
)

bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())
messages = []

@bot.event
async def on_ready():
    print("Bot online.")

    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send("Bot is ready.")

@bot.command(name = 'bot')
async def ask_openai(ctx, *, question):

    # Call the OpenAI GPT-3 API with the user's question using chat-based completion
    response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": question
        }
    ],

    model= "gpt-3.5-turbo",
    max_tokens= 150
)
    # Get the generated response from OpenAI
    answer = response.choices[0].message.content

    # Send the answer back to the user
    await ctx.send(f'{answer}')

bot.run(discord_token)