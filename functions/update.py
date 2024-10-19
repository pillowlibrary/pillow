import os
import json

UPDATE_STATUS_FILE = "update_status.json"

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
        files_list = files.split(',')
        set_update_flag(files_list)
        await ctx.send(f"Bot will update the following files on the next run: {', '.join(files_list)}")
    else:
        await ctx.send("Please provide the list of files to update.")
