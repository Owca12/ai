from Entity.BaseMovableObject import *


class Player(BaseMovableObject):
    def __init__(self, vec_pos, speed):
        self.image = pg.Surface((50, 40), pg.SRCALPHA)
        pg.draw.polygon(
            self.image,
            pg.Color('white'),
            ((1, 1), (49, 20), (1, 39)))
        super().__init__(self.image, vec_pos, speed)

    def rotate_player(self):
        self.rotate(pg.mouse.get_pos())

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
        end_point_position = [c * 150 for c in normalize(sub(pg.mouse.get_pos(), self.pos))]
        end_point_position = add(end_point_position, self.pos)
        for enemy in enemies:
            if distance(enemy.pos, self.pos) < distance(end_point_position, self.pos):
                enemy.pos = pg.math.Vector2(1000, 1000)
                enemy.speed = [0, 0]
                enemies.remove(enemy)

        return end_point_position