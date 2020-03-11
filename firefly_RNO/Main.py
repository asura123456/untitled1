from Swarm import Swarm
import config
import utils

def main():

    swarm = Swarm(config.ALPHA, config.ABSORPTION)
    update_brightness(swarm.fireflies)
    swarm.update_attractiveness()
    utils.description(swarm.fireflies)

    swarm.__str__()

    t = 0

    while t < config.MAX_GENERATION:
        for i, firefly in enumerate(swarm.fireflies):

            other_firefly = swarm.most_attractive[i]

            if other_firefly is not firefly and other_firefly.attractiveness > firefly.attractiveness:
                swarm.move(firefly, other_firefly)
            elif other_firefly.attractiveness == firefly.attractiveness:
                swarm.move_randomly(other_firefly)

            update_brightness(swarm.fireflies)
            swarm.update_attractiveness()

        t += 1

    print()
    swarm.__str__()

def update_brightness(fireflies):
    for firefly in fireflies:
        firefly.brightness = utils.Ackley_global_minimum(firefly)
        firefly.attractiveness = firefly.brightness

if __name__ == "__main__":
    main()
