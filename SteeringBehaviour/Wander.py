import random

from Entity.Player import *
from SteeringBehaviour.Seek import seek


class Wander:

    def __init__(self):
        self.wander_radius = 1
        self.wander_distance = 1.5
        self.wander_jitter = 0.5
        self.wander_target = pg.math.Vector2()

    def wander(self, wanderer):
        self.wander_target += pg.math.Vector2(random.uniform(-1, 1) * self.wander_jitter,
                                              random.uniform(-1, 1) * self.wander_jitter)
        self.wander_target.normalize()
        self.wander_target *= self.wander_radius
        print(self.wander_target)
        new_target = add(self.wander_target, [coord * self.wander_distance for coord in normalize(wanderer.vel)])
        print(new_target)
        return [c * wanderer.speed for c in normalize(new_target)]

