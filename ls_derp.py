#by 6n0m0n, SpaceSheep, and malachite_sprite
from ls_behavior import LS_behavior
from ls_lowbehavior import LS_lowbehavior

class LS_derp(LS_lowbehavior):

    def __init__(self, session, character):

        LS_lowbehavior.__init__(self, session, character)
        self.subtype = "derp"

    def update_character(self):

        bum = True
            
