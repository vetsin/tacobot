import discord
from discord import app_commands
import os
from utils import load_env

intents = discord.Intents.all()

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
guilds = [
  discord.Object(id=183730219763499009), # thetacolab
  discord.Object(id=912435960988450886)
]

@tree.command(description="User role self-management", guilds=guilds)
@app_commands.describe(role="The role we want to do the operation on")
async def role(interaction, command: str, role: discord.Role):
  if command == 'add':
    if role in interaction.user.roles:
      await interaction.response.send_message(f"You already have @{role}", ephemeral=True)
    else:
      await interaction.user.add_roles(role)
      await interaction.response.send_message(f"Added @{role} to you!", ephemeral=True)
  elif command == 'remove':
    if role in interaction.user.roles:
      await interaction.user.remove_roles(role)
      await interaction.response.send_message(f"Removed @{role} from you!", ephemeral=True)
    else:
      await interaction.response.send_message(f"You never had that role in the first place", ephemeral=True)

@role.autocomplete('command')
async def command_autocomplete(interaction, current):
  return [
    app_commands.Choice(name='add', value='add'),
    app_commands.Choice(name='remove', value='remove')
  ]

@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')
  for guild in guilds:
    await tree.sync(guild=guild)

if __name__ == '__main__':
  load_env()
  assert 'BOT_TOKEN' in os.environ, 'we require the bot token'
  client.run(os.environ['BOT_TOKEN'])