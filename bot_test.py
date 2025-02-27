#TODO: Add help commands
#
import random
import discord
from discord.ext import commands
from datetime import datetime
import re
import argparse
import configparser

from sam_bot_help import SamBotHelp

class BotConf():
    def __init__(self):
        self.bot_token = None
        self.setup()
    
    def setup(self):
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', '--config', help='Path to config file')
        args = parser.parse_args()

        # Read bot token from config file
        config = configparser.ConfigParser()
        config.read(args.config)
        self.bot_token = config['Input'].get('bot_token')


def main():
    # Set up bot
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    bot_conf = BotConf()
    bot = commands.Bot(command_prefix='!', intents=intents)
    bot.help_command = SamBotHelp()

    @bot.command()
    async def vibecheck(ctx, member: discord.Member):
        """Checks the vibe of a user"""
        if member == None:
            member = ctx.author
        # TODO: Add error handling for when the user doesn't exist
        # TODO:
        guild = ctx.guild
        guild_members = []
        for item in guild.members:
            guild_members.append(item)
        if member not in guild_members:
            await ctx.send('I don\'t know who that is!')
        else:
            temp_list = []
            async for message in ctx.channel.history(limit=5000):
                if message.author.name == member.name and message.content.startswith('!') == False:
                    temp_list.append(message)
            print(f' Length of list: {len(temp_list)}')
            my_message = random.choice(temp_list)
        await ctx.send(f'<@{member.id}> sent "{my_message.content}" on {datetime.strftime(my_message.created_at, "%m/%d/%Y")}.')

    @bot.command()
    async def ghorvas(ctx):
        """I shoot. That's it."""
        await ctx.send('I shoot.')

    @bot.command()
    async def wordcount(ctx, member: discord.Member, arg):
        """Counts the number of times a word has been used by a user in the last 5000 messages."""
        lookback = 5000
        guild = ctx.guild
        guild_members = []
        for item in guild.members:
            guild_members.append(item)
        print(member.display_name)
        if member not in guild_members:
            await ctx.send('I don\'t know who that is!')
        else:
            temp_list = []
            async for message in ctx.channel.history(limit=lookback):
                if message.author.name == member.name:
                    temp_list.append(message)
            print(f' Length of list: {len(temp_list)}')
            word_count = 0
            for message in temp_list:
                words = message.content.split()
                for word in words:
                    if word.lower() == arg.lower():
                        word_count += 1
            await ctx.send(f'<@{member.id}> has written {arg} {word_count} times in the last {lookback} messages!')

    @bot.command()
    async def roll(ctx, arg="1d100"):
        """Rolls a number xdy where x is the number of dice and y is the number of sides."""
        if 'd' in arg:
            num_dice, num_sides = arg.split('d')
            try:
                num_dice = int(num_dice)
                num_sides = int(num_sides)
                if num_dice <= 0 or num_sides <= 0:
                    await ctx.send('Number of dice and number of sides must be positive integers.')
                else:
                    rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
                    total = sum(rolls)
                    await ctx.send(f'Rolling {num_dice}d{num_sides}...> {rolls} (Total: {total}).')
            except ValueError:
                await ctx.send('Invalid input. Please use the format xdy where x is the number of dice and y is the number of sides.')
        else:
            await ctx.send('Invalid input. Please use the format xdy where x is the number of dice and y is the number of sides.')

        # if low == None:
        #     low = 1
        #     high = 100
        # elif high == None:
        #     high = low
        #     low = 1
        # if high < low:
        #     await ctx.send('High number must be larger than low number')
        # else:
        #     roll = random.randrange(int(low),int(high))
        #     await ctx.send(f'Rolling between {low} and {high}...> {roll}.')

    @bot.command()
    async def goodbot(ctx):
        """Thanks the bot for its service."""
        await ctx.send(f'Thanks, {ctx.author.display_name}! <:peepoCheer:690742015339790457>')

    async def check_twitter(message):
        """Checks if a message contains a twitter link and replaces it with an fxtwitter link."""
        twitter_pattern = r'(.*)https:\/\/twitter\.com\/(\w+\/status\/\d+)\?*\S*(.*)'
        x_pattern = r'(.*)https:\/\/x.com\/(\w+\/status\/\d+)\?*\S*(.*)'

        if re.match(twitter_pattern, message.content, flags = re.DOTALL):
            matches = re.match(twitter_pattern, message.content, flags = re.DOTALL)
            prequel = matches.group(1).strip()
            twitter_link = matches.group(2).strip()
            sequel = matches.group(3).strip()
            await message.delete()
            await message.channel.send(f"{message.author.display_name} sent: {prequel} https://fxtwitter.com/{twitter_link} {sequel}")

        elif re.match(x_pattern, message.content, flags=re.DOTALL):
            matches = re.match(x_pattern, message.content, flags = re.DOTALL)
            prequel = matches.group(1).strip()
            x_link = matches.group(2).strip()
            sequel = matches.group(3).strip()
            if message.reference is not None:
                await message.channel.send(f"{message.author.display_name}> sent: {prequel} https://fxtwitter.com/{x_link} {sequel}", reference=message.reference)
            else:
                await message.channel.send(f"{message.author.display_name} sent: {prequel} https://fxtwitter.com/{x_link} {sequel}")
            await message.delete()

    async def check_instagram(message):
        """Checks if a message contains a instagram reel link and replaces it with an ddinstagram link."""
        instagram_pattern = r'(.*)https:\/\/www\.instagram\.com\/(reel|share)\/'

        #https://www.instagram.com/reel/C7T6cJfxnHG/?igsh=MWJqcWpjZTE3cG1qbQ==
        if re.match(instagram_pattern, message.content):
            matches = re.match(instagram_pattern, message.content, flags = re.DOTALL)
            prequel = matches.group(1)
            reel_link = matches.group(2)
            sequel = matches.group(3)
            if message.reference is not None:
                await message.channel.send(f"<@{message.author.id}> sent: {prequel} https://ddinstagram.com/reel/{reel_link} {sequel}", reference=message.reference)
            else:
                await message.channel.send(f"<@{message.author.id}> sent: {prequel} https://ddinstagram.com/reel/{reel_link} {sequel}")
            await message.delete()

    @bot.event
    async def on_message(message):
        bot.loop.create_task(check_twitter(message))
        bot.loop.create_task(check_instagram(message))
        await bot.process_commands(message)

    bot.run(bot_conf.bot_token)

if __name__ == "__main__":
    main()

