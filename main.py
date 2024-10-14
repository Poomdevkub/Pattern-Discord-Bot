import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import json

# โหลดตัวแปรจากไฟล์ .env
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

if DISCORD_TOKEN is None:
    raise Exception("Discord token not found in environment variables.")
else:
    print("Discord token loaded successfully!")


# ดึง TOKEN จากไฟล์ .env
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Bot Event
@bot.event
async def on_ready():         # ทำงานแบบ Asynchronous
    print("Bot Online!")      # คำสั่ง check bot พร้อมใช้งาน
    synced = await bot.tree.sync() # ทำให้คำสั่ของ bot ซิงค์กับโค้ดของเรา
    print(f"{len(synced)} command(s)")


# แจ้งคนเข้า-ออกเซิร์ฟเวอร์
@bot.event                    
async def on_member_join(member):
    channel = bot.get_channel(962645903188058134)   # ID ห้อง
    text = f"Welcome to server, {member.mention}!"
    
    emmbed = discord.embed(title = 'Welcome to the server!',
                           description = text,
                           color = 0x66FFFF)
    
    await channel.send(text)    # ส่งข้อความไปที่ห้องนี้
    await channel.send(embed = emmbed) # ส่ง Embed ไปที่ห้องนี้
    await member.send(text)     # ส่งข้อความไปที่แชทส่วนตัวของ member
    
    
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(962645903188058134)   # ID ห้อง
    text = f"{member.name} has left the server!"
    await channel.send(text)    # ส่งข้อความไปที่ห้องนี้


# คำสั่ง chat bot
@bot.event
async def on_message(message):
    mes = message.content  # ดึงข้อความที่ถูกส่งมา
    if mes == 'hello':
        await message.channel.send("Hello, I'm here. What's up?.") # ส่งกลับไปที่ห้องนั่น
    # elif "I'm" in mes or "Im" in mes:
    #     await message.channel.send("That's your issue, not mine.")
    elif "wtf" in mes:
        await message.channel.send("It's not your business.")
    elif "hate" in mes:
        await message.channel.send("I don't care.")
    elif mes == 'hi bot':
        await message.channel.send("Hello, " + str(message.author.name))
    elif mes == 'hi':
        await message.channel.send("Hello, " + str(message.author.name))

    await bot.process_commands(message)
    # ทำคำสั่ง event แล้วไปทำคำสั่ง bot command ต่อ



@bot.event

# ฟังก์ชันเพื่อตรวจสอบคำหยาบคาย
async def load_profanity_list(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['profanity']

# โหลดคำหยาบจากไฟล์
profanity_list = load_profanity_list('profanity.json')

# ฟังก์ชันเพื่อตรวจสอบคำหยาบคาย
async def check_profanity(content):
    return any(profanity in content.lower() for profanity in profanity_list)



# กำหนดคำสั่งมให้บอท
@bot.command()
async def hello(ctx):
    await ctx.send(f"hello {ctx. author.name}!")


@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)


# Slash Commands
@bot.tree.command(name='hellobot', description='Replies with Hello')
async def hellocommand(interaction):
    await interaction.response.send_message("Hello It's me BOT DISCORD")


@bot.tree.command(name='name')
@app_commands.describe(name = "What's your name?")
async def namecommand(interaction, name : str):
    await interaction.response.send_message(f"Hello {name}")


# Embeds
@bot.tree.command(name='help', description='Bot Command')
async def helpcommand(interaction):
    emmbed = discord.Embed(title='Help Me! - Bot Commands', 
                           description='Bot Commands',
                           color=0x66FFFF,
                           timestamp=discord.utils.utcnow())
    
    # ใส่ข้อมูล
    emmbed.add_field(name='/hello1', value='Hello Command', inline=True)
    emmbed.add_field(name='/hello2', value='Hello Command', inline=True)
    emmbed.add_field(name='/hello3', value='Hello Command', inline=False)

    emmbed.set_author(name='Author', url='https://www.youtube.com/@cristiano', icon_url='https://yt3.googleusercontent.com/yKfa-GV-v_O-6jZKHwBuc2FX0Q5ths8OqYTOAmOwzVY0q3miZT0L-rUzve-M2QBdONcTYaEO_JI=s160-c-k-c0x00ffffff-no-rj')
    
    
    # ใส่รูปขนาดเล็ก-ใหญ่
    emmbed.set_thumbnail(url='')
    emmbed.set_image(url='')
    
    
    # Footer เนื้อหาส่วนท้าย
    emmbed.set_footer(text='Footer', icon_url='')
    
    
    
    await interaction.response.send_message(embed = emmbed)





bot.run(TOKEN)