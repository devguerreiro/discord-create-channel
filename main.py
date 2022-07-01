from os import getenv
from dotenv import load_dotenv

from discord.ext import commands
from discord import utils

load_dotenv()
TOKEN = getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!")


async def _create_category_if_not_exist(ctx, category_name):
    if category_name:
        category = utils.find(
            lambda c: c.name == category_name,
            ctx.guild.categories,
        )
        if not category:
            category = await ctx.guild.create_category_channel(category_name)
        return category


async def _create_text_channel_if_not_exist(ctx, channel_name, category=None):
    if not category:
        channel = utils.find(
            lambda c: not c.category and c.name == channel_name,
            ctx.guild.channels,
        )
        if not channel:
            await ctx.guild.create_text_channel(channel_name)
    else:
        channel = utils.find(
            lambda c: c.name == channel_name,
            category.channels,
        )
        if not channel:
            new_channel = await category.create_text_channel(channel_name)
            await new_channel.edit(sync_permissions=True)


@bot.command("nc")
@commands.has_role("SuperMan")
async def handler(ctx, category_name=None, channel_name=None):
    if category_name and channel_name:
        category = await _create_category_if_not_exist(ctx, category_name)
        await _create_text_channel_if_not_exist(ctx, channel_name, category)
    elif category_name:
        channel_name = category_name
        await _create_text_channel_if_not_exist(ctx, channel_name)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You need be a 'SuperMan' to use this command.")


bot.run(TOKEN)
