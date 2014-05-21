#by 6n0m0n, SpaceSheep, and malachite_sprite
from ls_behavior import LS_behavior
from ls_midbehavior import LS_midbehavior
from ls_astar import next_point_in_path as route
from ls_move import LS_move

class LS_movetoloc(LS_midbehavior):
    
    def __init__(self, session, character, targetloc):
        
        LS_midbehavior.__init__(self, session, character)
        self.targetloc = targetloc
        self.subtype = "moveto"
    
    def update_variables(self):
        # just a note: the deletion of finished children really ought to happen right after
        # the children finish their updates
        self.curr_loc = self.character.position
        if self.curr_loc == self.targetloc:
            self.status = "finished"
        else:
            next_loc = route( self.curr_loc, self.targetloc, self.session )
            if next_loc is None:
                self.status = "failure"
            elif len( self.children ) == 0:
                self.children.append(LS_move( self.session, self.character, next_loc ) )
        # NB! make sure ls_move sets status to "finished" after moving the character
    
    def update_triggers(self):
        
        bum = True
    
