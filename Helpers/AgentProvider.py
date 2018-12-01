import random

from Entity.Agent import Agent


def provide_agent(number, player_target, obstacles):
    enemies = []
    for iterator in range(number):
        x_obj = 200 * random.randint(0, 5) + random.randint(0, 20)
        y_obj = 200 * random.randint(0, 3) + random.randint(0, 20)
        enemy = Agent((x_obj, y_obj), 6, player_target, obstacles, 150)
        enemies.append(enemy)

    for enemy in enemies:
        enemy.add_neighbours(enemies)
        enemy.neighbours.remove(enemy)

    return enemies
