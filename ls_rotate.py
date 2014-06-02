#by 6n0m0n, SpaceSheep, and malachite_sprite
from ls_behavior import LS_behavior
from ls_lowbehavior import LS_lowbehavior

class LS_rotate(LS_lowbehavior):

    def __init__(self, session, character, direct):

        LS_lowbehavior.__init__(self, session, character)
        self.subtype = "rotate"
        self.character.orientation = direct
        self.status = "finished"

    def update_character(self):

        bum = True
            
