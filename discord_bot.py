import commands.dames_discord
from config import TOKEN, bot

@bot.event
async def on_ready():
    print(f"{bot.user.display_name} is connected! (Python)")

@bot.event
async def on_message(message):
    await bot.process_commands(message)

def main():
    _ = bot.run(TOKEN)

if __name__ == "__main__":
    main()
