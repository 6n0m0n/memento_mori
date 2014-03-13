#by 6n0m0n, SpaceSheep, and malachite_sprite
from ls_behavior import LS_behavior
from ls_midbehavior import LS_midbehavior

class LS_movetowards(LS_midbehavior):

    def __init__(self, session, character, target): #ideally this will be muti-type: a map coordinate or a character

        LS_midbehavior.__init__(self, session, character)
        self.target = target

        target_type = self.target.__class__.__name__ #"list", "LS_character", etc.

    def update_triggers(self):

        if target_type == "LS_character":
            #check whether target character is in vision
