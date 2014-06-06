#by 6n0m0n, SpaceSheep, and malachite_sprite
from ls_behavior import LS_behavior
from ls_midbehavior import LS_midbehavior
from ls_astar import next_location_in_path as nextloc
from ls_move import LS_move
from ls_derp import LS_derp

class LS_movetoloc(LS_midbehavior):
    
    def __init__(self, session, character, targetloc):
        
        LS_midbehavior.__init__(self, session, character)
        self.targetloc=targetloc
        self.subtype="movetoloc"
    
    def update_variables(self):
        self.curr_loc=self.character.position
        if self.curr_loc==self.targetloc:
            #print ("movetoloc finished")
            self.status="success"
        else:
            next_loc = nextloc(self.character, self.curr_loc, self.targetloc, self.session)
            if next_loc is None:
                print ("movetoloc failed")
                self.children=[LS_derp(self.session, self.character)]
            elif len( self.children ) == 0:
                #print ("movetoloc continuing")
                self.children.append(LS_move(self.session, self.character, next_loc))
            #else:
                #print ("movetoloc else")

    def update_triggers(self):
        bum = True
    
