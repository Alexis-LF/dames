import os
from dotenv import load_dotenv
from discord.ext import commands

from classes.Jeu import Jeu


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix = "/")



async def affiche(msg,ctx):
    await ctx.channel.send(
    f"""
    *Depuis la console :*
    **{msg}**
    """
    )

@bot.event
async def on_ready():
    print("Le bot est prêt.")

@bot.command(aliases = ["dame"])
async def dames(ctx, Arg = None):
    print("commande dames appellée")
    await ctx.channel.send(
        f"""
        **Jeu des dames**
        """
    )
    jeu = Jeu(affiche,ctx)
    print("commencement du jeu de dames !")
    jeu.chargementJeu()
    jeu.commenceJeu()
    print("fin du programme")


@bot.event
async def on_message(message):
    await bot.process_commands(message)

bot.run(TOKEN)
