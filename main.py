from os import getenv
from dotenv import load_dotenv

from discord.ext import commands
from discord import utils

load_dotenv()
TOKEN = getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!")


@bot.command("nc")
@commands.has_permissions(administrator=True)
async def handler(ctx, categoryName=None, channelName=None):
    if categoryName and channelName:
        category = utils.find(
            lambda c: c.name == categoryName,
            ctx.guild.categories,
        )
        if not category:
            category = await ctx.guild.create_category_channel(categoryName)

        channel = utils.find(
            lambda c: c.name == channelName,
            category.channels,
        )
        if not channel:
            new_channel = await category.create_text_channel(channelName)
            await new_channel.edit(sync_permissions=True)

    elif categoryName:
        channelName = categoryName
        channel = utils.find(
            lambda c: not c.category and c.name == channelName,
            ctx.guild.channels,
        )
        if not channel:
            await ctx.guild.create_text_channel(channelName)
        return


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Você não possui permissão para executar este comando.")


bot.run(TOKEN)
