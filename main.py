''' This bot is here to cheer you up. Key words will prompt it to send encouraging messages
Use the following commands:
 - !hello to greet the bot
 - !inspire to recieve an inspirational quote
 - !add + message to add a new encouragement
 - !reveal to see all saved encouragements in the db
 - !yeet + index to delete an encouragement from the db '''

import os
import discord
import requests
import json
import random
from replit import db

client = discord.Client()

sad_words = ["I'm sad", "depressed", "unhappy", "angry", "pissed", "miserable", "depressing", "big oof", "lonely", "heartbroken", "disapointed", "hopeless", "I'm lost"]
# beyond starter encouragements, users can add aditional nice things to the database through discord commands
starter_encouragements = [
  "You're doing fine sweetie! We love you!",
  "Cheer up buttercup!",
  "I'm sending you lots of hugs!",
  "XOXOXO",
  "Hang in there! You are beautiful!"
]
# quotes pulled from zenquotes API
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = "\"" + json_data[0]['q'] + "\"" + "\n-" + json_data[0]['a']
  return quote
  
# checks if encouragement exists
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]
    
# deletes selected encouragement
def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements
  
# successful startup prompt 
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  # bot will not respond to their own messages
  if message.author == client.user:
    return

  msg = message.content.lower()
  # commands
  if msg.startswith('!hello'):
    await message.channel.send('Hello beautiful!')

  if msg.startswith('!inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  options = starter_encouragements
  if "encouragements" in db.keys():
    options = options + list(db["encouragements"])

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

  if msg.startswith("!reveal"):
    encouragements = list(db["encouragements"])
    for i in range(len(encouragements)):
      await message.channel.send(str(i) + ": " + encouragements[i] + "\n")
    await message.channel.send("To delete a message, type $yeet + index.")

  if msg.startswith("!new"):
    encouraging_message = msg.split("$new ", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New message added! Thank you so much!")

  if msg.startswith("!yeet"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$yeet ", 1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    for i in range(len(encouragements)):
      await message.channel.send(str(i) + ": " + encouragements[i] + "\n")
    await message.channel.send("To delete a message, type $yeet + index.")

  if msg.startswith("thank you bot"):
    await message.channel.send("^w^")

  if msg.startswith("not you optibot"):
    await message.channel.send(":(")
    
client.run(os.environ['TOKEN'])
