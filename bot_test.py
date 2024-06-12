# This example requires the 'message_content' intent.

import random
import discord
from discord.ext import commands
from datetime import datetime

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
@bot.command()
async def vibecheck(ctx, member: discord.Member):
    if member == None:
        member = ctx.author
    #TODO: Add error handling for when the user doesn't exist
    #TODO: 
    print(f'arg: {str(member.display_name)}')
    guild = ctx.guild
    guild_members = []
    for item in guild.members:
        guild_members.append(item)
    print(guild_members)
    if member not in guild_members:
        await ctx.send('I don\'t know who that is!')
    else:
        temp_list = []  
        async for message in ctx.channel.history(limit=5000):
            print(f'Author: {message.author.id}')
            print(f'Member: {member.name}')
            if message.author.name == member.name and message.content.startswith('!') == False:
                temp_list.append(message)
        print(f' Length of list: {len(temp_list)}')
        my_message = random.choice(temp_list).content
        await ctx.send(f'<@{member.id}> sent "{my_message}" on {datetime.strftime(message.created_at, "%m/%d/%Y")}.')
    #await ctx.send(f'{ctx.author} is a receipt!')

@bot.command()
async def ghorvas(ctx):
    await ctx.send('I shoot.')

@bot.command()
async def wordcount(ctx, arg):
    guild = ctx.guild
    guild_members = []
    for member in guild.members:
        guild_members.append(member.name)
    print(arg)
    print(guild_members)
    if arg not in guild_members:
        await ctx.send('I don\'t know who that is!')
    else:
        temp_list = []  
        async for message in ctx.channel.history(limit=5000):
            if message.author.name == arg and message.content.startswith('!') == False:
                temp_list.append(message)
        print(f' Length of list: {len(temp_list)}')
        word_count = 0
        for message in temp_list:
            word_count += len(message.content.split())
        await ctx.send(f'{arg} has written {word_count} words in the last 5000 messages.')

bot.run('MTI0OTg5Mzg2ODE4MzIyODU1Nw.G045-u.Hx0JYa9twltIl8Ic611GNzW08VSgJMoP_mIZl0')