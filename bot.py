import discord
import openai
from discord.ext import commands

# ตั้งค่า API Key ของ OpenAI
openai.api_key = 'YOUR_OPENAI_API_KEY'

# ตั้งค่าบอท Discord
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# ฟังก์ชันเพื่อส่งข้อความไปยัง ChatGPT
async def ask_chatgpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # ใช้โมเดล ChatGPT
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

# โต้ตอบกับ ChatGPT เมื่อผู้ใช้ส่งข้อความใน Discord
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('!ask'):
        question = message.content[len('!ask '):]  # ตัด '!ask' ออกเพื่อเอาแต่คำถาม
        response = await ask_chatgpt(question)
        await message.channel.send(response)
    
    await bot.process_commands(message)

# รันบอทด้วย Token ของคุณ
bot.run('YOUR_DISCORD_BOT_TOKEN')
