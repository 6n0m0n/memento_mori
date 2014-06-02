#by 6n0m0n, SpaceSheep, and malachite_sprite
from ls_behavior import LS_behavior
from ls_midbehavior import LS_midbehavior
from ls_scaredypath import LS_scaredypath
from ls_move import LS_move

class LS_scaredymove(LS_midbehavior):

    def __init__(self, session, character, target_loc, avoid_arr, avoid_weights): #ideally this will be muti-type: a map coordinate or a character

        LS_midbehavior.__init__(self, session, character)
        self.target_loc = target_loc
        self.avoid_arr = avoid_arr
        self.avoid_weights = avoid_weights
        self.subtype = "scaredymove"
        #target_type = self.target.__class__.__name__ #"list", "LS_character", etc.

    def update_variables(self):
        next_loc = LS_scaredypath(self.character.position, self.target_loc, self.session, self.avoid_arr, self.avoid_weights)[1]
        self.children.append(LS_move(self.session, self.character, next_loc))

        if next_loc == self.target_loc:
            self.status = "finished"

    def update_triggers(self):
        bum = True

        
