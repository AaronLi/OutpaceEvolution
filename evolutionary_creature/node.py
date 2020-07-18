from lib.game_object import GameObject
from math import hypot
from pygame import Rect, draw
from lib.math_tools import clamp

class Node(GameObject):
    def __init__(self, startX :float, startY :float, mass :float, friction :float):

        self.mass = mass

        #positions are relative to the world
        self.startX = startX
        self.startY = startY

        self.x = startX
        self.y = startY

        self.vx = 0
        self.vy = 0
        self.friction = friction
        self.colour_scheme = 0

    def reset(self):
        self.x = self.startX
        self.y = self.startY
        self.vx = 0
        self.vy = 0

    def get_node_distance(self, otherNode) -> float:
        deltaX = self.x - otherNode.x
        deltaY = self.y - otherNode.y

        return hypot(deltaX, deltaY)

    def get_starting_node_distance(self, otherNode) -> float:
        deltaX = self.startX - otherNode.startX
        deltaY = self.startY - otherNode.startY

        return hypot(deltaX, deltaY)

    def update(self, time :int, air_friction = 0.95, gravity = 0.1):
        self.vx *= air_friction
        self.vy *= air_friction
        self.apply_gravity(gravity)
        self.x+=self.vx
        self.y+=self.vy

    def get_radius(self): # radius of this node for math and drawing
        return int((self.mass*50)**0.5)

    def collide_with_environment(self, rects :tuple, groundBounce = 0.2):

        normalForce = max(self.vy * self.mass, 0) # vertical normal force into the ground


        if self.y+self.get_radius() > 0: # if intersecting with ground
            self.vy = -self.vy * groundBounce
            self.y = -self.get_radius()
            self.x -= self.vx * self.friction * normalForce

            if self.vx > 0:
                self.vx -= normalForce * self.friction

                if self.vx < 0:
                    self.vx = 0

            elif self.vx < 0:
                self.vx += normalForce * self.friction

                if self.vx > 0:
                    self.vx = 0

    def apply_gravity(self, gravity = 0.1):
        self.vy += gravity

    def draw(self, surface, offsetX, offsetY):
        drawRect = draw.circle(surface, self.get_colour(), (int(self.x+offsetX), int(self.y+offsetY)), self.get_radius())

    def get_colour(self):

        colour = [0,0,0]

        colour[self.colour_scheme] = max(min(255, 255*self.friction * self.mass/1.5), 100)

        return tuple(colour)

    def set_startX(self, newX):
        self.startX = newX
        self.x = newX

    def set_startY(self, newY):
        self.startY = newY
        self.y = newY
    
    def set_colour_scheme(self, colour_index :int):
        self.colour_scheme = clamp(colour_index, 0, 2)