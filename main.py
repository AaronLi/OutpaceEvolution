# R to reset generation
# space to turn off automatic generation queueing
# 1 to generate next generation
# Left arrow key to go to last creature
# Right arrow key to go to next creature (assuming it has been generated)

#High score: Peewee, 5 nodes, 8 muscles, 1067.76 pixels ~450 generations
#High score: Peewee, 4 nodes, 5 muscles, 1435.56 pixels 6750 generations

if __name__ == "__main__":
    from pygame import *

    font.init()

    from evolutionary_creature import creature, node, muscle, creature_factory
    import lib.colour_constants as colour
    import lib.simulation_environment as simEnv
    import lib.evolution_driver as evoDriver
    from lib.math_tools import scale_percentage
    from lib import camera, help_menu
    from lib import creature_puppeteer
    import copy

    
    screen = display.set_mode((800,600))

    tree_sprite = scale_percentage(image.load("assets/tree.png").convert_alpha(), 0.4)

    montseratSmall = font.Font("assets/Montserrat-Regular.otf", 20)
    montseratMedium = font.Font("assets/Montserrat-Regular.otf", 50)
    montseratLarge = font.Font("assets/Montserrat-Regular.otf", 100)

    helpMenu = help_menu.HelpMenu(montseratSmall)

    cFactory = creature_factory.CreatureFactory()

    environment = simEnv.SimulationEnvironment(next(cFactory))

    activeCreaturePos = environment.get_active_creature().get_pos()

    cam = camera.Camera(activeCreaturePos[0], activeCreaturePos[1])

    puppeteer = creature_puppeteer.CreaturePuppeteer(next(cFactory))

    environment.creature_puppeteer = puppeteer

    running = True

    auto_generate = True

    show_help = False

    evolver = evoDriver.EvolutionDriver(environment, [next(cFactory) for i in range(1000)])

    results = evolver.simulate_creatures_in_background()


    clockity = time.Clock()

    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    environment.reset()

                elif e.key == K_1:
                    evolver.simulate_creatures_in_background()

                elif e.key == K_LEFT:
                    if show_help:
                        helpMenu.last_page()
                    else:
                        environment.last_creature()
                        environment.reset()

                elif e.key == K_RIGHT:
                    if show_help:
                        helpMenu.next_page()
                    else:
                        environment.next_creature()
                        environment.reset()

                elif e.key == K_a:
                    auto_generate = not auto_generate

                    print("\nAuto generate:", "on" if auto_generate else "off")

                elif e.key == K_v:
                    puppeteer.set_creature(copy.deepcopy(environment.get_active_creature()))

                    environment.reset()

                elif e.key == K_h:
                    show_help = not show_help

        if not environment.simulation_done():
            environment.update(0)

        if not evolver.is_simulating() and auto_generate:
            evolver.simulate_creatures_in_background()

        creature_progress = environment.get_progress()

        creaturePos = environment.get_active_creature().get_pos()

        cam.set_target(creaturePos[0], creaturePos[1])

        screen.fill(colour.SKY_COLOUR)

        cam.update()

        environment.draw(screen, 400-cam.x, cam.y+350, tree_sprite)

        if environment.simulation_done():
            simDoneRender = montseratMedium.render("END OF SIMULATION", True, colour.WHITE, colour.BLACK)

            screen.blit(simDoneRender, (400 - simDoneRender.get_width()//2, 400 - simDoneRender.get_height()//2))

            spaceToRestart = montseratSmall.render("(Space to replay)", True, colour.WHITE, colour.BLACK)

            screen.blit(spaceToRestart, (400 - spaceToRestart.get_width()//2, 400 + simDoneRender.get_height()//2+10+spaceToRestart.get_height()//2))

        frameRateRender = montseratSmall.render("FPS: %.2f"%(clockity.get_fps()), True, colour.WHITE, colour.BLACK)

        positionRender = montseratSmall.render("X: %-7.2f Y: %.2f"%(creature_progress[0], creature_progress[1]), True, colour.WHITE, colour.BLACK)

        simDurationRender = montseratSmall.render("Simulation time: %.2fs"%(environment.time/30), True, colour.WHITE, colour.BLACK)

        creatureNumberRender = montseratSmall.render("Generation %d"%(environment.active_creature + len(environment.test_subjects)+1), True, colour.WHITE, colour.BLACK)

        keyBindingRender = montseratSmall.render("press \"h\" to toggle help", True, colour.WHITE, colour.BLACK)


        screen.blit(frameRateRender, (3, 3))
        screen.blit(positionRender, (3, 6+frameRateRender.get_height()))
        screen.blit(simDurationRender, (3, 9+frameRateRender.get_height()+positionRender.get_height()))

        screen.blit(creatureNumberRender, (3, 12+frameRateRender.get_height()+positionRender.get_height() + simDurationRender.get_height()))

        screen.blit(keyBindingRender, (3, 15+frameRateRender.get_height()+positionRender.get_height() + simDurationRender.get_height() + creatureNumberRender.get_height()))

        if show_help:
            helpMenu.draw(screen, 0,0)

        display.flip()

        clockity.tick(30)
    quit()