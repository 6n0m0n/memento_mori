#by 6n0m0n, SpaceSheep, and malachite_sprite
from ls_square import LS_square
from ls_session import LS_session
from ls_move import LS_move
from ls_attack import LS_attack
from ls_randomwalk import LS_randomwalk
from ls_character import LS_character
from ls_rotate import LS_rotate
from tkinter import *
from PIL import *
from PIL import ImageTk
import PIL.Image
import os
import math
import tkinter as tk
import pickle as pickle
import copy as copy
#creates a root with widgets and dialoge to start session

class Memento_Mori(Frame):
    
    def __init__(self):
        self.root = tk.Tk()

        self.resolution = [1280, 720]
        self.z_level = 0
        self.view_rot = 0 #adding 1 to rot represents a clockwise rotation
        tk.Frame.__init__(self, self.root)
        
        self.root.configure(background = "black")
        self.root.wm_title("Memento Mori")
        self.make_widgets()
        self.open_images()

    def start(self):
        self.root.bind_all('<Key>', self.keypress)
        self.root.mainloop()

    def keypress(self, event):
        #print("You pressed "+event.char)
        if event.char in "wasd":
            wasd_dict = {"w": [0,-1,0], "a": [0,0,-1], "s": [0,1,0], "d": [0,0,1]}
            perm_order = "wasdwas"
            
            curr_pos = self.session.player.position
            
            wasd_perm = wasd_dict[perm_order[perm_order.index(event.char)+self.view_rot]]
            
            move_loc = [curr_pos[0], curr_pos[1]+wasd_perm[1], curr_pos[2]+wasd_perm[2]]
            self.session.player.roots.append(LS_move(self.session, self.session.player, move_loc))
            self.session.update()
            self.redrawmap()

        if event.char in "okl;":
            okl_dict = {"o": "N", "k": "W", "l": "S", ";": "E"}
            perm_order = "okl;okl"
            
            okl_perm = okl_dict[perm_order[perm_order.index(event.char)+self.view_rot]]
            
            self.session.player.roots.append(LS_rotate(self.session, self.session.player, okl_perm))
            self.session.update()
            self.redrawmap()

        if event.char == "u": #force update
            self.session.update()
            self.redrawmap()

        if event.char == "y": #do random walk yo
            self.session.player.roots.append(LS_randomwalk(self.session, self.session.player))
            self.session.update()
            self.redrawmap()

        if event.char == "e":
            print("e pushed!")
            self.session.player.roots.append(LS_attack(self.session, self.session.player))
            print("roots!")
            self.session.update()
            print("update!")
            self.redrawmap()

    def openfolder(self):
        folderloc = tk.filedialog.askdirectory()
        self.session = LS_session(folderloc)
        self.drawwalls()
        self.redrawmap()

    def opensession(self):
        pickleloc = tk.filedialog.askopenfilename()
        self.session = pickle.load(open(pickleloc, "rb"))
        self.drawwalls()
        self.redrawmap()
        print("LS_session opened from pickle")

    def savesession(self):
        folderloc = tk.filedialog.askdirectory()
        pickleloc = os.path.join(folderloc, "session.p")
        pickle.dump(self.session, open(pickleloc, "wb"))
        print("LS_session saved to pickle")

    def click(self, event):
        self.clickx = event.x
        self.clicky = event.y

    def clickdrag(self, event):
        self.x_canoff = self.x_canoff + int((event.x - self.clickx)/2)
        self.y_canoff = self.y_canoff + int((event.y - self.clicky)/2)
        self.maincan.tk.call(self.maincan._w, 'scan', 'dragto', self.x_canoff, self.y_canoff, 1)
        self.clickx = event.x
        self.clicky = event.y

    def doubleclick(self, event):
        self.view_rot = (self.view_rot+1)%4
        self.drawwalls()
        self.redrawmap()

    def make_widgets(self):
        
        #menu bar
        menubar = Menu(self.root)
        self.root["menu"] = menubar

        self.x_canoff = 0
        self.y_canoff = 0
        
        filemenu = Menu(menubar)
        optionmenu = Menu(menubar)
        
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Options", menu=optionmenu)

        filemenu.add_command(label="Open from folder", command=self.openfolder)
        filemenu.add_command(label="Open old session", command=self.opensession)
        filemenu.add_command(label="Save current session", command=self.savesession)
        optionmenu.add_command(label="Nothing")

        #main canvas
        self.maincan = tk.Canvas(master=self.root)

        self.maincan.titlecardpil = PIL.Image.open("titlecard.png")
        self.maincan.titlecard = ImageTk.PhotoImage(self.maincan.titlecardpil)
        self.maincan.config(width = self.resolution[0]-5, height = self.resolution[1]-10, background = "black")
        
        title = self.maincan.create_image(0,0,image=self.maincan.titlecard, anchor="nw")

        self.maincan.grid(row="0")
        self.maincan.bind("<Button-1>", self.click)
        self.maincan.bind("<B1-Motion>", self.clickdrag)
        self.maincan.bind("<Double-Button-1>", self.doubleclick)
        
    def drawwalls(self):

        animdex = 0
        anim_pause = 20

        symb_to_folder = {"B":"grey_wall_0", "X":"default_wall"}

        off_width = 114/2
        off_height = 80/2

        e_1 = [off_height, off_width]
        e_2 = [off_height, -off_width] #basis vectors : [y,x]

        map_arr = self.session.map_arr

        x_dim = len(map_arr[0][0])
        y_dim = len(map_arr[0])
        z_dim = len(map_arr)

        backdrop = PIL.Image.new("RGB", (int(off_width*(x_dim + y_dim+4)), int(off_height*(x_dim + y_dim+4))), "black")

        l = self.z_level #TODO make it iterate over zs

        self.image_list = []

        direction_permute = ["NS", "EW", "NS", "EW", "NS", "NE", "ES", "SW", "NW", "NE", "ES", "SW", "NES", "ESW", "NSW", "NEW", "NES", "ESW", "NSW", "N", "E", "S", "W", "N", "E", "S"]

        ordering_list = [[range(y_dim), range(x_dim)],[range(y_dim-1,-1,-1), range(x_dim)],[range(y_dim-1,-1,-1), range(x_dim-1,-1,-1)],[range(y_dim), range(x_dim-1,-1,-1)]]

        y_order = ordering_list[self.view_rot][0]
        x_order = ordering_list[self.view_rot][1]

        for i in y_order:
            for j in x_order:
                cur_ssquare = map_arr[l][i][j]

                if self.view_rot == 0:
                    rel_y = i*off_height + j*off_height
                    rel_x = j*off_width - i*off_width + off_width*(y_dim + 1)

                if self.view_rot == 1:
                    rel_y = (y_dim-i)*off_height + j*off_height
                    rel_x = -j*off_width + (y_dim-i)*off_width + off_width*(x_dim + 1)

                if self.view_rot == 2:
                    rel_y = (y_dim-i)*off_height + (x_dim-j)*off_height
                    rel_x = (x_dim-j)*off_width - (y_dim-i)*off_width + off_width*(y_dim + 1)

                if self.view_rot == 3:
                    rel_y = i*off_height + (x_dim-j)*off_height
                    rel_x = -(x_dim-j)*off_width + i*off_width + off_width*(x_dim + 1)
                
                if cur_ssquare.type == "wall":
                    trueorientation = cur_ssquare.wallorientation

                    if trueorientation != "":

                        if trueorientation == "NESW":
                            filename = "NESW.png"

                        else:

                            wall_index = direction_permute.index(trueorientation) + self.view_rot
                            filename = direction_permute[wall_index] + ".png" #reassigns filename according to rotation

                    else:
                        filename = "pillar.png"

                    folder = symb_to_folder[cur_ssquare.symb]

                    imgpath = os.path.join(folder, filename)
                    image = PIL.Image.open(imgpath)
                    
                    self.image_list.append(image)
                    
                    backdrop.paste(image, (int(rel_x), int(rel_y)), image)#draw onto file
                    
        self.wallspic = backdrop

    def open_images(self):

        self.grey_wall_tops_dict = {"pillar":PIL.Image.open(os.path.join("grey_wall_0_tops", "pillar.png")), "ES":PIL.Image.open(os.path.join("grey_wall_0_tops", "ES.png")),"ESW":PIL.Image.open(os.path.join("grey_wall_0_tops", "ESW.png")),"EW":PIL.Image.open(os.path.join("grey_wall_0_tops", "EW.png")),"NE":PIL.Image.open(os.path.join("grey_wall_0_tops", "NE.png")),"NES":PIL.Image.open(os.path.join("grey_wall_0_tops", "NES.png")),"NESW":PIL.Image.open(os.path.join("grey_wall_0_tops", "NESW.png")),"NEW":PIL.Image.open(os.path.join("grey_wall_0_tops", "NEW.png")),"NS":PIL.Image.open(os.path.join("grey_wall_0_tops", "NS.png")),"NSW":PIL.Image.open(os.path.join("grey_wall_0_tops", "NSW.png")),"NW":PIL.Image.open(os.path.join("grey_wall_0_tops", "NW.png")),"SW":PIL.Image.open(os.path.join("grey_wall_0_tops", "SW.png")),}
        self.default_ch_dict = {"E":PIL.Image.open(os.path.join("default_ch_walt", "E.png")),"E_alt":PIL.Image.open(os.path.join("default_ch_walt", "E_alt.png")),"N":PIL.Image.open(os.path.join("default_ch_walt", "N.png")),"N_alt":PIL.Image.open(os.path.join("default_ch_walt", "N_alt.png")),"S":PIL.Image.open(os.path.join("default_ch_walt", "S.png")),"S_alt":PIL.Image.open(os.path.join("default_ch_walt", "S_alt.png")),"W":PIL.Image.open(os.path.join("default_ch_walt", "W.png")),"W_alt":PIL.Image.open(os.path.join("default_ch_walt", "W_alt.png"))}
        self.player_ch_dict = {"E":PIL.Image.open(os.path.join("player_ch_walt", "E.png")),"E_alt":PIL.Image.open(os.path.join("player_ch_walt", "E_alt.png")),"N":PIL.Image.open(os.path.join("player_ch_walt", "N.png")),"N_alt":PIL.Image.open(os.path.join("player_ch_walt", "N_alt.png")),"S":PIL.Image.open(os.path.join("player_ch_walt", "S.png")),"S_alt":PIL.Image.open(os.path.join("player_ch_walt", "S_alt.png")),"W":PIL.Image.open(os.path.join("player_ch_walt", "W.png")),"W_alt":PIL.Image.open(os.path.join("player_ch_walt", "W_alt.png"))}
        try:
            self.zombie_ch_dict = {"E":PIL.Image.open(os.path.join("zombie_ch_walt", "E.png")),"E_alt":PIL.Image.open(os.path.join("zombie_ch_walt", "E_alt.png")),"N":PIL.Image.open(os.path.join("zombie_ch_walt", "N.png")),"N_alt":PIL.Image.open(os.path.join("zombie_ch_walt", "N_alt.png")),"S":PIL.Image.open(os.path.join("zombie_ch_walt", "S.png")),"S_alt":PIL.Image.open(os.path.join("zombie_ch_walt", "S_alt.png")),"W":PIL.Image.open(os.path.join("zombie_ch_walt", "W.png")),"W_alt":PIL.Image.open(os.path.join("zombie_ch_walt", "W_alt.png"))}
            self.player_ch_dict = {"E":PIL.Image.open(os.path.join("player_ch_walt", "E.png")),"E_alt":PIL.Image.open(os.path.join("player_ch_walt", "E_alt.png")),"N":PIL.Image.open(os.path.join("player_ch_walt", "N.png")),"N_alt":PIL.Image.open(os.path.join("player_ch_walt", "N_alt.png")),"S":PIL.Image.open(os.path.join("player_ch_walt", "S.png")),"S_alt":PIL.Image.open(os.path.join("player_ch_walt", "S_alt.png")),"W":PIL.Image.open(os.path.join("player_ch_walt", "W.png")),"W_alt":PIL.Image.open(os.path.join("player_ch_walt", "W_alt.png"))}
        except Exception as e:
            print("Character sprite fail")
            
    def redrawmap(self):

        self.backdrop = self.wallspic.copy() #copy.deepcopy doesn't work on images :(

        animdex = 0
        anim_pause = 20

        to_update = []

        symb_to_folder = {"B":"grey_wall_0_tops", "X":"default_wall"}

        off_width = 114/2
        off_height = 80/2

        e_1 = [off_height, off_width]
        e_2 = [off_height, -off_width] #basis vectors : [y,x]

        map_arr = self.session.map_arr

        x_dim = len(map_arr[0][0])
        y_dim = len(map_arr[0])
        z_dim = len(map_arr)

        l = self.z_level #TODO make it iterate over zs

        self.image_list = []

        direction_permute = ["NS", "EW", "NS", "EW", "NS", "NE", "ES", "SW", "NW", "NE", "ES", "SW", "NES", "ESW", "NSW", "NEW", "NES", "ESW", "NSW", "N", "E", "S", "W", "N", "E", "S"]

        ordering_list = [[range(y_dim), range(x_dim)],[range(y_dim-1,-1,-1), range(x_dim)],[range(y_dim-1,-1,-1), range(x_dim-1,-1,-1)],[range(y_dim), range(x_dim-1,-1,-1)]]

        y_order = ordering_list[self.view_rot][0]
        x_order = ordering_list[self.view_rot][1]

        for m in range(-1,2):
            for n in range(-1,2):
                for character in self.session.ch_arr:
                    to_update.append([character.position[0], character.position[1]+m, character.position[2]+n])

                for anim in self.session.animations:
                    if anim[0] == "move":
                        to_update.append([anim[2][0], anim[2][1]+m, anim[2][2]+n])

        for i in y_order:
            for j in x_order:
                if [l, i, j] in to_update:
                    cur_ssquare = map_arr[l][i][j]

                    if self.view_rot == 0:
                        rel_y = i*off_height + j*off_height
                        rel_x = j*off_width - i*off_width + off_width*(y_dim + 1)

                    if self.view_rot == 1:
                        rel_y = (y_dim-i)*off_height + j*off_height
                        rel_x = -j*off_width + (y_dim-i)*off_width + off_width*(x_dim + 1)

                    if self.view_rot == 2:
                        rel_y = (y_dim-i)*off_height + (x_dim-j)*off_height
                        rel_x = (x_dim-j)*off_width - (y_dim-i)*off_width + off_width*(y_dim + 1)

                    if self.view_rot == 3:
                        rel_y = i*off_height + (x_dim-j)*off_height
                        rel_x = -(x_dim-j)*off_width + i*off_width + off_width*(x_dim + 1)
                    
                    if cur_ssquare.type == "wall":
                        trueorientation = cur_ssquare.wallorientation

                        if trueorientation != "":

                            if trueorientation == "NESW":
                                filename = "NESW"

                            else:

                                wall_index = direction_permute.index(trueorientation) + self.view_rot
                                filename = direction_permute[wall_index] #reassigns filename according to rotation

                        else:
                            filename = "pillar"

                        image = self.grey_wall_tops_dict[filename].copy()
                        
                        self.image_list.append(image)
                        
                        self.backdrop.paste(image, (int(rel_x), int(rel_y)), image)#draw wall onto file self.map_image.paste(image, (int(rel_x), int(rel_y)), image)

                    if cur_ssquare.contained_ch != None:
                        cur_ch = cur_ssquare.contained_ch
                        ch_sprite_folder = cur_ch.sprite_folder

                        direction_index = direction_permute.index(cur_ch.orientation) + self.view_rot
                        base_filename = direction_permute[direction_index]

                        if ch_sprite_folder == "default_ch_walt":
                            image = self.default_ch_dict[base_filename]
                        elif ch_sprite_folder == "zombie_ch_walt":
                            image = self.zombie_ch_dict[base_filename]
                        elif ch_sprite_folder == "player_ch_walt" and self.player_ch_dict is not None:
                            image = self.player_ch_dict[base_filename]
                        else:
                            image = self.default_ch_dict[base_filename]

                        self.backdrop.paste(image, (int(rel_x), int(rel_y)), image)#draw character sprite onto file
                    
        self.map_image = ImageTk.PhotoImage(self.backdrop)
        title = self.maincan.create_image(0,0,image=self.map_image, anchor="nw")

        self.session.animations = [] #clean animations
        
Memento_Mori().start()

#self.maincan.testimg2 = PIL.Image.open("testimg2.png")
#self.maincan.titlecardpil.paste(self.maincan.testimg2, (50,40), self.maincan.testimg2)
