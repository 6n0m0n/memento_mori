#by 6n0m0n, SpaceSheep, and malachite_sprite
from ls_behavior import LS_behavior
from ls_midbehavior import LS_midbehavior
from ls_astar import next_location_in_path as nextloc
from ls_move import LS_move

class LS_movetoloc(LS_midbehavior):
    
    def __init__(self, session, character, targetloc):
        
        LS_midbehavior.__init__(self, session, character)
        self.targetloc=targetloc
        self.subtype="moveto"
    
    def update_variables(self):
        self.curr_loc=self.character.position
        if self.curr_loc==self.targetloc:
            self.status="finished"
        else:
            next_loc = nextloc(self.curr_loc, self.targetloc, self.session)
            if next_loc is None:
                self.status="failure"
            elif len( self.children )==0:
                self.children.append(LS_move(self.session, self.character, next_loc))
    
    def update_triggers(self):
        bum = True
    
