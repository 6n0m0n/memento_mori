#by 6n0m0n, SpaceSheep, and malachite_sprite
from ls_behavior import LS_behavior

class LS_highbehavior(LS_behavior):
    
    # honestly this is the exact same as ls_midbehavior, maybe we should just join them?
    
    def __init__(self, session, character):
        LS_behavior.__init__(self, session, character)
        self.update_children = True