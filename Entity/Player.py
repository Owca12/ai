from Entity.BaseMovableObject import *
from Entity.uiElements import Laser


class Player(BaseMovableObject):
    def __init__(self, vec_pos, speed, screen, player_hp):
        self.player_hp = player_hp
        self.image = pg.Surface((50, 40), pg.SRCALPHA)
        pg.draw.polygon(
            self.image,
            pg.Color('white'),
            ((1, 1), (49, 20), (1, 39)))
        super().__init__(self.image, vec_pos, speed)
        self.laser = Laser(screen)
        self.attack_cool_down = 0

    def rotate_player(self):
        self.rotate(pg.mouse.get_pos())

    def refresh_cooldown(self, clock):
        if self.attack_cool_down > 0:
            self.attack_cool_down -= clock.get_time()

    def player_do_move(self):
        self.do_move(pg.mouse.get_pos())

    def do_dodge(self, direction):
        face_vector = sub(pg.mouse.get_pos(), self.pos)
        norm_face_vector = normalize(face_vector)
        target_vector = pg.math.Vector2()
        target_vector.x = norm_face_vector[0]
        target_vector.y = norm_face_vector[1]
        if direction is 0:
            move_vector = [c * self.speed for c in normalize(perpendicular_vector(target_vector))]
        else:
            move_vector = [c * self.speed for c in normalize(-perpendicular_vector(target_vector))]
        self.vel = move_vector

    def shoot_laser(self, enemies):
        self.attack_cool_down = 500
        # for enemy in enemies:
        #     angle = dot(normalize(self.laser.head - self.pos), normalize(enemy.pos - self.pos))
        #     if distance(self.pos, enemy.pos) < self.laser.distance and 1.0 > angle > 0.95:
        #         return enemy
        return self.laser.shoot(self, enemies)

    def animate_laser(self):
        self.laser.animate(self)
