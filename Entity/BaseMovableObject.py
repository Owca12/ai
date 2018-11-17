from Helpers.vectorCalculator import *


class BaseMovableObject(pg.sprite.Sprite):

    def __init__(self, sprite, vec_pos, speed):
        super().__init__()
        self.image = sprite
        self.orig_img = self.image
        self.rect = self.image.get_rect(center=vec_pos)
        self.pos = pg.math.Vector2(vec_pos)
        self.vel = pg.math.Vector2(0, 0)
        self.speed = speed
        self.face_target = pg.math.Vector2(0, 0)

    def update(self):
        _, angle = (self.face_target - self.pos).as_polar()
        self.image = pg.transform.rotozoom(self.orig_img, -angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.pos += self.vel
        self.rect.center = self.pos

    def rotate(self, face_target):
        self.face_target = face_target

    def do_move(self, target_position):
        target_vector = sub(target_position, self.pos)
        move_vector = [c * self.speed for c in normalize(target_vector)]
        self.vel = move_vector

    def stop(self):
        self.vel = pg.math.Vector2(0, 0)


