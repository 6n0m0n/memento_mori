#by 6n0m0n, SpaceSheep, and malachite_sprite
from ls_behavior import LS_behavior
from ls_highbehavior import LS_highbehavior
from ls_bite import LS_bite
from ls_derp import LS_derp
from ls_randomwalk import LS_randomwalk
from ls_astar import NY_dist
from ls_movetowards import LS_movetowards

class LS_zombie(LS_highbehavior):

    def __init__(self, session, character):

        LS_highbehavior.__init__(self, session, character)
        self.children = [LS_derp(self.session, self.character)]
        self.target = None
        self.subtype = "zombie"
        self.randomwalk = LS_randomwalk(self.session, self.character)

    def update_variables(self):
        if self.target is not None:
            if self.target_in_range:
                self.children[0] = LS_bite(self.session, self.character, self.target)
            else:
                self.children[0] = LS_movetowards(self.session, self.character, self.target)
        else:
            self.children[0] = self.randomwalk
        print ("finished updating variables")
        print (self.children)

    def update_triggers(self):
        self.target_in_range = False
        for square in self.character.vision:
            if square.contained_ch is not None and square.contained_ch.subtype == "walker":
                if NY_dist( [square.zloc, square.yloc, square.xloc], self.character.position ) == 1:
                    self.target = square.contained_ch
                    self.target_in_range = True
                    return
        for square in self.character.vision:
            if square.contained_ch is not None and square.contained_ch.subtype == "walker":
                self.target = square.contained_ch
                return
