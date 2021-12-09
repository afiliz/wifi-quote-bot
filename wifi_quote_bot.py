from stayin_alive import keep_alive
import discord
import random
import os

client = discord.Client()
secret_token = os.environ['TOKEN']

quotes_db = []
last_index = -1

# populate quote bot from quotes.txt file
with open('quotes.txt') as f:
  quotes_db = f.readlines()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# have the bot repond on command (! commands)
@client.event
async def on_message(message):
  if message.author == client.user:
        return

  # If a user uses !quote command, print random quote from db (don't use same quote twice)
  if message.content.startswith('!quote'):
    global last_index # make sure last index is tracked globally (can't be tracked within fn)
    sent_quote = False

    while sent_quote == False:
      quote_index = random.randrange(0, len(quotes_db)) # get random quote index

      # keep checking to make sure the last quote isn't picked, exit while loop when done
      if quote_index != last_index:
        await message.channel.send(quotes_db[quote_index])
        last_index = quote_index
        sent_quote = True
  
  # if user uses !add-quote, take quote from message and insert it into text file
  if message.content.startswith('!add-quote'):
    try:
      user_quote = message.content.split('!add-quote ', 1)[1]
    except:
      await message.channel.send("Failed to add a quote to the database. Fix yo syntax!")

  
    quotes_file = open('quotes.txt', 'a')
    quotes_file.write('\n' + user_quote)
    quotes_file.close()
    await message.channel.send("New quote added to the database!")

  # if user uses !help-quote, print message detailing bot's functions
  if message.content.startswith('!help-quote'):
    await message.channel.send("!quote : Prints out a random quote from the gang.\n!add-quote [quote] : Adds a new quote to the quote database.\n!help-quote : You're reading it you dingus.")


keep_alive() # run flask server to keep bot alive
client.run(secret_token)
