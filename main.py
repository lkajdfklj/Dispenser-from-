import discord
from discord.ext import commands
import random
from links import links

intents = discord.Intents.all()
activity = discord.Activity(type=discord.ActivityType.watching, name="for new links.")
bot = commands.Bot(command_prefix="!", intents=intents)


class SimpleView(discord.ui.View):
    url = ('https://cdn.discordapp.com/attachments/1195877766147604532/1218398301070819358/hit.png?ex=6610bf57&is=65fe4a57&hm=89a784c3b7e1c8b9edd37767fe749f32c857727bdb85f8d0267be99ff92d0706&')

    cooldown = commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.member)

    @discord.ui.button(label="Get Link",
                       style=discord.ButtonStyle.primary)
    async def hello(self, interaction: discord.Interaction, button: discord.ui.Button):
        bucket = self.cooldown.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            await interaction.response.send_message(
                f"Slow Down! This button is on cooldown. Try again in {round(retry, 1)} seconds.", ephemeral=True)
        else:
            dm = await interaction.user.create_dm()
            embed = discord.Embed(title="Here's your link!", description=random.choice(links),
                                  color=discord.Color.orange())
            embed.set_footer(text="Leak = Ban :)", icon_url=self.url)
            await dm.send(embed=embed)
            await interaction.response.send_message("Successfully sent dm.", ephemeral=True)


@bot.hybrid_command()
async def panel(ctx):
    if str(ctx.author.id) == "1002565312681611354":
        embed = discord.Embed(title="Dispenser", description="Click the button to get your link from the dispenser!",
                              color=discord.Color.orange())
        embed.set_footer(text="Dispenser", icon_url=bot.user.avatar.url)
        view = SimpleView()
        await ctx.send(embed=embed, view=view)

@bot.command(name="sync")
async def sync(ctx):
    if str(ctx.author.id) == '1002565312681611354':
        synced = await bot.tree.sync()
        await ctx.send(f"Synced {len(synced)} command(s).")
    else:
        await ctx.send("Error: You don't have permissions to run this command!")


@bot.event
async def on_ready():
    await bot.change_presence(activity=activity)
    print(f"Logged in as {bot.user}")


bot.run('MTIyMzY5NzAzNjM2MTMzODkzMA.G8ZhCt.Ivbt-rYyHd0kxQihFWiEDTDsCoqZQ8TeN2gJIk')
