class Thing:
    '''Fields: id (Nat),
               name (Str),
               description (Str)
    '''
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        
    def __repr__(self):
        return '<thing #{0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        
class Player:
    '''Fields: id (Nat),
               name (Str), 
               description (Str),
               location (Room),
               inventory ((listof Thing))
    '''
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        self.location = None
        self.inventory = []
        
    def __repr__(self):
        return '<player #{0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        if len(self.inventory) != 0:
            print('Carrying: {0}.'.format(
                ', '.join(map(lambda x: x.name,self.inventory))))
 
class Room:
    '''Fields: id (Nat),
               name (Str), 
               description (Str),
               contents ((listof Thing)),
               exits ((listof Exit))
    '''    
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        self.contents = []
        self.exits = []
        
    def __repr__(self):
        return '<room {0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        if len(self.contents) != 0:
            print('Contents: {0}.'.format(
                ', '.join(map(lambda x: x.name, self.contents))))
        if len(self.exits) != 0:
            print('Exits: {0}.'.format(
                ', '.join(map(lambda x: x.name, self.exits)))) 
 
class Exit:
    '''Fields: name (Str), 
               destination (Room),
               key (Thing),
               message (Str)
    '''       
    
    def __init__(self,name,dest):
        self.name = name
        self.destination = dest
        self.key = None
        self.message = ''
        
    def __repr__(self):
        return '<exit {0}>'.format(self.name)

class World:
    '''Fields: rooms ((listof Room)), 
               player (Player)
    '''       
    
    msg_look_fail = "You don't see that here."
    msg_no_inventory = "You aren't carrying anything."
    msg_take_succ = "Taken."
    msg_take_fail = "You can't take that."
    msg_drop_succ = "Dropped."
    msg_drop_fail = "You aren't carrying that."
    msg_go_fail = "You can't go that way."
    
    msg_quit = "Goodbye."
    msg_verb_fail = "I don't understand that."
    
    def __init__(self, rooms, player):
        self.rooms = rooms
        self.player = player

    def look(self, noun):
        '''
        prints the noun and the description of the noun the player is trying to 
        look at based self
        
        Effects: noun and the description of noun is printed
        
        look: World Str -> None
        '''
        if noun == "me":
            self.player.look()
            return None
        elif noun == "here":
            self.player.location.look()
            return None
        for thing in self.player.inventory:
            if noun == thing.name:
                thing.look()
                return None
        for thing in self.player.location.contents:
            if noun == thing.name:
                thing.look()
                return None
        print(self.msg_look_fail)
                
    def inventory(self):
        '''
        prints the discription of the inventory in self
        
        Effects: a discription of the inventory is printed
        
        inventory: World -> None
        '''
        if self.player.inventory == []:
            print(self.msg_no_inventory)
        else:
            inventory_string = 'Inventory: '
            for thing in self.player.inventory:
                inventory_string = inventory_string + thing.name + ", "
            print(inventory_string[:-2])
            
    def take(self, noun):
        '''
        mutates self to add the noun to the inventory and remove it from the 
        location if the object can be taken and prints if the object is taken
        
        Effects: self is mutated
                 prints whether if the object is taken
        take: World Str -> None
        '''
        for thing in self.player.location.contents:
            if thing.name == noun:
                self.player.location.contents.remove(thing)
                self.player.inventory.append(thing)
                print(self.msg_take_succ)
                return None
        print (self.msg_take_fail)
                    
    def drop(self, noun):
        '''
        mutates self to remove the noun from inventory and add it to the self
        location if the object can be dropped and prints if the object is 
        dropped
        
        Effects: self is mutated
                 prints whether if the object is dropped
        
        drop: World Str -> None
        '''
        for thing in self.player.inventory:
            if thing.name == noun:
                self.player.location.contents.append(thing)
                self.player.inventory.remove(thing)
                print(self.msg_drop_succ)
                return None
        print(self.msg_drop_fail)
        
    def go(self, noun):
        '''
        mutates self to the new location if the player can reach the new 
        location named noun and prints if the player can reach noun 
        
        Effects: self is mutated
                 prints if the player has reached the new location 
        
        go: World Str -> None
        '''
        for exit in self.player.location.exits:
            if noun == exit.name:
                if exit.key == None:
                    self.player.location = exit.destination
                    self.player.location.look()
                else:
                    if exit.key in self.player.inventory:
                        self.player.location = exit.destination
                        self.player.location.look()
                    else:
                        print(exit.message)
                return None
            
        print(self.msg_go_fail)
        
        
    def play(self):
        player = self.player
        
        player.location.look()
        
        while True:
            line = input( "- " )
            
            wds = line.split()
            verb = wds[0]
            noun = ' '.join( wds[1:] )
            
            if verb == 'quit':
                print( self.msg_quit )
                return
            elif verb == 'look':
                if len(noun) > 0:
                    self.look(noun)  
                else:
                    self.look('here')
            elif verb == 'inventory':
                self.inventory()     
            elif verb == 'take':
                self.take(noun)    
            elif verb == 'drop':
                self.drop(noun)
            elif verb == 'go':
                self.go(noun)   
            else:
                print( self.msg_verb_fail )

    ## Q3
    def save(self, fname):
        '''
        Consumes a world and a string argument giving the name of the file,
        opens the file named fname, writes self using a text format in fname
        
        Effects: Writes to a file called fname
        
        save: World Str -> None
        '''
        f = open(fname,"w")
        rooms = self.rooms
        for room in rooms:
            things = room.contents
            for thing in things:
                f.write("thing #{0} {1}\n".format(thing.id, thing.name))
                f.write(thing.description + "\n")
        inventory = self.player.inventory
        for thing in inventory:
            f.write("thing #{0} {1}\n".format(thing.id, thing.name))
            f.write(thing.description + "\n")
        for room in rooms:
            f.write("room #{0} {1}\n".format(room.id,room.name))
            f.write(room.description + "\n")
            contents = ''
            for content in room.contents:
                contents = contents + "#" + str(content.id) + ' '
            f.write("contents " + contents + "\n")
        player = self.player
        f.write("player #{0} {1}\n".format(player.id, player.name))
        f.write(player.description + "\n")
        items = ''
        for item in player.inventory:
            items = items + "#" + str(item.id) + ' '
        f.write("inventory "+ items + "\n")
        f.write("location " + "#" + str(player.location.id) + "\n")
        for room in rooms:
            exits = room.exits
            for exit in exits:
                nm = exit.name
                dest = str(exit.destination.id)
                if exit.key == None:
                    f.write("exit "+"#"+str(room.id)+' #'+ dest +' '+ nm +"\n")
                else:
                    f.write("keyexit "+"#"+str(room.id)+' #'+ dest+' '+nm +"\n")
                    f.write("#" + str(exit.key.id) + ' '+ exit.message + "\n")
        f.close()
    
            
    

            
        

## Q2
def load( fname ):
    '''
    Consumes a string giving the name of the file, opens the file fname, reads
    each line, and returns a world created from the lines in fname

    Effect: Reads the file named fname
    
    load: Str -> World
    '''
    f = open(fname,"r")
    line = f.readline()
    rooms = []
    things = []
    while line != "":
        obj = line.split() 
        if obj[0] == "room":
            room = Room(int(obj[1][1:]))
            room.name = " ".join(obj[2:])
            room.description = f.readline()[:-1]
            contents = f.readline().split()[1:]
            contents = list(map(lambda x: int(x[1:]), contents))
            objects = []
            for thing in things:
                if thing.id in contents:
                    objects.append(thing)
            room.contents = objects
            room.exits = []
            rooms.append(room)
        elif obj[0] == "player":
            player = Player(int(obj[1][1:]))
            player.name = " ".join(obj[2:])
            player.description = f.readline()[:-1]
            inventory = f.readline().split()[1:]
            inventory = list(map(lambda x: int(x[1:]), inventory))
            objects = []
            for thing in things:
                if thing.id in inventory:
                    objects.append(thing)
            player.inventory = objects
            location = int(f.readline().split()[1][1:])
            for room in rooms:
                if room.id == location:
                    player.location = room
        elif obj[0] == "thing":
            thing = Thing(int(obj[1][1:]))
            thing.name = " ".join(obj[2:])
            thing.description = f.readline()[:-1]
            things.append(thing)
        elif obj[0] == "exit":
            for room in rooms:
                if room.id == int(obj[1][1:]):
                    for room_exit in rooms:
                        if room_exit.id == int(obj[2][1:]):
                            exit_rm = room_exit
                    room.exits.append(Exit(" ".join(obj[3:]), exit_rm))
        elif obj[0] == "keyexit":
            for room in rooms:
                if room.id == int(obj[1][1:]):
                    for room_exit in rooms:
                        if room_exit.id == int(obj[2][1:]):
                            room.exits.append(Exit(" ".join(obj[3:]),room_exit))
                    key_info = f.readline()
                    key_info = key_info.split()
                    room.exits[-1].message = ' '.join(key_info[1:])
                    for thing in things:
                        if thing.id == int(key_info[0][1:]):
                            room.exits[-1].key = thing
        line = f.readline()
    f.close()
    return World(rooms, player)

        
            
               
def makeTestWorld(usekey):
    wallet = Thing(1)
    wallet.name = 'wallet'
    wallet.description = 'A black leather wallet containing a WatCard.'
    
    keys = Thing(2)
    keys.name = 'keys'
    keys.description = 'A metal keyring holding a number of office and home keys.'
    
    phone = Thing(3)
    phone.name = 'phone'
    phone.description = 'A late-model smartphone in a Hello Kitty protective case.'
    
    coffee = Thing(4)
    coffee.name = 'cup of coffee'
    coffee.description = 'A steaming cup of black coffee.'
    
    hallway = Room(5)
    hallway.name = 'Hallway'
    hallway.description = 'You are in the hallway of a university building. \
Students are coming and going every which way.'
    
    c_and_d = Room(6)
    c_and_d.name = 'Coffee Shop'
    c_and_d.description = 'You are in the student-run coffee shop. Your mouth \
waters as you scan the room, seeing many fine foodstuffs available for purchase.'
    
    classroom = Room(7)
    classroom.name = 'Classroom'
    classroom.description = 'You are in a nondescript university classroom. \
Students sit in rows at tables, pointedly ignoring the professor, who\'s \
shouting and waving his arms about at the front of the room.'
    
    player = Player(8)
    player.name = 'Stu Dent'
    player.description = 'Stu Dent is an undergraduate Math student at the \
University of Waterloo, who is excelling at this studies despite the fact that \
his name is a terrible pun.'
    
    c_and_d.contents.append(coffee)
    player.inventory.extend([wallet,keys,phone])
    player.location = hallway
    
    hallway.exits.append(Exit('shop', c_and_d))
    ex = Exit('west', classroom)
    if usekey:
        ex.key = coffee
        ex.message = 'On second thought, it might be better to grab a \
cup of coffee before heading to class.'
    hallway.exits.append(ex)
    c_and_d.exits.append(Exit('hall', hallway))
    classroom.exits.append(Exit('hall', hallway))
    
    return World([hallway,c_and_d,classroom], player)

testworld = makeTestWorld(False)
testworld_key = makeTestWorld(True)
