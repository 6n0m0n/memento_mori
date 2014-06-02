#by 6n0m0n, SpaceSheep, and malachite_sprite
from ls_behavior import LS_behavior
from ls_midbehavior import LS_midbehavior
from ls_movetoloc import LS_movetoloc
from ls_derp import LS_derp
from random import randrange

class LS_randomwalk(LS_midbehavior):
    
    def __init__(self, session, character):
        
        LS_midbehavior.__init__(self, session, character)
        self.target_loc = character.position
        self.subtype = "randomwalk"
    
    def update_variables(self):

        if len(self.children) == 0:
            self.target_loc = self.get_random_open_square(self.session)
            print ("moving to ", self.target_loc)
            self.children.append(LS_movetoloc(self.session, self.character, self.target_loc))
        else:
            for i in range(len(self.children)):
                if self.children[i].status == "failed":
                    self.children[i] = LS_derp(self.session, self)
                    
    
    def update_triggers(self):
        
        bum = True
    
    def get_random_open_square(self, session):
        # WARNING: here there be monsters
        new_x = randrange( len(self.session.map_arr[0][0]) )
        new_y = randrange( len(self.session.map_arr[0]) )
        new_z = randrange( len(self.session.map_arr) )
        # you have been warned...
        if session.map_arr[new_z][new_y][new_x].pathblocker:
            return self.get_random_open_square(session)
        else:
            return [new_z, new_y, new_x]
