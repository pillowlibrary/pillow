import os
import json
import re

UPDATE_STATUS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "update_status.json")

def ensure_update_file_exists():
    if not os.path.exists(UPDATE_STATUS_FILE):
        data = {
            "update": False,
            "files_to_update": []
        }
        with open(UPDATE_STATUS_FILE, "w") as f:
            json.dump(data, f)

def set_update_flag(files):
    ensure_update_file_exists()
    
    data = {
        "update": True,
        "files_to_update": files
    }
    
    with open(UPDATE_STATUS_FILE, "w") as f:
        json.dump(data, f)

async def update_command(ctx, *, files=None):
    if files:
        files_list = [file.strip() for file in files.split(',')]

        invalid_files = [file for file in files_list if not file.endswith('.py')]
        if invalid_files:
            await ctx.send(f"**Error: Invalid file name** `{', '.join(invalid_files)}`")
            return

        for file in files_list:
            if not re.match(r'^[\w\-.]+\.py$', file):
                await ctx.send(f"**Error: Invalid file name** `{file}`.")
                return

        set_update_flag(files_list)
        await ctx.send(f"✅ **The following files will be updated/added on the next run:** `{', '.join(files_list)}`")
    else:
        await ctx.send("**Please provide the list of files to update** `(e.g. !update delete.py,screenshot.py)`")
