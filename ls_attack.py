#by 6n0m0n, SpaceSheep, and malachite_sprite
from ls_behavior import LS_behavior
from ls_lowbehavior import LS_lowbehavior

class LS_attack(LS_lowbehavior):

    def __init__(self, session, character):
        LS_lowbehavior.__init__(self, session, character)
        self.subtype = "attack"

    def get_character(self):
        return self.character

    def update_character(self):
        print("attempting update")
        
