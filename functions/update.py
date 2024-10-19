import os

def set_update_flag():
    if not os.path.exists("update_status.txt"):
        with open("update_status.txt", "w") as f:
            f.write("update=false")

    with open("update_status.txt", "w") as f:
        f.write("update=true")

async def update_command(ctx):
    set_update_flag()

    await ctx.send("Bot will check for updates on the next run.")
