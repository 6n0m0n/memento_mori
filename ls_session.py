#by 6n0m0n, SpaceSheep, and malachite_sprite
from ls_square import LS_square
from ls_character import LS_character
from ls_minion import LS_minion
import copy as copy
import os
import math
from random import randrange

class LS_session: #loads up a save's various files, contains game info, talks to gui about display, organizes updates

    def __init__(self, folderloc):

        self.map_arr = []
        self.movetry_arr = []
        self.ch_arr = []
        self.lb_arr = []
        self.animations = []
        self.submitted_ch = []
        self.folderloc = folderloc
        
        self.fullmapfile = open(os.path.join(folderloc, "region.txt"), "r+").readlines()

        self.chfile = open(os.path.join(folderloc, "ch.txt"), "r+").readlines()

        self.makemap()
        self.initialize_chs()

    def update(self):

        for i in self.ch_arr:
            i.update()

    def get_square(self, coord):
        return self.map_arr[coord[0]][coord[1]][coord[2]]

    def add_lowbehavior(self, lowbehavior):

        if not(lowbehavior.character in self.submitted_ch):
            self.lb_arr.append(lowbehavior)
        
        self.submitted_ch.append(lowbehavior.character)

        try:
            assert(self.lb_arr[-1] is lowbehavior)
        except AssertionError:
            print(lowbehavior)
        
        if len(self.lb_arr) == len(self.ch_arr):
            self.try_lb_updates()
            #print("Trying updates")


    def try_lb_updates(self):
        self.success_dict = {}
        self.already_there = []
        movetry_arr = copy.deepcopy(self.movetry_arr)
        movefrom_arr = copy.deepcopy(self.movetry_arr)
        staying_arr = copy.deepcopy(self.movetry_arr)
        orient_dict = {"N": [0,-1,0], "S": [0,1,0], "E": [0,0,1], "W":[0,0,-1]}

        for w in self.lb_arr:
            self.already_there.append(w.character.position) #lists in the same order where the characters already are

        for v in range(len(self.lb_arr)):
            self.success_dict[v] = "unknown"

        for i in range(len(self.already_there)):

            if self.lb_arr[i].subtype == "move":
                movefrom_arr[self.already_there[i][0]][self.already_there[i][1]][self.already_there[i][2]] = i

            else:
                staying_arr[self.already_there[i][0]][self.already_there[i][1]][self.already_there[i][2]] = i

        for i in range(len(self.lb_arr)):
            
            if self.lb_arr[i].subtype == "move": #check move commands
                movetry_arr[self.lb_arr[i].move_loc[0]][self.lb_arr[i].move_loc[1]][self.lb_arr[i].move_loc[2]].append(i)

        for i in range(len(movetry_arr)):
            for j in range(len(movetry_arr[i])):
                for k in range(len(movetry_arr[i][j])):

                    if (staying_arr[i][j][k] != []) or self.map_arr[i][j][k].pathblocker: #i.e. someone is staying put here OR if the square is a pathblocker
                        for w in movetry_arr[i][j][k]: #w is not an index here
                            self.success_dict[w] = "failure" #can't move where someone is standing still

                    if len(self.movetry_arr[i][j][k]) > 1:
                        winner_index = randrange(len(self.movetry_arr[i][j][k]))
                        
                        for p in range(len(movetry_arr[i][j][k])):

                            if p == winner_index and self.success_dict[self.movetry_arr[i][j][k][p]] != "failure": #could have failed in the staying check
                                self.success_dict[movetry_arr[i][j][k][p]] = "no_move_conflict" #does not totally determine if you can move; need to check dependencies

                            else:
                                self.success_dict[movetry_arr[i][j][k][p]] = "failure" #means you will not move
                    
                    if len(movetry_arr[i][j][k]) == 1:
                        if self.success_dict[movetry_arr[i][j][k][0]] != "failure":
                            self.success_dict[movetry_arr[i][j][k][0]] = "no_move_conflict"

                    if movefrom_arr[i][j][k] != []: #i.e. someone is standing where you're trying to go, but they want to move too

                        for w in movetry_arr[i][j][k]:
                            self.success_dict[w] = movefrom_arr[i][j][k] #can only ever contain one anyway; index indicates a character as per its command index in the lb_arr

                            
        for e in range(2*len(self.success_dict)): #just making sure thing propogate fully 
            for g in self.success_dict:

                if type(self.success_dict[g]) is int:
                    self.success_dict[g] = self.success_dict[self.success_dict[g]]
        for t in self.success_dict:

            if type(self.success_dict[t]) is int:
                self.success_dict[t] = "success"

            if self.success_dict[t] == "no_move_conflict":
                self.success_dict[t] = "success"

        for q in range(len(self.lb_arr)):

            if self.lb_arr[q].subtype == "move":
                setattr(self.lb_arr[q], "status", self.success_dict[q])
  
        for b in range(len(self.lb_arr)):
            if self.lb_arr[b].subtype == "attack":
                temp = []
                for i in range (1,2):
                    for r in range (0,3):
                        if i == 1:
                            orient = orient_dict[self.lb_arr[b].get_character().orientation]
                            temp.append(self.lb_arr[b].get_character().position[r]+orient[r])
                        elif i == 2:
                            temp[r] = temp[r]+orient[r]
                    #print (temp)
                    if self.get_square(temp).contained_ch != None:
                        self.get_square(temp).contained_ch.receive_damage()
                        #print ("update sent")

                self.lb_arr[b].status = "finished"

        for b in range(len(self.lb_arr)): #this is a comment
            if self.lb_arr[b].subtype == "bribe":
                temp = []
                for r in range (0,3):
                    orient = orient_dict[self.lb_arr[b].character.orientation]
                    temp.append(self.lb_arr[b].get_character().position[r]+orient[r])
                if self.get_square(temp).contained_ch != None and self.lb_arr[b].character.money >= 20:
                    if self.get_square(temp).contained_ch.subtype != "target":
                        print (self.get_square(temp).contained_ch.position)
                        self.get_square(temp).contained_ch.roots.append(LS_minion(self, self.get_square(temp).contained_ch))
                        print ("Bribe successful")

                self.lb_arr[b].status = "finished"

        for m in range(len(self.lb_arr)):   
            self.lb_arr[m].update_character()

                
        self.lb_arr = []
        self.submitted_ch = []

    def initialize_chs(self):

        for i in range(len(self.chfile)):
            chindex = i
            ch_info_list = self.chfile[i].split(";")
            #print (i,ch_info_list)
            character = LS_character(self, chindex, ch_info_list)
            self.ch_arr.append(character)
        #print (self.ch_arr)

    def makemap(self):

        ylength = int(self.fullmapfile[0]) #the y length of a z-level
        
        self.fullmapfile.pop(0)
        
        edgesymb = self.fullmapfile[0][0]
        self.fullmapfile.pop(0)

        self.mapfile = self.fullmapfile
        
        for j in range(len(self.mapfile)):
            for i in range((len(self.mapfile[0])-1)): #len(mapfile[0])-1

                xcoord = i
                ycoord = j % ylength
                zcoord = int(math.floor(j / ylength))

                square = LS_square(self.mapfile, ylength, xcoord, ycoord, zcoord, edgesymb)
                    
                if xcoord == 0: #beginning of an x-line

                    if ycoord == 0: #beginning of a z-level
                        new_zlist = []
                        self.map_arr.append(new_zlist)

                    new_ylist = []
                    self.map_arr[zcoord].append(new_ylist)


                self.map_arr[zcoord][ycoord].append(square)
                
                if xcoord == 0:

                    if ycoord == 0:
                        new_zlist = []
                        self.movetry_arr.append(new_zlist)

                    new_ylist = []
                    self.movetry_arr[zcoord].append(new_ylist)

                self.movetry_arr[zcoord][ycoord].append([])

                    
            
