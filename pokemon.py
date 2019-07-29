import time
import random
import discord
import re

#get this from discord developer portal, might break
token = 'NjA0NDAxMzgyNjYxMDI5ODg4.XT6Phg.JvEiaEIYkUsIJbMu7OnxLqtAqWs'

#other variables to change
#amount of time to sleep after every message, doesnt work very well
sleepTime = .5

#low and high values for damage, picks a random number between these
damageMin = 3
damageMax = 7

#setup discord object
client = discord.Client()

#setup pokemon object with health and a name, attack lowers opponent health and says something in discord
class Pokemon:
    def __init__(self, name, startingHP):
        self.name = name
        self.hp = startingHP
        self.startingHP = startingHP
    
    async def attack(self, opponent, channel):
        opponent.hp -= random.randint(damageMin, damageMax)
        await client.send_message(channel, "{} attacks! {} has {} health!".format(self.name, opponent.name, opponent.hp))

    def alive(self):
        if self.hp > 0:
            return True
        else:
             return False

    def resetHP(self):
        self.hp = self.startingHP

#create list of pokemon from the mons.txt file
pokemon = []

mons = open("mons.txt", "r")

for line in mons:
    attributes = line.split()
    name = attributes[0]
    health = int(attributes[1])

    #add pokemon objects to the list
    pokemon.append(Pokemon(name, health))

mons.close()

#function to add a pokemon to the mons.txt file
def addMon(name, hp):
    #make hp an int
    hp = int(hp)

    mons = open("mons.txt", "a")

    #start with a newline, then the name and health separated by a space
    mons.write("\n{} {}".format(name, hp))

    #add it to the pokemon list
    pokemon.append(Pokemon(name, hp))

    mons.close()

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

    #do a battle using !battle [p1name] [p2name]
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
        except Exception as e:
            await client.send_message(message.channel, "Something went wrong, {}".format(e))
            return

        print("battle over")

    #add a mon using !add [name] [hp], still needs more type checks and stuff
    if message.content.startswith("!add"):
        args = message.content.lower().split()
        name = args[1]
        hp = args[2]
        
        try:
            addMon(name, hp)

        except IndexError: #wrong amount of arguments
            await client.send_message(message.channel, "Use it like this you bruh moment:\n!add [name] [hp]\n(also dont put spaces in the name)")
            return

        except ValueError: #hp isnt an int
            await client.send_message(message.channel, "The hp has to be a number you bruh moment, use it like this:\n!add [name] [hp]")
            return

        await client.send_message(message.channel, "Added {} with {} health".format(name, hp))

    if message.content == "!pokehelp":
        await client.send_message(message.channel, "Battles: !battle [p1name] [p2name] \nAdd a new player: !add [name] [hp]")

client.run(token)