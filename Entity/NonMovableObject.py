from Helpers.vectorCalculator import *
import random

class NonMovableObject(pg.sprite.Sprite):
    def __init__(self, pos, radius):
        super().__init__()
        self.radius = radius
        self.image = pg.Surface((2*radius, 2*radius), pg.SRCALPHA)
        pg.draw.circle(
            self.image,
            pg.Color('white'),
            (radius, radius), radius, 0)
        self.orig_img = self.image
        self.rect = self.image.get_rect(center=pos)
        self.pos = pg.math.Vector2(pos)

