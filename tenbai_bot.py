import os
import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import tasks, commands

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = 1197874255350734918  # Thay bằng ID kênh bạn muốn gửi vào

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

KEYWORDS = ["ポケモンカード", "NIKE", "Switch", "Travis", "限定", "BOX", "コラボ"]

# Danh sách URL các trang có thể có sản phẩm lời (giới hạn một số trang cơ bản)
URLS = [
    "https://www.mercari.com/jp/search/?keyword=NIKE",
    "https://www.suruga-ya.jp/search?category=&search_word=ポケモンカード",
    "https://www.amazon.co.jp/s?k=ポケモンカード",
    "https://www.snkrdunk.com/search?keyword=travis",
    "https://jp.pokemoncenter-online.com/?s=ポケモンカード"
]

@bot.event
async def on_ready():
    print(f'Đã đăng nhập thành {bot.user}')
    fetch_items.start()

@bot.slash_command(name="ping", description="Kiểm tra hoạt động bot")
async def ping(ctx):
    await ctx.respond("Bot đang hoạt động!")

@tasks.loop(minutes=10)
async def fetch_items():
    channel = bot.get_channel(CHANNEL_ID)
    for url in URLS:
        try:
            response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.find_all("a")
            for item in items:
                text = item.get_text()
                link = item.get("href")
                if any(keyword in text for keyword in KEYWORDS):
                    if link and not link.startswith("http"):
                        link = "https://www." + url.split("/")[2] + link
                 await channel.send(f"Sản phẩm có thể trả lời: **{text.strip()}**\n🔗 {link}")
🔗 {link}")
        except Exception as e:
            print(f"Lỗi khi quét {url}: {e}")

bot.run(TOKEN)
