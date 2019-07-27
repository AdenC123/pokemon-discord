import time
import random
import discord
import re

#get this from discord developer portal, might break
token = 'NjA0NDAxMzgyNjYxMDI5ODg4.XTtbAA.HVyAzzgRjVTHi2_LjYkVcQ12vIY'

#setup discord object
client = discord.Client()

#setup pokemon object with health and a name, attack lowers opponent health and says something in discord
class Pokemon:
    def __init__(self, name, startingHP):
        self.name = name
        self.hp = startingHP
        self.startingHP = startingHP
    
    async def attack(self, opponent, channel):
        opponent.hp -= random.randint(3,7)
        await client.send_message(channel, "{} attacks! {} has {} health!".format(self.name, opponent.name, opponent.hp))

    def alive(self):
        if self.hp > 0:
            return True
        else:
             return False

    def resetHP(self):
        self.hp = self.startingHP

#list of pokemon
sean = Pokemon("Sean", 20)
tanner = Pokemon("Tanner", 20)
moze = Pokemon("Moze", 20)

pokemon = [sean, tanner, moze]

#list of pokemon name strings, unused
"""
pokeNames = []
for poke in pokemon:
    pokeNames.append(poke.name)
"""

#amount of time to sleep after every message, very jank
sleepTime = .5

async def battle(p1, p2, channel):
    await client.send_message(channel, "A battle between {} and {}!".format(p1.name, p2.name))
    time.sleep(sleepTime * 2)

    #main battle loop, hp can be negative and p1 still attacks one more time after dying
    while p1.alive() and p2.alive():
        await p1.attack(p2, channel)
        time.sleep(sleepTime)
        await p2.attack(p1, channel)
        time.sleep(sleepTime)
    
    #winner check
    if (not p1.alive()) and (not p2.alive()):
        await client.send_message(channel, "It's a tie!")
    elif p1.alive():
        await client.send_message(channel, "{} wins!".format(p1.name))
    elif p2.alive():
        await client.send_message(channel, "{} wins!".format(p2.name))

    #reset health
    p1.resetHP()
    p2.resetHP()

#actual discord events
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #add more stuff here
    if message.content.startswith("!battle"):
        print("battle requested")

        #list of arguments split by a space
        args = message.content.lower().split()
        print(args)

        #player names are the 2nd and 3rd arguments
        try:
            p1Name = args[1]
            p2Name = args[2]
        except IndexError:
            await client.send_message(message.channel, "Wrong number of arguments")
            return

        #get pokemon objects from names using list of pokemon
        for poke in pokemon:
            if poke.name.lower() == p1Name.lower():
                p1 = poke
            elif poke.name.lower() == p2Name.lower():
                p2 = poke

        #do the battle
        try:
            await battle(p1, p2, message.channel)
        except:
            await client.send_message(message.channel, "Something went wrong")
            return

        print("battle over")

client.run(token)