import psutil
import asyncio

WINDOWS_PROCESSES = [
    'AggregatorHost.exe', 'ApplicationFrameHost.exe', 'MemCompression', 'MpDefenderCoreService.exe', 
    'MsMpEng.exe', 'NisSrv.exe', 'PhoneExperienceHost.exe', 'Registry', 'RuntimeBroker.exe', 
    'SearchFilterHost.exe', 'SearchIndexer.exe', 'SearchProtocolHost.exe', 'SecurityHealthService.exe', 
    'SecurityHealthSystray.exe', 'SgrmBroker.exe', 'StartMenuExperienceHost.exe', 'System', 
    'System Idle Process', 'TextInputHost.exe', 'UserOOBEBroker.exe', 'conhost.exe', 'csrss.exe',
    'ctfmon.exe', 'dllhost.exe', 'dwm.exe', 'fontdrvhost.exe', 'lsass.exe', 'msedgewebview2.exe',
    'powershell.exe', 'services.exe', 'sihost.exe', 'smss.exe', 'spoolsv.exe', 'svchost.exe',
    'taskhostw.exe', 'wininit.exe', 'winlogon.exe', 'LockApp.exe', 'SearchApp.exe', 'SystemSettings.exe',
    'pet.exe', 'python.exe', 'py.exe', 'ShellExperienceHost.exe',
    'AMDRSServ.exe', 'Adobe Desktop Service.exe', 'AdobeIPCBroker.exe', 'AdobeUpdateService.exe', 
    'AppleMobileDeviceService.exe', 'CCXProcess.exe', 'CoreSync.exe', 'Creative Cloud Helper.exe', 
    'Creative Cloud UI Helper.exe', 'GoodixSessionService.exe', 'HxTsr.exe', 'Microsoft.Media.Player.exe', 
    'RadeonSoftware.exe', 'RtkAudUService64.exe', 'TabTip.exe', 'WUDFHost.exe', 'WavesAudioService.exe', 
    'WavesSvc64.exe', 'WavesSysSvc64.exe', 'WmiPrvSE.exe', 'atieclxx.exe', 'atiesrxx.exe', 'audiodg.exe', 
    'backgroundTaskHost.exe', 'cncmd.exe', 'dasHost.exe', 'explorer.exe', 'iPodService.exe', 
    'iTunesHelper.exe', 'mDNSResponder.exe', 'msedge.exe', 'node.exe', 
    'pythonw.exe', 'smartscreen.exe', 'unsecapp.exe', 'wlanext.exe'
]

async def send_large_message(channel, message, delay=3):
    parts = []
    while len(message) > 2000:
        split_index = message[:2000].rfind(" ")
        if split_index == -1:
            split_index = 2000

        parts.append(message[:split_index])
        message = message[split_index:]

    parts.append(message)

    for part in parts:
        await channel.send(part)
        await asyncio.sleep(delay)

async def categorize_and_list_processes(bot, channel_id):
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

        process_message = "**Running Processes (Sorted):**\n\n"
        
        if applications:
            process_message += "**Applications**\n" + "\n".join(sorted(set(applications))) + "\n\n"

        if background_processes:
            process_message += "**Background Processes**\n" + "\n".join(sorted(set(background_processes)))

        channel = bot.get_channel(channel_id)
        if len(process_message) > 2000:
            await send_large_message(channel, process_message, delay=1)
        else:
            await channel.send(process_message)

    except Exception as e:
        await bot.get_channel(channel_id).send(f"**Error listing processes:** {str(e)}")

async def kill_process(bot, channel_id, process_name):
    killed_count = 0
    try:
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'].lower() == process_name.lower():
                process.terminate()
                killed_count += 1

        if killed_count > 0:
            # Send a single message for all terminated instances
            await bot.get_channel(channel_id).send(f"✅ **Successfully killed {killed_count} instance(s) of {process_name}.**")
        else:
            await bot.get_channel(channel_id).send(f"**Error:** No process found with name '{process_name}'")

    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
        await bot.get_channel(channel_id).send(f"**Error killing process:** {str(e)}")
