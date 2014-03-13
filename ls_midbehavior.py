#by 6n0m0n, SpaceSheep, and malachite_sprite
from ls_behavior import LS_behavior

class LS_midbehavior(LS_behavior):

    def __init__(self, session, character):
        LS_behavior.__init__(self, session, character)
        self.update_children = True
