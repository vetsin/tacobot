import discord
from discord import app_commands
import os, re, copy
import nltk
nltk.download('cmudict')
from nltk.corpus import cmudict
from utils import load_env

CMU = cmudict.dict()
intents = discord.Intents.all()

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
guilds = {
  discord.Object(id=183730219763499009): {}, # thetacolab
  discord.Object(id=912435960988450886): {'haiku': True}
}

class Haiku:
    level_maxes = [5, 12, 17]

    def __init__(self, text):
        self.text = text

    def _get_syllables(self, word):
        word = ''.join(filter(str.isalnum, word))
        pronunciations = CMU.get(word.lower())

        def count_syl(pron):
            return len([syl for syl in pron if syl[-1].isdigit()])

        syl = [count_syl(pron) for pron in pronunciations] if pronunciations else [1]
        return list(set(syl))

    def _is_haiku(self, words, total=0, level=0, phrases={}):
        if (not words) and (total == self.level_maxes[-1]):
            self.phrases = phrases
            return True
        if not words:
            return False
        if level == len(self.level_maxes):
            return False
        word = words[0]
        remnants = words[1:]

        # print(word)
        # print(get_syllables(word))

        for count in self._get_syllables(word):
            current_total = total + count
            if current_total > self.level_maxes[level]:
                continue

            current_phrases = copy.deepcopy(phrases)
            current_phrases[level] = current_phrases.get(level, [])
            current_phrases[level].append(word)

            if current_total == self.level_maxes[level]:
                level += 1
            result = self._is_haiku(remnants, current_total, level, current_phrases)
            if result:
                return True

        return False

    def is_haiku(self):
        return self._is_haiku(self.text.split())

    def formatted(self):
        return '\n'.join(' '.join(self.phrases[i]) for i in range(len(self.phrases)))

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
  for guild in guilds.keys():
    await tree.sync(guild=guild)

def get_option(iguild, key):
  for guild, conf in guilds.items():
    if iguild.id == guild.id:
      if r := conf.get(key, None):
        return r
  return None

async def handle_haiku(message, content):
  if get_option(message.guild, 'haiku') is not True:
    return
  h = Haiku(content)
  if h.is_haiku():
      await message.reply(h.formatted())

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  mangled = re.sub(r'(?m)^> .*$\n?', '', message.content)
  await handle_haiku(message, mangled)

if __name__ == '__main__':
  load_env()
  assert 'BOT_TOKEN' in os.environ, 'we require the bot token'
  client.run(os.environ['BOT_TOKEN'])