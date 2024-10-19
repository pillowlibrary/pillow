import psutil
import GPUtil
import time
import discord

async def monitor_system(bot, CHANNEL_ID):
    try:
        # Get CPU usage percentage
        cpu_usage = psutil.cpu_percent(interval=1)

        # Get memory usage percentage
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent

        # Get disk usage percentage
        disk_info = psutil.disk_usage('/')
        disk_usage = disk_info.percent

        # Get GPU usage percentage (if available)
        gpus = GPUtil.getGPUs()
        gpu_usage = [gpu.load * 100 for gpu in gpus] if gpus else None

        # Calculate system uptime
        boot_time = psutil.boot_time()
        current_time = time.time()
        uptime_seconds = int(current_time - boot_time)
        uptime_hours, remainder = divmod(uptime_seconds, 3600)
        uptime_minutes, uptime_seconds = divmod(remainder, 60)

        usage_report = (
            "**System Usage Report:**\n\n"
            f"**🖥️ CPU Usage:** ` {cpu_usage}% `\n"
            f"**🧠 Memory Usage:** ` {memory_usage}% `\n"
            f"**💿 Disk Usage:** ` {disk_usage}% `\n"
        )

        # Add GPU information if available
        if gpu_usage is not None:
            gpu_info = ', '.join([f"GPU {i+1}: ` {usage:.2f}% `" for i, usage in enumerate(gpu_usage)])
            usage_report += f"**🎮 GPU Usage:** ` {gpu_info} ` \n"
        else:
            usage_report += "**🎮 GPU Usage:** ` No GPU detected ` \n"

        # Add Uptime after GPU usage
        usage_report += f"**⏳ Uptime:** ` {uptime_hours}h {uptime_minutes}m {uptime_seconds}s `\n"

        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(usage_report)

    except Exception as e:
        error_message = f"Error in system_usage function: {e}"
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(error_message)
