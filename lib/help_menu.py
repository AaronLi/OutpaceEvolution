#just so there isn't a block of text to read in main.pow

from lib import game_object
from lib import colour_constants as colour
from pygame import Surface, draw, font, rect

help_text = """What is this?
    It's an evolution simulator! It generates random creatures (initially!) whose only goal in life is to make it as far right as possible. After making this initial generation it will simulate the creature's entire 15 second lifetime before killing off the 900 worst creatures and making modifications to the 100 best in hopes of improving their movement capabilities. This process repeats ad infinitum

    Is this a game?
    Well... it was made as an evolution simulator first and a game second, turns out our tiny primitive human brains have a difficult time controlling 2D node based creatures and so the game part of this is optional but still included (free of charge!). The idea is to use the displayed keys to toggle a muscle on the creature. The bars you see moving towards the keys are the moments to hit if you wish to sync up with the creature's internal timing system that it would use to control it's own muscles. Follow them if you wish or freestyle if you believe your enormous human brain can be easily modified to control the simple creature's body.
    [p] Some useful keys:

    Space - restarts the simulation to t = 0, the start of the current creature's life
    Left Arrow Key- switches the currently displayed creature (red) to the creature that came before it, assuming it exists
    Right Arrow Key- switches the currently displayed creature (red) to the creature that came after it, assuming it exists
    A - turns off auto generation, in case you didn't want the progression of evolution to change the red creature you're interacting with
    V - clones the current red creature being simulated and sets it as your blue creature for you to control and interact with
    1 - simulates a generation of 1000 creatures in the background without turning on automatic background generation
    H - toggles this help screen on and off

    Feel free to dig around and modify the code to your satisfaction
    Inspired by CaryKH
    (I'm surprised the text fit into each page so easily!)

    Some more advanced stuff:
    This program uses Python 3's multiprocessing library to simulate one thousand creatures all in the background to have minimal impact on the render thread. It uses pygame to draw creatures and it uses vanilla Python 3 and some clever math to do physics simulation of the creatures.

    If you are running this program on a more powerful computer with access to more than 2 cores you can increase the amount of processes used for background evolving in ./lib/evolution_driver.py in the __init__ function's num_processes. If evolving creatures is the only thing you wish to do I recommend leaving one thread available for graphics and the remaining for simulating, i.e. An 8 core 16 thread Processor should have 15 processes for simulating and one remaining for graphics.

    If you want more complex creatures that you don't wish to have enough keys to control, you can look into ./evolutionary_creature/creature_factory's node_count_max and increase it. Note that ./lib/creature_puppeteer.py won't be able to control creatures with more than 4 muscles so complex creatures are only for visual enjoyment.

    You can get a much better experience running this on your personal computer offline but repl's online interpreter works for evaluating the program.

    Go to the next page for a breakdown of the files that comprise this program
    [p] A quick breakdown of the files and what they do:
    
    main.py
    > The main program, not much to configure here. You can change fonts
    > or the tree sprites used in the background
    
    assets

    assets/Montserrat-Regular.otf
    > The font used for everything

    assets/tree.png
    > The sprite used for the simulation's background

    evolutionary_creature

    evolutionary_creature/creature.py
    > A class that combines nodes and muscles together, it mostly wraps
    > together nodes and muscles into an easy interface that can be
    > called to call all it's components as a whole. Not much to modify
    > here, but you can see how it works

    evolutionary_creature/creature_factory.py
    > A class that generates random nodes, muscles, and creatures. If you
    > wish to make major changes to how creatures behave like muscle 
    > strength and timing or node weight and friction, then this is the
    > place to go

    evolutionary_creature/muscle.py
    > Muscles apply forces to nodes in a creature. Not much to modify
    > but it's there for your evaluation and enjoyment

    evolutionary_creature/node.py
    > Nodes are the component of the creature that have mass and can
    > push it around with friction. Again, not much to modify

    lib/camera.py
    > The camera class is what provides the smooth moving and panning
    > you see when creatures move around or the simulation is reset
    > You can modify the camera's acceleration curve through the
    > distance equation in the camera's update function

    lib/colour_constants.py
    > Colour constants. Changing some of the basic colour constants may
    > lead to unexpected graphical changes elsewhere in the program but
    > key_red, key_blue, environment_colour, and sky_colour should be
    > safe to modify

    lib/creature_puppeteer.py
    > This is the player's interface into the blue creature's muscles
    > You can modify the keys used in creature_puppeteer.USABLE_KEYS
    > Refer to pygame's key constants for adding key constants

    lib/evolution_driver.py
    > OOOOOOOO this is file is where the cool stuff happens.
    > You can change how much creatures are modified between
    > generations by modifying the mutate_creature function,
    > you can change how creatures are removed from the
    > 'gene pool' in the _cull_creatures function, and you
    > can change how the creatures are reproduced to form the
    > next generation in the _reproduce_creatures function. 
    > All the stuff actually dealing with multiprocessing should be fine
    > and shouldn't need modification but if you know what you're doing
    > feel free to play around with it. Just be sure you don't make any
    > process leaks...

    lib/game_object.py
    > This is a template for how anything that exists in the game can be
    > interacted with it's basic and shouldn't be modified, unless you want
    > a feature to be in everything that's drawn or updated

    lib/help_menu.py
    > Hey that's where this text is stored! If you want to add your own
    > text to the help menu then type away. The renderer takes account for
    > \\ n newline characters and will convert [ p ] into a new page. Otherwise
    > the text will have basic auto line wrapping

    lib/math_tools.py
    > useful math tools, modify this if you wish to break things. Otherwise,
    > adding things to this won't do anything as the functions must be
    > explicitly called elsewhere

    lib/simulation_environment.py
    > This is where creatures live their entire lives. Not much to modify other
    > than how long the simulations run for. Default is
    > 30 * 15 (30 fps/ 15 seconds)
    > but you can change the 15 to any number of seconds you wish. This
    > will increase the amount of time it takes to simulate each generation.

    wip_features
    > I'm not gonna bother to comment on these. I kinda wanted to add
    > them but lost interest during development
    """

class HelpMenu(game_object.GameObject):
    def __init__(self,drawFont: font.Font, width = 750, height = 550):
        self.current_page = 0
        self.pages = [Surface((width, height))]
        self.pages[0].fill(colour.WHITE)
        drawArea = rect.Rect(5,5,width-5, height-5)

        wordHorizontalSpacing = 5
        wordVerticalSpacing = 2
        leftMargin = 10
        topMargin = 7
        wordXOffset = leftMargin
        wordYOffset = topMargin
        for line in help_text.split('\n'):
            for word in line.split():

                if word == '[p]':
                    wordXOffset = leftMargin
                    wordYOffset = topMargin
                    self.pages.append(Surface((width, height)))
                    self.pages[-1].fill(colour.WHITE)
                    continue
                renderedWord = drawFont.render(word, True, colour.BLACK)

                if wordXOffset+renderedWord.get_width()+wordHorizontalSpacing > drawArea.width:
                    wordXOffset = leftMargin
                    wordYOffset += wordVerticalSpacing + renderedWord.get_height()

                if wordYOffset + renderedWord.get_height() + wordVerticalSpacing > drawArea.height:
                    wordYOffset = topMargin
                    self.pages.append(Surface((width, height)))
                    self.pages[-1].fill(colour.WHITE)

                self.pages[-1].blit(renderedWord, (wordXOffset, wordYOffset))

                wordXOffset += wordHorizontalSpacing + renderedWord.get_width()
            
            wordYOffset += drawFont.get_height()+wordVerticalSpacing
            wordXOffset = leftMargin

        for i,v in enumerate(self.pages):
            pageNumberRender = drawFont.render("<- Page %d of %d ->"%(i+1, len(self.pages)), True, colour.BLACK)

            v.blit(pageNumberRender, (v.get_width() - pageNumberRender.get_width() - 3, v.get_height() - pageNumberRender.get_height() - 3))

    def update(self, time):
        pass

    def draw(self, surface, offsetX, offsetY):

        drawPage = self.pages[self.current_page]
            
        surface.blit(drawPage, (surface.get_width()//2 - drawPage.get_width()//2, surface.get_height()//2 - drawPage.get_height()//2))

    def next_page(self):
        self.current_page = (self.current_page + 1) % len(self.pages)

    def last_page(self):
        self.current_page = (self.current_page - 1) % len(self.pages)