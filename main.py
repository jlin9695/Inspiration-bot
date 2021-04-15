from keep_alive import keep_alive
import discord
import os
import requests
import json
import random
from replit import db

client = discord.Client() #sets the client to a discord client.

sad_words = [
    "sad", "depressed", "unhappy", "heartbroken", "melancholy", "mournful",
    "angry", "miserable"
] #list of word-that the bot should pick up in user messages.

starter_encouragements = [
    "Cheer up!", "Hang in there.", "You are a great person / bot!"
] #first list of example encouragements for the bot to use. This is expanded later on.

if "responding" not in db.keys():
    db["responding"] = True #used to determine if the bot responds to user input or not.


def get_quote(): #inspiration quote function declared 
    response = requests.get("https://zenquotes.io/api/random") #gets quote from zenquotes
    json_data = json.loads(response.text) #loads response into user-readable form.
    quote = json_data[0]['q'] + " - " + json_data[0]['a'] #separates the quote and speaker.
    return (quote) #posts the final response.

def update_encouragements(encouraging_message): #function to add encouragements declared
    if "encouragements" in db.keys(): #checks if encouragements is a key in the dictionary yet.
        encouragements = db["encouragements"] #declares the current list of encouragements as a separate list.
        encouragements.append(encouraging_message) #adds the new encouragement to the list.
        db["encouragements"] = encouragements #posts the updated list back to the database of definitions.
    else: #if encouragements does not already exist in the database
        db["encouragements"] = [encouraging_message] #declares the new dictionary with definition of the suggested message.


def delete_encouragement(index): #function to remove an encouragement declared.
    encouragements = db["encouragements"] #redeclares the current list of encouragements into a list.
    if len(encouragements) > index:   #if the length of the encouragements is larger than the current index declared.
        del encouragements[index] #delete the element that the index indicates.
    db["encouragements"] = encouragements   #establishes the encouragements dictionary with the element removed.


@client.event #watches for a certain event
async def on_ready(): #on_ready is when the bot is fully executed and on standby, is a function built into Discord code itself.
    print('We have logged in as {0.user}'.format(client)) #prints a message onto console that the bot is ready to go.


@client.event #event watcher
async def on_message(message): #function executes when a discord user types in a message
    if message.author == client.user: #checks if the message posted is by the bot itself
        return #makes sure the bot does not execute on messages from itself.

    msg = message.content #establishes the message content as a different variable.

    if msg.startswith('$inspire'): #command for inspirational quote retrieval
        quote = get_quote() #instates the quote function
        await message.channel.send(quote)  #sends the quote into the channel.

    if db["responding"]: #checks if the bot is set to respond.
        options = starter_encouragements #sets the options for the bot to respond with encouragements.
        if "encouragements" in db.keys(): #checks if encouragements as a dictionary exists.
            options += db["encouragements"] #adds all the current encouragements to the options.

        if any(word in msg for word in sad_words): #checks if the message includes any sad words.
            await message.channel.send(random.choice(options)) #gives an encouragement from one of the "options" available.

    if msg.startswith("$new"): #command to add new encouragements.
        encouraging_message = msg.split("$new ", 1)[1] #sets the new encouragement to everything typed after the first command.
        update_encouragements(encouraging_message) #adds the new encouragement to the encouragement dictionary.
        await message.channel.send("New encouraging message added.") #informs users that the encouragement is added.

    if msg.startswith("$del"): #command to delete any encouragements.
        encouragements = [] #sets encouragements to an empty list
        if "encouragements" in db.keys(): #checks if encouragements exists as a database already.
            index = int(msg.split("$del", 1)[1]) #index is the number typed after the command.
            delete_encouragement(index) #deletes the encouragement at the specified index.
            encouragements = db["encouragements"] #establishes the database without the specified encouragement.
        await message.channel.send(encouragements) #shows the new list of encouragements.

    if msg.startswith("$list"): #command for checking list.
        encouragements = [] #establishes an empty encouragement list.
        if "encouragements" in db.keys(): #checks if encouragements is an existing database
            encouragements = db["encouragements"] #puts database into the list
        await message.channel.send(encouragements) #posts list of encouragements

    if msg.startswith("$sleep"): #sleep command
      await message.channel.send("Sleep is a vital, often neglected, component of every person's overall health and well-being. Sleep is important because it enables the body to repair and be fit and ready for another day. Getting adequate rest may also help prevent excess weight gain, heart disease, and increased illness duration.")
      #posts a copypasta about the necessity of sleep
      
    if msg.startswith("$responding"): #command to change response status of the bot
        value = msg.split("$responding", 1)[1] #splits message

        if value.lower() == "true": #checks if responding is set to activate.
            db["responding"] = True #sets bot to active state
            await message.channel.send("Responding is on.") #informs users of active state.
        else: #Any other value
            db["responding"] = False #shuts down the bot
            await message.channel.send("Responding is off.")  #informs users of bot inactive state.


keep_alive() #function to keep the bot active without being logged into it manually.
client.run(os.getenv('TOKEN')) #Gets token for the bot.
