import discord
from discord.ext import commands

class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="**thilyCore Help**", description="Functions:", color=0xcd0000)

        # Create a sorted list of commands, but exclude the 'help' command
        commands_list = sorted(self.context.bot.commands, key=lambda c: c.name)
        for command in commands_list:
            if command.hidden or command.name == "help":  # Skip hidden and 'help' command
                continue
            name = f"!{command.name} {command.signature}"
            description = command.help or "No description provided."
            embed.add_field(name=name, value=description, inline=False)

        # Set the footer for the help embed
        embed.set_footer(text="thilyCore v0.1 alpha • pwning noobs since 2015")

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        pass

    async def send_error_message(self, error):
        pass

def setup_help_command(bot):
    bot.help_command = CustomHelpCommand()
