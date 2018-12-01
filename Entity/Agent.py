from SteeringBehaviour.GroupBehaviour import *
from SteeringBehaviour.SteeringBehaviourManager import *


class Agent(BaseMovableObject):
    def __init__(self, vec_pos, speed, player_target, obstacles, search_radius):
        self.image = pg.Surface((2 * 30, 2 * 30), pg.SRCALPHA)
        pg.draw.circle(
            self.image,
            pg.Color('red'),
            (20, 20), 20, 0)
        super().__init__(self.image, vec_pos, speed)
        self.neighbours = []
        self.target = player_target
        self.behaviour_manager = SteeringBehaviourManager()
        self.obstacles = obstacles
        self.search_radius = search_radius
        self.attack_cool_down = 0

    def refresh_cooldown(self, clock):
        if self.attack_cool_down > 0:
            self.attack_cool_down -= clock.get_time()

    def attack(self):
        if self.attack_cool_down <= 0:
            if self.rect.colliderect(self.target.rect):
                self.target.player_hp -= 1
                self.attack_cool_down = 3000

    def add_neighbours(self, neighbours):
        for agent in neighbours:
            self.neighbours.append(agent)

    def apply_pursuit(self):
        return SingleBehaviour(self).pursuit(self.target)

    def apply_seek(self, target):
        return SingleBehaviour(self).seek(target)

    def apply_wander(self):
        return Wander(self).wander()

    def apply_cohesion(self):
        return GroupBehaviour(self).cohesion(self.neighbours)

    def apply_all_beh(self):
        self.vel = pg.math.Vector2()
        self.vel += [c / 100 for c in self.apply_cohesion()]
        self.vel += self.apply_wander()

    def on_persuit(self):
        self.behaviour_manager.enable("Persuit")

    def on_avoid(self):
        self.behaviour_manager.enable("Avoid")

    def on_hide(self):
        self.behaviour_manager.enable("Hide")

    def on_wander(self):
        self.behaviour_manager.enable("Wander")

    def on_cohesion(self):
        self.behaviour_manager.enable("Cohesion")

    def apply_steering_force(self):
        self.vel = self.behaviour_manager.calculate_dithered(self)

    def pack_is_ready(self):
        counter = 0
        for neighbour in self.neighbours:
            if 150 > distance(self.pos, neighbour.pos):
                counter += 1
        if counter > 3:
            self.behaviour_manager.change_dithered_probabilistic("Persuit", 0.5)
            self.behaviour_manager.change_dithered_probabilistic("Wander", 0.1)
            self.behaviour_manager.change_dithered_probabilistic("Cohesion", 0)
            self.behaviour_manager.change_dithered_probabilistic("Hide", 0)



