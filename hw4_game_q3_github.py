#name: Roshan Ram
#created: 9/20/19
class Room(object):
    # from simple-text-adventure-game.py (with slight edits)
    def __init__(self, name):
        self.name = name
        self.exits = [None] * 2 # up, down
        self.items = []

    def getDirection(self, dirName):
        # from simple-text-adventure-game.py (with slight edits)
        dirName = dirName.lower()
        if (dirName in ['u', 'up']): return 0
        elif (dirName in ['d', 'down']): return 1
        else:
            print(f'Sorry, I do not recognize the direction {dirName}')
            return None

    def setExit(self, dirName, room):
        # from simple-text-adventure-game.py (with slight edits)
        direction = self.getDirection(dirName)
        self.exits[direction] = room

    def getExit(self, dirName):
        # from simple-text-adventure-game.py 
        direction = self.getDirection(dirName)
        if (direction == None):
            return None
        else:
            return self.exits[direction]

    def getAvailableDirNames(self):
        # from simple-text-adventure-game.py (with slight edits)
        availableDirections = [ ]
        for dirName in ['Up', 'Down']:
            if (self.getExit(dirName) != None):
                availableDirections.append(dirName)
        if (availableDirections == [ ]):
            return 'None'
        else:
            return ', '.join(availableDirections)

class Item(object):
    # from simple-text-adventure-game.py 
    def __init__(self, name, shortName):
        self.name = name
        self.shortName = shortName

class Game(object):
    # from simple-text-adventure-game.py 
    def __init__(self, name, goal, startingRoom, startingInventory):
        self.name = name
        self.goal = goal
        self.room = startingRoom
        self.commandCounter = 0
        self.inventory = startingInventory
        self.gameOver = False

    def getCommand(self):
        # from simple-text-adventure-game.py 
        self.commandCounter += 1
        response = input(f'[{self.commandCounter}] Your command --> ')
        print()
        if (response == ''): response = 'help'
        responseParts = response.split(' ')
        command = responseParts[0]
        target = '' if (len(responseParts) == 1) else responseParts[1]
        return command, target

    def play(self):
        # from simple-text-adventure-game.py (with slight edits)
        print(f'Welcome to {self.name}!')
        print(f'Your goal: {self.goal}!')
        print('Just press enter for help.')
        while (not self.gameOver):
            self.doLook()
            command, target = self.getCommand()
            if (command == 'help'): self.doHelp()
            elif (command == 'superhelp'): self.doSuperhelp()
            elif (command == 'look'): self.doLook()
            elif (command == 'go'): self.doGo(target)
            elif (command == 'get'): self.doGet(target)
            elif (command == 'put'): self.doPut(target)
            elif (command == 'do'): self.doDo(target)
            elif (command == 'sharpen'): self.doSharpen(target)
            elif (command == 'give'): self.doGive(target) #added 1:27 PM
            elif (command == 'quit'): break
            else: print(f'Unknown command: {command}. Enter "help" for help.')
        print('\nGoodbye!')

    def doHelp(self):
        print('''
Welcome to the KosDragon game!  Here are some commands I, KosDragon, know:
    help (print this message)
    look (see what's around you)
-----------------
    go up (or just 'go u'), go down
    get thing
    put thing
-----------------
    do thing
    sharpen thing 
    give thing
    quit
Have fun!''')

    def doSuperhelp(self):
        print('''
go up #(112land)
get problem 
go down #(sky)
get pencil #(blunt/unsharpened)
go down #(ground)
sharpen pencil #(specific to ground)
do problem #(specific to ground)
go down #(underworld)
give problem #(to dragon friend :) )

#and you win :)
''')

    def printItems(self, items):
        # from simple-text-adventure-game.py 
        if (len(items) == 0):
            print('Nothing.')
        else:
            itemNames = [item.name for item in items]
            print(', '.join(itemNames))

    def findItem(self, targetItemName, itemList):
        # from simple-text-adventure-game.py 
        for item in itemList:
            if (item.shortName == targetItemName):
                return item
        return None

    def doLook(self): 
        #from simple-text-adventure-game.py (with slight edits)
        print(f'\nI am in {self.room.name}')
        print(f'I can go these directions: {self.room.getAvailableDirNames()}')
        print('I can see these things: ', end='')
        self.printItems(self.room.items)
        print('These things are in my KosCoat: ', end='')
        self.printItems(self.inventory)
        print()

    def doGo(self, dirName):
        # from simple-text-adventure-game.py 
        newRoom = self.room.getExit(dirName)
        if (newRoom == None):
            print(f'Sorry, I cannot go in that direction.')
        else:
            self.room = newRoom

    def doGet(self, itemName): 
        # from simple-text-adventure-game.py (with slight edits)
        item = self.findItem(itemName, self.room.items)
        if (item == None):
            print('Sorry, but I do not see that here.')
        elif (len(self.inventory) == 5): #changed 2 to 5
            print('Sorry, I cannot carry more (maybe put something down)')
        else:
            self.room.items.remove(item)
            self.inventory.append(item)

    def doPut(self, itemName):
         # from simple-text-adventure-game.py
        item = self.findItem(itemName, self.inventory)
        if (item == None):
            print('Sorry, but I do not seem to be carrying that!')
        else:
            self.inventory.remove(item)
            self.room.items.append(item)

    def doDo(self, itemName): 
        #issue: unable to unlink unsharpened pencil and problem 
        #still being able to be done #resolved 1:46 PM
        pencil = self.findItem('pencil', self.inventory)
        problem = self.findItem('problem', self.inventory)
        if (itemName != 'problem'):
            print('I do not know how to do that! Maybe I need to study harder...')
        elif (problem == None):
            print('I do not have anything to do! I wish I had more work for '
            + 'the first time ever.')
        elif (pencil == None):
            print('I do not have a pencil... :/')
        elif ('sharpened' not in pencil.name):
            print('How did you expect to do the problem with an unsharpened pencil'
            + ' --with the eraser?')
        elif ('finished' in problem.name):
            print('The problem is already finished!')
        elif ('sky' in self.room.name.lower()):
            print('How are you supposed to get any work done while flying??')
        else:
            problem.name = 'A finished problem!'

    def doSharpen(self, itemName):
        pencil = self.findItem('pencil', self.inventory)
        problem = self.findItem('problem', self.inventory)
        if (itemName != 'pencil'):
            print("That sure doesn't sound like fun.")
        elif (pencil == None):
            print('There are no pencils in the KosCoat! Silly freshman.')
        elif (problem == None):
            print("You can't sharpen the pencil unless you have a reason the sharpen it :)")
        elif ('ground' not in self.room.name.lower()):
            print("Didn't your mother teach you not to sharpen pencils in " 
            + self.room.name + "???")
        else:
            pencil.name = 'A nice sharpened pencil.'


    def doGive(self, itemName): #left off here 1:40 AM 9/21
        pencil = self.findItem('pencil', self.inventory)
        problem = self.findItem('problem', self.inventory)
        if (itemName != 'problem'):
            ("I have a hunch my friends might not like that.")
        elif (problem == None):
            print('I am not carrying a problem!')
        elif ('finished' not in problem.name):
            print('You cruel being...why would you want to give '
            + 'an unfinished problem to another dragon.')
        elif ('underworld' not in self.room.name.lower()):
            print("There are no other FellowDragons to give problems to here :(")
        else:
            print('You did it!!!!  You finished the HARD code tracing problem'
            + ' and handed it over to your dragon friend to be checked!')
            self.gameOver = True


def playSimpleGame():
    # Make the Rooms
    ground = Room('The Ground')
    the112land = Room('The The112land')
    sky = Room('The Sky')
    underworld = Room('The Underworld')

    # Make the map (note: it need not be physically possible)
    ground.setExit('Up', sky)
    ground.setExit('Down', underworld)
    sky.setExit('Down', ground)
    sky.setExit('Up', the112land)
    the112land.setExit('Down', sky)
    underworld.setExit('Up', ground)


    # Make some items
    writing = Item('a lovely 112 code tracing problem', 'problem')
    the112land.items.append(writing)
    fellowDragon = Item('a fellow dragon friend', 'friend')
    underworld.items.append(fellowDragon)
    pencil = Item('a blunt pencil (needs sharpening) ', 'pencil')
    sky.items.append(pencil)


    # Make the game and play it
    game = Game('This KosDragon Game',
                'Finish your 112 code tracing problem and hand it over '
                + 'to a FellowDragon to be checked. Simple enough, right?',
                sky,
                [ ])
    game.play()

playSimpleGame()
