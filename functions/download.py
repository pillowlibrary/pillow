import os

DISCORD_FILE_SIZE_LIMIT_MB = 10
FILE_IO_SIZE_LIMIT_MB = 2000
FILE_IO_UPLOAD_URL = "https://file.io"

def is_valid_file_size(file_path, limit_mb=DISCORD_FILE_SIZE_LIMIT_MB):
    file_size = os.path.getsize(file_path) / (1024 * 1024)
    return file_size <= limit_mb

def upload_to_file_io(file_path):
    try:
        from requests import post
        with open(file_path, 'rb') as file:
            response = post(FILE_IO_UPLOAD_URL, files={'file': file})
        if response.status_code == 200:
            return response.json()['link']
        else:
            return f"**Error: Upload failed with status code** `{response.status_code}`"
    except Exception as e:
        return f"**Error: Failed to upload file to file.io** `{e}`"

def compress_directory_to_zip(directory_path):
    import zipfile
    directory_path = directory_path.rstrip("\\/")
    directory_name = os.path.basename(directory_path)
    archive_name = f"{directory_name}.zip"
    archive_path = os.path.join(directory_path, archive_name)
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zip_archive:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, directory_path)
                if full_path != archive_path:
                    zip_archive.write(full_path, arcname=relative_path)
    return archive_path

async def send_file_from_memory(bot, CHANNEL_ID, file_path):
    try:
        if not os.path.isfile(file_path):
            channel = bot.get_channel(CHANNEL_ID)
            await channel.send(f"**Error: Invalid file path** `{file_path}`")
            return
        with open(file_path, 'rb') as file:
            from io import BytesIO
            file_data = BytesIO(file.read())
        channel = bot.get_channel(CHANNEL_ID)
        file_name = os.path.basename(file_path)
        from discord import File
        await channel.send(file=File(fp=file_data, filename=file_name))
    except Exception as e:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f"**Error: Failed to send file** `{e}`")

async def send_large_file(bot, CHANNEL_ID, file_path):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb > FILE_IO_SIZE_LIMIT_MB:
            await channel.send(f"**Error: File size exceeds file.io's 2GB limit, aborting**")
            return
        await channel.send(f"**⚠️ File is a directory or exceeds Discord's limit, uploading to file.io**")
        link = upload_to_file_io(file_path)
        await channel.send(f"Download: {link}")
        if file_path.endswith(".zip"):
            os.remove(file_path)
    except Exception as e:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f"**Error: Failed to handle large file** `{e}`")

async def download_and_send(bot, CHANNEL_ID, file_path):
    try:
        if os.path.isdir(file_path):
            compressed_zip = compress_directory_to_zip(file_path)
            file_size_mb = os.path.getsize(compressed_zip) / (1024 * 1024)
            if file_size_mb > FILE_IO_SIZE_LIMIT_MB:
                channel = bot.get_channel(CHANNEL_ID)
                await channel.send(f"**Error: Compressed directory size exceeds 2GB limit** `{file_size_mb:.2f}` MB")
                os.remove(compressed_zip)
                return
            await send_large_file(bot, CHANNEL_ID, compressed_zip)
        elif os.path.isfile(file_path):
            if not os.access(file_path, os.R_OK):
                channel = bot.get_channel(CHANNEL_ID)
                await channel.send(f"**Error: File cannot be accessed due to permissions** `{file_path}`")
                return
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            if is_valid_file_size(file_path):
                await send_file_from_memory(bot, CHANNEL_ID, file_path)
            else:
                await send_large_file(bot, CHANNEL_ID, file_path)
        else:
            channel = bot.get_channel(CHANNEL_ID)
            await channel.send(f"**Error: Invalid file path** `{file_path}`")
    except Exception as e:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(f"**Error:** `{e}`")
