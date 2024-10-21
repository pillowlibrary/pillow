import psutil
import asyncio

# List of common Windows system processes
WINDOWS_PROCESSES = [
    'AggregatorHost.exe', 'ApplicationFrameHost.exe', 'MemCompression', 'MpDefenderCoreService.exe', 
    'MsMpEng.exe', 'NisSrv.exe', 'PhoneExperienceHost.exe', 'Registry', 'RuntimeBroker.exe', 
    'SearchFilterHost.exe', 'SearchIndexer.exe', 'SearchProtocolHost.exe', 'SecurityHealthService.exe', 
    'SecurityHealthSystray.exe', 'SgrmBroker.exe', 'StartMenuExperienceHost.exe', 'System', 
    'System Idle Process', 'TextInputHost.exe', 'UserOOBEBroker.exe', 'conhost.exe', 'csrss.exe',
    'ctfmon.exe', 'dllhost.exe', 'dwm.exe', 'fontdrvhost.exe', 'lsass.exe',  'msedgewebview2.exe',
    'powershell.exe', 'services.exe', 'sihost.exe', 'smss.exe', 'spoolsv.exe',  'svchost.exe',
    'taskhostw.exe', 'wininit.exe', 'winlogon.exe', 'LockApp.exe', 'SearchApp.exe', 'SystemSettings.exe',
    'pet.exe', 'python.exe', 'py.exe', 'ShellExperienceHost.exe'
]

async def send_large_message(channel, message, delay=3):
    """
    Sends a large message to Discord in chunks if it exceeds the 2000-character limit.
    """
    parts = []
    while len(message) > 2000:
        split_index = message[:2000].rfind(" ")
        if split_index == -1:
            split_index = 2000  # If no space is found, split at 2000 chars.

        parts.append(message[:split_index])
        message = message[split_index:]

    parts.append(message)

    for part in parts:
        await channel.send(part)
        await asyncio.sleep(delay)

async def categorize_and_list_processes(bot, channel_id):
    """
    Lists all running processes categorized as applications or background processes.
    """
    applications = []
    background_processes = []

    try:
        for process in psutil.process_iter(['pid', 'name']):
            try:
                process_name = process.info['name']

                # Categorize known Windows system processes as background processes
                if process_name in WINDOWS_PROCESSES:
                    background_processes.append(process_name)
                else:
                    # Anything not in WINDOWS_PROCESSES is considered an application
                    applications.append(process_name)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # Format message
        process_message = "**Running Processes (Sorted):**\n\n"
        
        # Add applications section
        if applications:
            process_message += "**Applications**\n" + "\n".join(sorted(set(applications))) + "\n\n"

        # Add background processes section
        if background_processes:
            process_message += "**Background Processes**\n" + "\n".join(sorted(set(background_processes)))

        # Send to Discord
        channel = bot.get_channel(channel_id)
        if len(process_message) > 2000:
            await send_large_message(channel, process_message, delay=1)
        else:
            await channel.send(process_message)

    except Exception as e:
        await bot.get_channel(channel_id).send(f"**Error listing processes:** {str(e)}")
