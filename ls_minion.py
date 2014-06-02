#by 6n0m0n, SpaceSheep, and malachite_sprite
from ls_behavior import LS_behavior
from ls_highbehavior import LS_highbehavior
from ls_attack import LS_attack
from ls_derp import LS_derp
from ls_rotate import LS_rotate
from random import randrange

class LS_minion(LS_highbehavior):

    def __init__(self, session, character): #ideally this will be a character

        LS_highbehavior.__init__(self, session, character)
        self.children.append(LS_attack(self.session, self.character))
        self.children.append(LS_derp(self.session, self.character))

    def update_variables(self):
        if self.target_in_sight:
            self.children[0].update_self = True
            self.children[1].update_self = False
        else:
            direction = randrange(4)
            dirdict = [ (0, "N"),
                        (1, "E"),
                        (2, "S"),
                        (3, "W")
                        ]
            self.children[1] = LS_rotate(self.session, self, dirdict[randrange(4)])
            
            self.children[0].update_self = False
            self.children[1].update_self = True
            

    def update_triggers(self):
        self.target_in_sight = False
        for square in self.character.vision:
            if square.contained_ch.subtype == "target":
                self.target_in_sight = True
