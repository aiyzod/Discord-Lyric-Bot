import discord
from lyric import lyric


# Use Bot to create slash command
bot = discord.Bot()


@bot.slash_command()
async def sing(ctx, keyword: str = None):
    res = await ctx.respond('Searching...')

    song = lyric(keyword)

    if song is None:
        await res.edit_original_response(content='Not Found')
    else:
        embed = discord.Embed(title=song.title,
                              description=song.lyric,
                              colour=discord.Colour.random())
        embed.set_author(name=song.artist)
        embed.set_thumbnail(url=song.img)
        await res.edit_original_response(content='', embed=embed)

bot.run('CLIENT SECRET')