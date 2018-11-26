import random
from SteeringBehaviour.SingleBehaviour import *
from Entity.Player import *


class Wander:

    def __init__(self, agent):
        self.agent = agent
        self.wander_radius = 0.3*agent.speed
        self.wander_distance = agent.speed
        self.wander_jitter = 0.3
        self.wander_target = pg.math.Vector2()

    def wander(self):
        self.wander_target += pg.math.Vector2(random.uniform(-1, 1) * self.wander_jitter,
                                              random.uniform(-1, 1) * self.wander_jitter)
        self.wander_target.normalize()
        self.wander_target *= self.wander_radius
        new_target = add(self.wander_target, [coord * self.wander_distance for coord in normalize(self.agent.vel)])
        return new_target

