from lib.game_object import GameObject
from pygame import draw
import evolutionary_creature.node as creatureNode
from math import atan2, sin, cos, degrees

class Muscle(GameObject):
    def __init__(self, node1 :creatureNode.Node, node2 :creatureNode.Node, force :float, change_time :int, cycle_time: int, contracted_length: float):

        # essentially the tendons of the muscle, the nodes the muscle exists between
        self.node1 = node1
        self.node2 = node2

        # muscle starts trying to extend
        # change_time is when the muscle begins trying to contract to its contracted length
        # cycle time is when the muscle interaction timer loops around to extend and contract again
        #yes I know real muscles can only contract or relax
        self.change_time = change_time
        self.cycle_time = cycle_time

        #contracted length is a value in the interval (0,1) relative to the extended length
        self.contracted_length = contracted_length

        self.target_length = self.get_extended_length()

        self.force = force # arbitrary units, tbd

        self.contracted = False

    def reset(self):
        self.target_length = self.get_extended_length()

    def update(self, time :int):
        timeInCycle = time%self.cycle_time

        if time >= 0: # negative time means muscle is disabled

            if timeInCycle < self.change_time:
                self.extend()
            else:
                self.contract()

        self.apply_force()

    def get_length(self) -> float:
        return self.node1.get_node_distance(self.node2)

    def apply_force(self):
        target_percentage = 1 - (self.get_length() / self.target_length)

        appliedForce = min(0.9, max(-0.9, target_percentage * self.force))

        deltaX = self.node1.x - self.node2.x
        deltaY = self.node1.y - self.node2.y

        angle = atan2(deltaY, deltaX)

        #pull nodes together
        self.node1.vx += cos(angle) * appliedForce / self.node1.mass
        self.node1.vy += sin(angle) * appliedForce / self.node1.mass

        self.node2.vx -= cos(angle) * appliedForce / self.node2.mass
        self.node2.vy -= sin(angle) * appliedForce / self.node2.mass


    def get_contracted_length(self) -> float:
        return self.get_extended_length()*self.contracted_length

    def get_extended_length(self) -> float:
        return max(self.node1.get_starting_node_distance(self.node2), 0.001)

    def draw(self, surface, offsetX, offsetY):
        drawRect = draw.line(surface, self.get_colour(), (int(self.node1.x+offsetX), int(self.node1.y+offsetY)), (int(self.node2.x + offsetX), int(self.node2.y + offsetY)), max(int(self.force*1.6), 2))

    def get_colour(self):
        light_grey = 255
        dark_grey = 50

        difference = light_grey - dark_grey

        extension_percentage = self.get_extension_percentage()

        draw_grey = min(max( difference * extension_percentage + dark_grey, dark_grey), light_grey)

        return draw_grey, draw_grey, draw_grey

    def get_extension_percentage(self):
        return self.get_length() / self.get_extended_length()

    def contract(self):
        self.target_length = self.get_contracted_length()
        self.contracted = True

    def extend(self):
        self.target_length = self.get_extended_length()
        self.contracted = False

    def get_time_until_next_trigger(self, time):
        time_in_cycle = time%self.cycle_time

        if time_in_cycle < self.change_time:
                return self.change_time - time_in_cycle

        else:
            return self.cycle_time - time_in_cycle

    def get_contracted(self):
        return self.contracted