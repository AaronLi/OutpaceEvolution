from lib import game_object

class StatusWindow(game_object.GameObject):
    def __init__(self, drawFont):
        self.display_elements = []
        self.element_separation = 3
        self.draw_font = drawFont

    def update(self, time):
        pass

    def draw(self, surface, offsetX, offsetY):
        yOffset = 0
        for i in self.display_elements:
            element_rendering = self.draw_font.render(str(i), True, (255,255,255), (0,0,0))

            yOffset+=element_rendering + self.element_separation

