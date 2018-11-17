from SteeringBehaviour.Pursuit import *
from SteeringBehaviour.Wander import Wander


class Agent(BaseMovableObject):
    def __init__(self, vec_pos, speed):
        self.image = pg.Surface((2 * 30, 2 * 30), pg.SRCALPHA)
        pg.draw.circle(
            self.image,
            pg.Color('red'),
            (30, 30), 30, 0)
        BaseMovableObject.__init__(self, self.image, vec_pos, speed)
        self.vel = pg.math.Vector2(1, 1)

    def apply_pursuit(self, target):
        self.vel = pursuit(target, self)
        self.rotate(normalize(self.vel))

    def apply_seek(self, target):
        self.vel = seek(self, target)
        self.rotate(normalize(self.vel))

    def apply_wander(self):
        wander = Wander()
        self.vel = wander.wander(self)
        self.rotate(normalize(self.vel))


