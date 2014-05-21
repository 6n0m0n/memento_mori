#by 6n0m0n, SpaceSheep, and malachite_sprite

class LS_behavior:

    def __init__(self, session, character):
        
        self.session = session
        self.character = character
        self.children = []
        self.update_children = False
        self.status = "initiated"
        self.subtype = ""

    def update(self):
        
        self.update_triggers()
        self.update_variables()
        
        if self.update_children:
            for i in range(len(self.children)):
                if self.children[i].status in ["finished", "failure"]:
                    del self.children[i]
                else:
                    self.children[i].update()
