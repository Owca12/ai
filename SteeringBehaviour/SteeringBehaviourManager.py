import random
from Helpers.vectorCalculator import *

from SteeringBehaviour.GroupBehaviour import GroupBehaviour
from SteeringBehaviour.SingleBehaviour import SingleBehaviour
from SteeringBehaviour.Wander import Wander


class SteeringBehaviourManager:
    def __init__(self):
        self.behaviours = []
        self.multiWander = 1
        self.multiCohesion = 0.1
        self.multiPersuit = 0.1

    def truncate(self, vector, max_magnitude):
        current = magnitude(vector)
        if current > max_magnitude:
            vector = [c * max_magnitude for c in normalize(vector)]
        return vector

    def accumulate_force(self, agent, total_force, force):
        force_so_far = magnitude(total_force)
        force_remaining = agent.speed - force_so_far
        if force_remaining <= 0:
            return False
        force_to_add = magnitude(force)
        if force_to_add < force_remaining:
            total_force += force
        else:
            total_force += self.truncate(force, force_remaining)
        return True

    def enable(self, behaviour):
        self.behaviours.append(behaviour)

    def calculate_dithered(self, agent):
        steering_force = pg.math.Vector2(0, 0)
        if "Wander" in self.behaviours:
            new_force = [c * self.multiWander for c in Wander(agent).wander()]
            if not self.accumulate_force(agent, steering_force, new_force):
                return steering_force
        if "Cohesion" in self.behaviours:
            new_force = [c * self.multiCohesion for c in GroupBehaviour(agent).cohesion(agent.neighbours)]
            if not self.accumulate_force(agent, steering_force, new_force):
                return steering_force
        if "Persuit" in self.behaviours:
            new_force = [c * self.multiPersuit for c in SingleBehaviour(agent).pursuit(agent.target)]
            if not self.accumulate_force(agent, steering_force, new_force):
                return steering_force
        return steering_force

    def change_dithered_probabilistic(self, behaviour, probabilistic):
        if behaviour is "Wander":
            self.prWander = probabilistic
        if behaviour is "Persuit":
            self.prPersuit = probabilistic
        if behaviour is "Cohesion":
            self.prCohesion = probabilistic
