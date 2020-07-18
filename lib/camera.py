from math import atan2, sin, cos, hypot

class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.vx = 0
        self.vy = 0
        
        self.targetX = x
        self.targetY = y

        self.moveSpeed = 1

    def set_target(self, targetX, targetY):
        self.targetX = targetX
        self.targetY = targetY

    def update(self):

        deltaX = self.get_deltaX()

        deltaY = self.get_deltaY()

        angle_to_target = atan2(deltaY, deltaX)

        distance = max(hypot(deltaX, deltaY)/30, 0.2)

        self.vx = abs(cos(angle_to_target) * self.moveSpeed * distance)
        self.vy = abs(sin(angle_to_target) * self.moveSpeed * distance)

        if self.x < self.targetX:
            self.x+=self.vx
            if self.x > self.targetX:
                self.x = self.targetX
        elif self.x > self.targetX:
            self.x-=self.vx
            if self.x < self.targetX:
                self.x = self.targetX
    
        if self.y < self.targetY:
            self.y += self.vy
            if self.y > self.targetY:
                self.y = self.targetY
        elif self.y > self.targetY:
            self.y -= self.vy
            if self.y < self.targetY:
                self.x = self.targetX

    def get_deltaX(self):
        return self.x - self.targetX

    def get_deltaY(self):
        return self.y - self.targetY