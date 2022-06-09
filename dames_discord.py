import os
from dotenv import load_dotenv
from discord.ext import commands

from classes.Jeu import Jeu


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix = "/")



async def affiche(msg,message_a_edit):
    await message_a_edit.edit(content=msg)

async def prompt(joueur : str):
    msgDiscord = await bot.wait_for("message")
    channelBon = msgDiscord.channel == ctx.channel
    bonJoueur = msgDiscord.author.nick = joueur
    if channelBon and bonJoueur:
        msg = msgDiscord.content.strip()
        await msgDiscord.delete()
        return msg

@bot.event
async def on_ready():
    print("Le bot est prêt.")

@bot.command(aliases = ["dame"])
async def dames(ctx, Arg = None):
    print("commande dames appellée")
    message_a_edit = await ctx.channel.send(
        f"""
        **Jeu des dames**
        """
    )
    jeu = Jeu(affiche,prompt,message_a_edit)
    print("commencement du jeu de dames !")
    jeu.chargementJeu()
    jeu.commenceJeu()
    print("fin du programme")


@bot.event
async def on_message(message):
    await bot.process_commands(message)

bot.run(TOKEN)
