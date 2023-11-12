"""
Chatgpt discord bot
Programmed by: Samu Niemelä
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
        await channel.send("Bot is now ready.")

@bot.command(name = 'bot')
async def ask_openai(ctx, *, question):

    if question == "help":
        
        embed = discord.Embed(
            title = "**Bot information:**",
            color = 0xff0000
            )
        
        embed.set_thumbnail(url = "https://i.imgur.com/DNsXXq9.jpeg")
        embed.add_field(name= "Bot commands:", value= "ChatGPT answer: **!bot**\n    Help: **!bot help**", inline= False)
        embed.add_field(name= "Automatic actions:", value= "Adds role 'Paska Alaluokka' automatically for a new member.", inline= False)
        embed.set_footer(text = "Information requested by: {}".format(ctx.author.display_name))
        
        await ctx.send(embed=embed)
        return
    
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
    await ctx.reply(f'{answer}')


@ask_openai.error
async def info_error(ctx, error):

    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.reply("Please write a prompt for the bot.")
    
    if isinstance(error, OpenAI.error.RateLimitError):
        await ctx.reply("You are out of credits.")

bot.run(discord_token)
