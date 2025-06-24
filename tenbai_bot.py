import os
import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import tasks

TOKEN = "MTM4NzAxNDA0NDIwNDAxMTYzMg.GErlY8.9WPvQdMz6NjyvDRCAkv0NCMPPjzeE55c3V3ILY"  # Không an toàn để public
CHANNEL_ID = 1197874255350734918  # ID kênh Discord

KEYWORDS = ["ポケモンカード", "NIKE", "Switch", "Travis", "限定", "BOX", "コラボ"]
URLS = [
    "https://www.mercari.com/jp/search/?keyword=NIKE",
    "https://www.suruga-ya.jp/search?category=&search_word=ポケモンカード",
    "https://www.amazon.co.jp/s?k=ポケモンカード",
    "https://www.snkrdunk.com/search?keyword=travis",
    "https://jp.pokemoncenter-online.com/?s=ポケモンカード"
]

intents = discord.Intents.default()
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập: {bot.user}")
    fetch_items.start()

@bot.slash_command(name="ping", description="Kiểm tra bot hoạt động")
async def ping(ctx):
    await ctx.respond("🟢 Bot đang hoạt động!")

@tasks.loop(minutes=10)
async def fetch_items():
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("❌ Không tìm thấy kênh Discord!")
        return

    for url in URLS:
        try:
            response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.find_all("a")

            for item in items:
                text = item.get_text(strip=True)
                link = item.get("href")
                if any(keyword in text for keyword in KEYWORDS):
                    if link and not link.startswith("http"):
                        link = "https://www." + url.split("/")[2] + link
                    await channel.send(f"Sản phẩm có thể lời: **{text}**\n🔗 {link}")
        except Exception as e:
            print(f"Lỗi khi quét {url}: {e}")

bot.run(TOKEN)
