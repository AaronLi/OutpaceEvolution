from pygame import draw, Rect, image, transform
from lib import game_object, colour_constants
import evolutionary_creature.creature
from lib.math_tools import scale_percentage


class SimulationEnvironment(game_object.GameObject):
    TREE_SPACING = 300

    def __init__(self, subjectCreature: evolutionary_creature.creature):
        self.test_subjects = [subjectCreature]

        if subjectCreature is not None:
            self.test_subjects[-1].reset()
            self.startPos = self.test_subjects[-1].get_pos()

        self.time = 0

        #used for when the player is controlling a creature
        self.creature_puppeteer = None

        self.active_creature = -1

        self.simulationSteps = 30 * 15 # 30 frames per second for 15 seconds

    def draw(self, surface, offsetX: int, offsetY: int, tree_sprite = None):
        # draw environment
        if tree_sprite is not None:
            num_trees = surface.get_width()//SimulationEnvironment.TREE_SPACING
            for i in range(-num_trees//2, num_trees//2+2):

                drawX = i*SimulationEnvironment.TREE_SPACING+offsetX%SimulationEnvironment.TREE_SPACING

                surface.blit(tree_sprite, (drawX, offsetY- tree_sprite.get_height()))

        draw.line(surface, (255,0,0), (offsetX+self.startPos[0], 0), (offsetX+self.startPos[0], surface.get_height()), 5)

        worldRect = Rect(0, offsetY, surface.get_width(), surface.get_height())
        draw.rect(surface, colour_constants.ENVIRONMENT_COLOUR, worldRect)

        # draw test subject
        self.test_subjects[self.active_creature].draw(surface, offsetX, offsetY)

        if self.creature_puppeteer is not None:
            self.creature_puppeteer.draw(surface, offsetX, offsetY)

    def update(self, time: int):
        self.simulate_step()

        if self.creature_puppeteer is not None:
            self.creature_puppeteer.update()

    def simulate_step(self):
        self.test_subjects[self.active_creature].update(self.time)
        self.time += 1

    def simulate_until_end(self):
        while self.time < self.simulationSteps:
            self.simulate_step()

        return self.get_progress()

    def simulation_done(self):
        return self.time >= self.simulationSteps

    def get_progress(self):
        subject_pos = self.test_subjects[self.active_creature].get_pos()

        return subject_pos[0] - self.startPos[0], self.startPos[1] - subject_pos[1]

    def reset(self):
        self.time = 0
        self.test_subjects[self.active_creature].reset()

        if self.creature_puppeteer is not None:
            self.creature_puppeteer.reset()

    def set_creature(self, new_subject):
        self.test_subjects.append(new_subject)
        self.active_creature = -1
        self.reset()
        self.startPos = self.test_subjects[self.active_creature].get_pos()

    def set_active_creature(self, creatureIndex):
        if creatureIndex < 0:
            self.active_creature = max(creatureIndex, -len(self.test_subjects))
        elif creatureIndex >= 0:
            self.active_creature = max(-len(self.test_subjects), creatureIndex - len(self.test_subjects))

    def last_creature(self):
        self.set_active_creature(self.active_creature+len(self.test_subjects)-1)

    def next_creature(self):
        self.set_active_creature(self.active_creature+1)

    def get_active_creature(self):
        return self.test_subjects[self.active_creature]