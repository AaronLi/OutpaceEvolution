# creature_puppeteer.py
# Dumfing
# Entry point for user to control the muscles of a creature
#"Puppeteering" more like Dance Dance Revolution

from pygame.locals import *
from pygame import key, draw, font
from lib import game_object
from lib import colour_constants as colour

if font.get_init():
    KEY_FONT = font.Font("assets/Montserrat-Regular.otf", 25)

class CreaturePuppeteer(game_object.GameObject):

    USABLE_KEYS = (K_q, K_w, K_o, K_p)

    def __init__(self, creature):
        self.creature = creature
        self.creature.set_colour_scheme(2)
        self.keybinds = {}
        self.keyStates = {}
        self.oldKeysDown = []

        self.auto_assign_keys()
        self.triggerClock = 0


    def set_creature(self, creature):
        self.creature = creature
        self.auto_assign_keys()
        self.creature.set_colour_scheme(2)

    
    def auto_assign_keys(self):
        self.keybinds = {}
        self.keyStates = {}
        for muscle, boundKey in zip(self.creature.muscles, CreaturePuppeteer.USABLE_KEYS):
            self.keybinds[boundKey] = muscle
            self.keyStates[boundKey] = False

    def update(self):
        keysDown = key.get_pressed()

        for i in self.keybinds:
            if keysDown[i] and not self.oldKeysDown[i]:
                self.keyStates[i] = not self.keyStates[i]
                if self.keyStates[i]:
                    self.keybinds[i].contract()
                else:
                    self.keybinds[i].extend()

        self.creature.update(-1)
        self.triggerClock+=1
        self.oldKeysDown = keysDown

    def draw(self, surface, offsetX: int, offsetY: int):
        self.creature.draw(surface, offsetX, offsetY)

        key_trigger_times = self.get_key_trigger_times()

        for i, v in enumerate(self.keyStates):
            muscle_cycle_time = self.triggerClock % self.keybinds[v].cycle_time
            keyColor = colour.KEY_RED if self.keyStates[v] else colour.KEY_BLUE

            newMuscleState = colour.RED if muscle_cycle_time < self.keybinds[v].change_time else colour.BLUE

            key_combo_height = surface.get_height()//2 + 150

            draw.rect(surface, keyColor, (i*76+15, key_combo_height, 50, 10))

            draw.rect(surface, newMuscleState, (i*76+5, key_combo_height + key_trigger_times[v][0] * 3-10, 70, 20))

            key_font_render = KEY_FONT.render(key.name(v).upper(), True, colour.LIGHT_GREY, keyColor)

            surface.blit(key_font_render, (i*76 + 5 + 35 - key_font_render.get_width()//2, key_combo_height - key_font_render.get_height()))
        

    def reset(self):
        self.creature.reset()
        self.triggerClock = 0

        for i in self.keybinds:
            self.keyStates[i] = False

    def get_bound_keys(self):
        return tuple(map(key.name, self.keybinds.keys()))

    def get_key_trigger_times(self):
        outTimes=  {}

        for i in self.keybinds:
            outTimes[i] = (self.keybinds[i].get_time_until_next_trigger(self.triggerClock), self.keybinds[i].get_contracted())
        
        return outTimes

        