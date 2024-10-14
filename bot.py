import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import json

# โหลดตัวแปรจากไฟล์ .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    raise Exception("Discord token not found in environment variables.")
else:
    print("Discord token loaded successfully!")

# สร้าง instance ของ bot
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# ฟังก์ชันโหลดคำหยาบคาย
def load_profanity_list(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['profanity']

# โหลดคำหยาบจากไฟล์
profanity_list = load_profanity_list('profanity.json')

# ฟังก์ชันเพื่อตรวจสอบคำหยาบคาย
def check_profanity(content):
    return any(profanity in content.lower() for profanity in profanity_list)

# Bot Event
@bot.event
async def on_ready():
    print("Bot Online!")
    synced = await bot.tree.sync()
    print(f"{len(synced)} command(s)")

# แจ้งคนเข้า-ออกเซิร์ฟเวอร์
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(962645903188058134)  # ID ห้อง
    text = f"Welcome to server, {member.mention}!"
    
    embed = discord.Embed(title='Welcome to the server!', description=text, color=0x66FFFF)
    
    await channel.send(text)
    await channel.send(embed=embed)
    await member.send(text)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(962645903188058134)  # ID ห้อง
    text = f"{member.name} has left the server!"
    await channel.send(text)

# คำสั่ง chat bot
@bot.event
async def on_message(message):
    # ไม่ให้ bot ตอบข้อความของตัวเอง
    if message.author == bot.user:
        return
    
    mes = message.content  # ดึงข้อความที่ถูกส่งมา
    
    # ตรวจสอบคำหยาบ
    if check_profanity(mes):
        await message.delete()  # ลบข้อความที่มีคำหยาบ
        await message.channel.send(f"{message.author.mention}, please avoid using offensive language.")
        return

    if mes == 'hello':
        await message.channel.send("Hello, I'm here. What's up?")
    elif "wtf" in mes:
        await message.channel.send("It's not your business.")
    elif "hate" in mes:
        await message.channel.send("I don't care.")
    elif mes == 'hi bot':
        await message.channel.send("Hello, " + str(message.author.name))
    elif mes == 'hi':
        await message.channel.send("Hello, " + str(message.author.name))

    await bot.process_commands(message)

# กำหนดคำสั่งให้บอท
@bot.command()
async def hello(ctx):
    await ctx.send(f"hello {ctx.author.name}!")

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

# Slash Commands
@bot.tree.command(name='hellobot', description='Replies with Hello')
async def hellocommand(interaction):
    await interaction.response.send_message("Hello It's me BOT DISCORD")

@bot.tree.command(name='name')
@app_commands.describe(name="What's your name?")
async def namecommand(interaction, name: str):
    await interaction.response.send_message(f"Hello {name}")

# Embeds
@bot.tree.command(name='help', description='Bot Command')
async def helpcommand(interaction):
    embed = discord.Embed(title='Help Me! - Bot Commands', 
                          description='Bot Commands',
                          color=0x66FFFF,
                          timestamp=discord.utils.utcnow())
    
    # ใส่ข้อมูล
    embed.add_field(name='/hello', value='Hello Command', inline=True)
    embed.add_field(name='/name', value='Name Command', inline=True)
    embed.add_field(name='/help', value='Help Command', inline=False)

    embed.set_author(name='Author', url='https://www.youtube.com/@cristiano', 
                     icon_url='https://yt3.googleusercontent.com/yKfa-GV-v_O-6jZKHwBuc2FX0Q5ths8OqYTOAmOwzVY0q3miZT0L-rUzve-M2QBdONcTYaEO_JI=s160-c-k-c0x00ffffff-no-rj')
    
    # ใส่รูปขนาดเล็ก-ใหญ่
    embed.set_thumbnail(url='')
    embed.set_image(url='')
    
    # Footer เนื้อหาส่วนท้าย
    embed.set_footer(text='Footer', icon_url='')
    
    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)
