#by 6n0m0n, SpaceSheep, and malachite_sprite
from ls_behavior import LS_behavior
from ls_midbehavior import LS_midbehavior

class LS_movetoloc(LS_midbehavior):

    def __init__(self, session, character, targetloc): #ideally this will be muti-type: a map coordinate or a character

        LS_midbehavior.__init__(self, session, character)
        self.targetloc = targetloc

    def update_triggers(self):

        self.curr_loc = self.character.position
    
