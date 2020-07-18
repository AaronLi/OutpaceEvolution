import random
from evolutionary_creature import *

#NODES

#NODE POSITION
node_count_max = 5

node_xmin = 150 #farthest left
node_xmax = 300 #farthest right
node_ymin = -150 #the highest position the node can be, conversely
node_ymax = -10 # the lowest position the node can be

#NODE COUNT
min_node_count = 3
max_node_count = 4

#NODE WEIGHT
min_node_weight = 0.7
max_node_weight = 1.2

#NODE FRICTION
min_node_friction = 0.4
max_node_friction = 1


#MUSCLES

#MUSCLE CYCLE TIMING
#divide by 30 for time in seconds
#corresponds to Muscle.cycle_time
min_cycle_time = 80
max_cycle_time = 150

#MUSCLE EXTEND TIMING
#corresponds to Muscle.change_time
min_extend_time = 30
max_extend_time = 110

#MUSCLE CONTRACTION AMOUNT
#corresponds to Muscle.contracted_length
min_contraction_amount = 0.4
max_contraction_amount = 1

#MUSCLE FORCE
#corresponds to Muscle.force
min_force = 0.5
max_force = 3


def CreatureFactory():
    while True:
        nodes = []
        muscles = []

        num_nodes = random.randint(min_node_count, max_node_count)

        num_muscles=  random.randint(num_nodes-1, min(num_nodes*3-6, node_count_max))

        for i in range(num_nodes):
            nodes.append(generate_random_node())

        for i in range(num_nodes):
            for j in range(i+1, num_nodes):
                muscles.append(generate_random_muscle(nodes[i], nodes[j]))

        random.shuffle(muscles)

        while len(muscles) > num_muscles:
            del muscles[0]

        creatureOut = creature.Creature("Peewee")

        nodesWithoutMuscles = set(nodes)

        #prevents having single nodes that had all their muscles deleted, possiblity of having two pairs of nodes still exists
        for cMuscle in muscles:
            nodesWithoutMuscles.discard(cMuscle.node1)
            nodesWithoutMuscles.discard(cMuscle.node2)
        

        for cNode in nodes:
            if cNode not in nodesWithoutMuscles:
                creatureOut.addNode(cNode)

        for cMuscle in muscles:
            creatureOut.addMuscle(cMuscle)


        yield creatureOut


def generate_random_node():

    positionX = random.randint(node_xmin, node_xmax)
    positionY = random.randint(node_ymin, node_ymax)

    friction = random.random()*(max_node_friction-min_node_friction)+min_node_friction
    mass = random.random()*(max_node_weight - min_node_weight) + min_node_weight

    nodeOut = node.Node(positionX, positionY, mass, friction)

    return nodeOut

def generate_random_muscle(node1, node2):

    cycleTime = random.randint(min_cycle_time, max_cycle_time)

    extendTime = random.randint(min(min_extend_time, cycleTime - 40), min(cycleTime-20, max_extend_time))


    contractionRange = max_contraction_amount - min_contraction_amount

    contractionAmount = random.random()*contractionRange + min_contraction_amount

    forceRange = max_force - min_force

    forceAmount = random.random() * forceRange + min_force

    muscleOut = muscle.Muscle(node1, node2, forceAmount, extendTime, cycleTime, contractionAmount)

    return muscleOut