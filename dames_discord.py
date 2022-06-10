import os
from dotenv import load_dotenv
from discord.ext import commands

from classes.Jeu import Jeu

import asyncio
import nest_asyncio
nest_asyncio.apply()

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix = "/")



async def affiche(msg,message_a_edit):
    await message_a_edit.edit(content=msg)

async def prompt(ctx,joueur : str = False):
    channelBon = False
    bonJoueur = False
    while (not channelBon) or (not bonJoueur) :
        channelBon = False
        bonJoueur = False        
        print(f"entrée dans prompt pour discord : joueur = {joueur}")
        loop = asyncio.get_event_loop()
        coroutine  = bot.wait_for("message")
        msgDiscord = loop.run_until_complete(coroutine)
        print(f"\tMessage reçu !")
        channelBon = msgDiscord.channel == ctx.channel
        if  joueur :
            bonJoueur = msgDiscord.author.display_name == joueur
        else:
            bonJoueur = msgDiscord.author.display_name != ctx.me.display_name
        
        if channelBon and bonJoueur:
            msg = msgDiscord.content.strip()
            print(f"reçu : \"{msg}\"")
            await msgDiscord.delete()
            return msg
        else:
            print("\tmauvaise personne concenée")
    print("ERREUR INTERNE : dans prompt")
    

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
    jeu = Jeu(affiche,prompt,message_a_edit,ctx)
    print("commencement du jeu de dames !")
    jeu.chargementJeu()
    jeu.commenceJeu()
    print("fin du programme")


@bot.event
async def on_message(message):
    await bot.process_commands(message)

bot.run(TOKEN)
