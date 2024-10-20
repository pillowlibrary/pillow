import io
import discord
from PIL import ImageGrab, Image
import random
import string

def generate_random_filename():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(10)) + ".png"

async def capture_and_send(bot, CHANNEL_ID):
    try:
        screenshot = ImageGrab.grab(all_screens=True)
        screenshot = screenshot.convert("RGB")

        buffer = io.BytesIO()
        screenshot.save(buffer, format="PNG")
        buffer.seek(0)

        random_filename = generate_random_filename()

        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            file = discord.File(fp=buffer, filename=random_filename)
            await channel.send(file=file)

    finally:
        buffer.close()
        del screenshot
