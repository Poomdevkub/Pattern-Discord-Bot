import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import openai
import os

# โหลดตัวแปรจากไฟล์ .env
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if DISCORD_TOKEN is None or OPENAI_API_KEY is None:
    raise Exception("Discord token or OpenAI API key not found in environment variables.")
else:
    print("Discord token and OpenAI API key loaded successfully!")

# ตั้งค่า OpenAI API Key
openai.api_key = OPENAI_API_KEY

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# ฟังก์ชันเพื่อตรวจสอบคำหยาบคายโดยใช้ ChatGPT
async def check_profanity(content):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # ใช้โมเดลที่เหมาะสม
            messages=[{"role": "user", "content": f"Check if this message contains profanity: {content}"}]
        )
        result = response.choices[0].message['content'].strip().lower()
        return "yes" in result  # ถ้า ChatGPT ระบุว่ามีคำหยาบ จะคืนค่าเป็น True
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return False

# Bot Event
@bot.event
async def on_ready():
    print("Bot Online!")
    synced = await bot.tree.sync()
    print(f"{len(synced)} command(s) synced")

# แจ้งคนเข้า-ออกเซิร์ฟเวอร์
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(962645903188058134)  # ID ห้อง
    text = f"Welcome to the server, {member.mention}!"
    
    embed = discord.Embed(title='Welcome to the server!',
                           description=text,
                           color=0x66FFFF)
    
    await channel.send(text)    # ส่งข้อความไปที่ห้องนี้
    await channel.send(embed=embed)  # ส่ง Embed ไปที่ห้องนี้
    await member.send(text)     # ส่งข้อความไปที่แชทส่วนตัวของ member

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(962645903188058134)  # ID ห้อง
    text = f"{member.name} has left the server!"
    await channel.send(text)    # ส่งข้อความไปที่ห้องนี้

# คำสั่ง chat bot
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    mes = message.content  # ดึงข้อความที่ถูกส่งมา
    
    # ตรวจจับคำหยาบคาย
    if await check_profanity(mes):
        await message.delete()  # ลบข้อความที่มีคำหยาบคาย
        await message.channel.send(f'{message.author.mention}, your message has been removed due to inappropriate content.')
    else:
        if mes.lower() in ['hello', 'hi bot', 'hi']:
            await message.channel.send(f"Hello, {message.author.name}")

    await bot.process_commands(message)  # ทำคำสั่ง event แล้วไปทำคำสั่ง bot command ต่อ

# กำหนดคำสั่งให้บอท
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}!")

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

# Slash Commands
@bot.tree.command(name='hellobot', description='Replies with Hello')
async def hellocommand(interaction):
    await interaction.response.send_message("Hello, it's me BOT DISCORD!")

@bot.tree.command(name='name')
@app_commands.describe(name="What's your name?")
async def namecommand(interaction, name: str):
    await interaction.response.send_message(f"Hello {name}!")

# Embeds
@bot.tree.command(name='help', description='Bot Command')
async def helpcommand(interaction):
    embed = discord.Embed(title='Help Me! - Bot Commands', 
                           description='Bot Commands',
                           color=0x66FFFF,
                           timestamp=discord.utils.utcnow())
    
    # ใส่ข้อมูล
    embed.add_field(name='/hello', value='Greets the user', inline=True)
    embed.add_field(name='/name', value='Replies with your name', inline=True)
    embed.add_field(name='/help', value='Displays this help message', inline=False)

    embed.set_author(name='Author', url='https://www.youtube.com/@cristiano', 
                     icon_url='https://yt3.googleusercontent.com/yKfa-GV-v_O-6jZKHwBuc2FX0Q5ths8OqYTOAmOwzVY0q3miZT0L-rUzve-M2QBdONcTYaEO_JI=s160-c-k-c0x00ffffff-no-rj')
    
    # ใส่รูปขนาดเล็ก-ใหญ่
    embed.set_thumbnail(url='')  # สามารถเพิ่ม URL ของภาพได้ที่

    embed.set_image(url='')      # สามารถเพิ่ม URL ของภาพได้ที่นี่
    
    # Footer เนื้อหาส่วนท้าย
    embed.set_footer(text='Footer', icon_url='')

    await interaction.response.send_message(embed=embed)

bot.run(DISCORD_TOKEN)
