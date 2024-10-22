import discord
from discord.ext import commands

EMBED_COLOR = 0xcd0000
FOOTER_TEXT = "thilyCore v1.0 beta • pwning noobs since 2015"

class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="**thilyCore Help**", description="Functions:", color=EMBED_COLOR)

        commands_list = sorted(self.context.bot.commands, key=lambda c: c.name)
        for command in commands_list:
            if command.hidden or command.name == "help":
                continue
            name = f"!{command.name} {command.signature}"
            description = command.help or "No description provided."
            embed.add_field(name=name, value=description, inline=False)

        embed.set_footer(text=FOOTER_TEXT)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(color=EMBED_COLOR)
        name = f"!{command.name} {command.signature}"
        embed.title = name
        description = command.help or "No description provided."
        embed.description = description
        embed.set_footer(text=FOOTER_TEXT)
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_error_message(self, error):
        embed = discord.Embed(description="**Error:** Command not found.", color=EMBED_COLOR)
        embed.set_footer(text=FOOTER_TEXT)
        channel = self.get_destination()
        await channel.send(embed=embed)

def setup_help_command(bot):
    bot.help_command = CustomHelpCommand()
