#by 6n0m0n, SpaceSheep, and malachite_sprite
from ls_behavior import LS_behavior
from ls_highbehavior import LS_highbehavior
from ls_movetoloc import LS_movetoloc
from ls_randomwalk import LS_randomwalk
from ls_derp import LS_derp

class LS_movetowards(LS_highbehavior):

    def __init__(self, session, character, target): #ideally this will be a character

        LS_highbehavior.__init__(self, session, character)
        self.target = target
        self.children.append(LS_randomwalk(self.session, self.character))
        self.children.append(LS_derp(self.session, self.character))
        self.target_in_sight = False

    def update_variables(self):
        if self.target_in_sight:
            self.children[1] = LS_movetoloc(self.session, self.character, self.target.position)
            self.children[0].update_self = False
            self.children[1].update_self = True
        else:
            self.children[0].update_self = True
            self.children[1].update_self = False
        print ("movetowards finished updating variables")

    def update_triggers(self):
        self.target_in_sight = False
        for square in self.character.vision:
            if self.target == square.contained_ch:
                self.target_in_sight = True
        print("movetowards finished updating triggers")
