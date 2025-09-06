import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# Intents setup (every single permission will be included in them)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is up and running!")
    # HERE
    # channel = client.get_channel(CHANNEL_ID)
    #         if channel:
    #             await channel.send("Hello from your Discord bot!")
    #         else:
    #             print(f"Channel with ID {CHANNEL_ID} not found.")
    #         await client.close() # Close the bot after sending the message
    
@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server, {member.name}!")

@bot.event
async def on_message(message):
    # Bot shouldn't reply to its own messages
    if message.author == bot.user:
        return
    # If any message contains prohibited words, delete it and warn sender
    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention}, language!!")

    await bot.process_commands(message)     # allows bot to continue processing the rest of the messages

# !hello
@bot.command()
async def hello(ctx):   # ctx - context on what triggered the command
    # send in the curr channel (where the context took place)
    await ctx.send(f"Hi {ctx.author.mention}!")     # whoever triggered the command

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Officer")
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to Officer!")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Officer")
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} is no longer an Officer")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
@commands.has_role("Officer")       # role-specific command
async def secret(ctx):
    await ctx.send("Secret...")

@secret.error   # secret is the role-specific command's name
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f"You don't have permission to do that: {error}")

# !dm msg
@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")

@bot.command()
async def reply(ctx):
    await ctx.reply("Replying to your message")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="Poll!", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("🍓")
    await poll_message.add_reaction("🍵")

# MUST be at the end of file
# Otherwise, once bot.run() is called, the event loop starts and the rest of the file never gets registered
bot.run(token, log_handler=handler, log_level=logging.DEBUG)    # Run the bot such that debug logs are saved to handler file