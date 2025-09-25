import discord
from discord.ext import commands
import logging
import os
from dotenv import load_dotenv
from gemini import ask_gemini

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Logging setup
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logging.info(f"Bot connected as {bot.user}")
    print(f"✅ Bot is online as {bot.user}")

@bot.command(name="ask")
async def ask_ai(ctx, *, question: str):
    logging.info(f"Question from {ctx.author}: {question}")
    await ctx.send("🤖 Thinking...")
    answer = ask_gemini(question)
    await ctx.send(answer)

@bot.command(name="log")
async def show_log(ctx):
    try:
        with open("logs/bot.log", "r") as f:
            lines = f.readlines()[-10:]  # Show last 10 log entries
        log_text = "📜 Last 10 log entries:\n" + "".join(lines)
        await ctx.send(f"```\n{log_text}\n```")
    except Exception as e:
        await ctx.send(f"❌ Failed to read log: {e}")

@bot.event
async def on_command_error(ctx, error):
    logging.error(f"Error: {error}")
    await ctx.send(f"❌ Error: {error}")

bot.run(TOKEN)
