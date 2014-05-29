#by 6n0m0n, SpaceSheep, and malachite_sprite

class LS_behavior:

    def __init__(self, session, character):
        
        self.session = session
        self.character = character
        self.children = []
        self.update_children = False
        self.update_self = True
        self.status = "initiated"
        self.subtype = ""

    def update(self):
        if self.update_self:
            self.update_triggers()
            self.update_variables()
        
            if self.update_children:
                for i in range(len(self.children)):
                    self.children[i].update()

            self.children = [s for s in self.children if (not (s.status in ["finished", "failure", "success"]))]
