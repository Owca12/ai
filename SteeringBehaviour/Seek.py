from Entity.Player import *


def seek(agent, target_pos):
    target_vector = sub(target_pos, agent.pos)
    move_vector = [c * agent.speed for c in normalize(target_vector)]
    return move_vector