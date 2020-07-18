from multiprocessing import pool, cpu_count
import time, copy, random
from lib.math_tools import clamp, random_step_float, random_step_int
from lib import simulation_environment
from evolutionary_creature import creature_factory

print("CPU core count: %d"%cpu_count())

def single_simulation(environment, creature):
    environment.set_creature(creature)
    results = environment.simulate_until_end()
    return results, creature



class EvolutionDriver:
    def __init__(self, environment, creatureList, num_processes = 1):
        print("Using %d process(es) for simulation"%(num_processes))
        self.environment = environment
        self.creature_list = creatureList
        self.num_processes = num_processes
        self.simulation_in_progress = False #it's a mutex lock I guess
        self.simPool = pool.Pool(num_processes)
        self.simState = None
        self.creature_factory = creature_factory.CreatureFactory()

    def simulate_creatures(self):

        print("Beginning simulation of %d creatures"%(len(self.creature_list)))

        start_time = time.time()
        test_data = [(self.environment, i) for i in self.creature_list]

        output = pool.Pool(processes = self.num_processes).starmap(single_simulation, test_data)

        print('finished in %.2f seconds'%(time.time()-start_time))

        best_result = max(output)

        nodes, muscles = best_result[1].get_configuration()

        print("the best one travelled %.2f pixels, it has %d nodes and %d muscles"%(best_result[0][0], nodes, muscles))
        return output

    def simulate_creatures_in_background(self):
        # after running a simulation, the best creature of the generation is placed into the demo environment and a new generation is prepared
        if not self.simulation_in_progress:
            self.simulation_in_progress = True
            print("\nBeginning simulation of %d creatures in background"%(len(self.creature_list)))

            test_data = [(self.environment, i) for i in self.creature_list]

            self.simState = self.simPool.starmap_async(single_simulation, test_data, callback= self._generate_new_generation)
        else:
            print("Simulation already in progress")
            if self.simState.ready():
                self.simulation_in_progress = False
                print(self.simState.successful())

    def set_creature_list(self, creatureList):
        self.simPool.terminate()
        self.simPool = pool.Pool(self.num_processes)
        self.creature_list = creatureList

    def is_simulating(self):
        return self.simulation_in_progress

    def mutate_creature(self, creature):

        MUSCLE_CHANGE_CHANCE = 0.3 # 0.05 would be a 5% chance
        NODE_CHANGE_CHANCE = 0.3

        creatureOut = copy.deepcopy(creature)

        for cMuscle in creatureOut.muscles:

            if random.random() < MUSCLE_CHANGE_CHANCE:

                cMuscle.cycle_time = random_step_int(cMuscle.cycle_time, 4, creature_factory.min_cycle_time, creature_factory.max_cycle_time)

                cMuscle.change_time = random_step_int(cMuscle.change_time, 3, creature_factory.min_extend_time, cMuscle.cycle_time-10)

                cMuscle.contracted_length = random_step_float(cMuscle.contracted_length, 0.1, creature_factory.min_contraction_amount, creature_factory.max_contraction_amount)

                cMuscle.force = random_step_float(cMuscle.force, 0.05, creature_factory.min_force, creature_factory.max_force)

        for cNode in creatureOut.nodes:

            if random.random() < NODE_CHANGE_CHANCE:
                cNode.set_startX(random_step_float(cNode.startX, 3, creature_factory.node_xmin, creature_factory.node_xmax))

                cNode.set_startY(random_step_float(cNode.startY, 3, creature_factory.node_ymin, creature_factory.node_ymax))

                cNode.mass = random_step_float(cNode.mass, 0.1, creature_factory.min_node_weight, creature_factory.max_node_weight)

                cNode.friction = random_step_float(cNode.friction, 0.1, creature_factory.min_node_friction, creature_factory.max_node_friction)

        return creatureOut

    def _cull_creatures(self, creature_data): # takes in a list of endposition, creature pairs
        originalCount = len(creature_data)
        creature_data.sort(reverse=True)
        outList = creature_data[:100]
        print("Culled %d creatures down to %d"%(originalCount, len(outList)))
        return [i[1] for i in outList]

    def _reproduce_creatures(self, creatureList):
        #assumes creatures are already sorted by largest to small
        originalListLength = len(creatureList)
        numCreaturesGenerated = 0
        for i in range(originalListLength):
            new_creature_amount = int(1.0357**(originalListLength-i))
            for j in range(new_creature_amount):
                creatureList.append(self.mutate_creature(creatureList[i]))
                numCreaturesGenerated+=1
        
        print("Created %d mutated creatures"%numCreaturesGenerated)

        while len(creatureList) < 1000:
            creatureList.append(next(self.creature_factory))
            numCreaturesGenerated+=1
        print("Created %d new creatures total"% numCreaturesGenerated)

    def _generate_new_generation(self, creatureList):

        print("Simulation complete, interpreting results and generating next generation")
        best_result = max(creatureList)
        self.environment.set_creature(best_result[1])


        print("The best creature travelled %.2f pixels, it has %d nodes and %d muscles."%(best_result[0][0], len(best_result[1].nodes), len(best_result[1].muscles)))

        outList = self._cull_creatures(creatureList)

        self._reproduce_creatures(outList)

        self.creature_list = outList

        #this line actually has to be at the end because the callback is not called on the main thread
        self.simulation_in_progress = False