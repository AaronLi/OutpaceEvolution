from lib.game_object import GameObject

class Creature(GameObject):
    def __init__(self, name):
        self.name = name
        self.nodes = []
        self.muscles = []

    def draw(self, surface, offsetX :int, offsetY :int):
        for cMuscle in self.muscles:
            cMuscle.draw(surface, offsetX, offsetY)
        for cNode in self.nodes:
            cNode.draw(surface, offsetX, offsetY)

    def update(self, time):
        for cMuscle in self.muscles:
            cMuscle.update(time)

        #do wall collisions

        for cNode in self.nodes:
            cNode.collide_with_environment(tuple())

        for cNode in self.nodes:
            cNode.update(time)

    def reset(self):
        for cNode in self.nodes:
            cNode.reset()

        for cMuscle in self.muscles:
            cMuscle.reset()

    def addNode(self, nodeIn):
        self.nodes.append(nodeIn)
    def addMuscle(self, muscleIn):
        self.muscles.append(muscleIn)

    def get_pos(self):
        xPos = 0
        yPos = 0

        if len(self.nodes) == 0:
            return 0, 0

        for cNode in self.nodes:
            xPos += cNode.x
            yPos += cNode.y

        return xPos/len(self.nodes), yPos/len(self.nodes)

    def get_configuration(self):
        return len(self.nodes), len(self.muscles)

    #if two creatures move the same distance then this will be used
    def __gt__(self, other):
        return 0

    def set_colour_scheme(self, colour):
        for i in self.nodes:
            i.set_colour_scheme(colour)