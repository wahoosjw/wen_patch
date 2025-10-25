#TODO: Add help commands
#
import random
import discord
from discord.ext import commands
from datetime import datetime
import re
import argparse
import configparser
import boto3

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
        self.boto3_secret = config['Input'].get('boto3_secret')
        self.aws_key = config['Input'].get('aws_key')
        self.region = config['Input'].get('region')
        self.instance_id = config['Input'].get('instance_id')

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


    @bot.command()
    async def startmc(ctx):
        """Starts the AWS instance defined in the config."""
        try:
            # Initialize the boto3 client
            session = boto3.Session(
                aws_access_key_id=bot_conf.aws_key,
                aws_secret_access_key=bot_conf.boto3_secret,
                region_name=bot_conf.region
            )
            ec2 = session.client('ec2')

            # Start the instance
            response = ec2.start_instances(InstanceIds=[bot_conf.instance_id])
            instance_state = response['StartingInstances'][0]['CurrentState']['Name']

            await ctx.send(f"Minecraft is starting now. Current state: {instance_state}.")
        except Exception as e:
            await ctx.send(f"Failed to start the Minecraft server")

    @bot.command()
    async def stopmc(ctx):
        """Stops the AWS instance defined in the config."""
        try:
            # Initialize the boto3 client
            session = boto3.Session(
                aws_access_key_id=bot_conf.aws_key,
                aws_secret_access_key=bot_conf.boto3_secret,
                region_name=bot_conf.region
            )
            ec2 = session.client('ec2')

            # Stop the instance
            response = ec2.stop_instances(InstanceIds=[bot_conf.instance_id])
            instance_state = response['StoppingInstances'][0]['CurrentState']['Name']

            await ctx.send(f"Minecraft is stopping now. Current state: {instance_state}.")
        except Exception as e:
            await ctx.send(f"Failed to stop the Minecraft server")


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
        """Checks if a message contains an Instagram reel or share link and replaces it with a kkinstagram link."""
        instagram_pattern = r'(.*)https:\/\/(www\.)?instagram\.com\/(reel|share)(?:\/reel)?\/([^\/\?\s]*)\?*\S*(.*)'


        if re.match(instagram_pattern, message.content):
            matches = re.match(instagram_pattern, message.content, flags=re.DOTALL)
            prequel = matches.group(1).strip()
            reel_or_share = matches.group(3).strip()
            link_id = matches.group(4).strip()
            sequel = matches.group(5).strip()
            if reel_or_share == 'share':
                if 'reel' not in sequel:
                    new_link = f"https://kkinstagram.com/share/reel/{link_id}"
            else:
                new_link = f"https://kkinstagram.com/reel/{link_id}"
            if message.reference is not None:
                await message.channel.send(f"<@{message.author.id}> sent: {prequel} {new_link} {sequel}", reference=message.reference)
            else:
                await message.channel.send(f"<@{message.author.id}> sent: {prequel} {new_link} {sequel}")
            await message.delete()

    @bot.event
    async def on_message(message):
        bot.loop.create_task(check_twitter(message))
        bot.loop.create_task(check_instagram(message))
        await bot.process_commands(message)

    bot.run(bot_conf.bot_token)

if __name__ == "__main__":
    main()

