from vectorCalculator import *
import math


class BaseMovableObject(pg.sprite.Sprite):

    def __init__(self, sprite, vec_pos, speed):
        super().__init__()
        self.image = sprite
        self.orig_img = self.image
        self.rect = self.image.get_rect(center=vec_pos)
        self.pos = pg.math.Vector2(vec_pos)
        self.vel = pg.math.Vector2(0, 0)
        self.speed = speed
        self.angle = 0
        self.vector = 0
        self.perception_point_one = pg.math.Vector2(0, 0)
        self.perception_point_two = pg.math.Vector2(0, 0)

    def update(self):
        self.image = pg.transform.rotozoom(self.orig_img, -self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.pos += self.vel
        self.rect.center = self.pos

    def rotate(self, face_target):
        _, self.angle = (face_target-self.pos).as_polar()

    def do_move(self, target_position):
        target_vector = sub(target_position, self.pos)
        move_vector = [c * self.speed for c in normalize(target_vector)]
        self.vel = move_vector

    def stop(self):
        self.vel = pg.math.Vector2(0, 0)

    def search_range(self, range, distacne):
        # Perception range and distance
        perception_range = range
        perception_distance = distacne
        # Perception points - testing these for potential collisions
        perception_point_one_x = perception_distance * math.cos(
            math.radians(self.angle + perception_range))
        perception_point_one_y = perception_distance * math.sin(
            math.radians(self.angle + perception_range))
        self.perception_point_one = pg.math.Vector2(self.pos[0] + perception_point_one_x,
                                                    self.pos[1] + perception_point_one_y)

        perception_point_two_x = perception_distance * math.cos(
            math.radians(self.angle - perception_range))
        perception_point_two_y = perception_distance * math.sin(
            math.radians(self.angle - perception_range))
        self.perception_point_two = pg.math.Vector2(self.pos[0] + perception_point_two_x,
                                                    self.pos[1] + perception_point_two_y)

    def do_move_avoid_obstacle(self, target_position, obstacle_position, is_collision, direction):
        target_vector = sub(target_position, self.pos)
        if is_collision == True:
            #Force vector pushing the object away from the obstacle according to position
            obstacle_vector_one = normalize(sub(self.perception_point_one, obstacle_position))
            obstacle_vector_two = normalize(sub(self.perception_point_two, obstacle_position))
            # Force vector pushing the object perpendicullary away from the obstacle
            force_vector_two = normalize(perpendicular_vector((sub(target_position, self.pos))))
            force_vector_one = normalize(rev_perpendicular_vector((sub(target_position, self.pos))))

            if direction == 0:
                move_vector = [c * self.speed for c in (add(force_vector_one,obstacle_vector_one))]

            elif direction == 1:
                move_vector = [c * self.speed for c in (add(force_vector_two,obstacle_vector_two))]

        elif is_collision == False:
            move_vector = [c * self.speed for c in normalize(target_vector)]

        self.vel = move_vector

















        #print("avoiding")
        # elif math.hypot(obstacle_position[0] - self.perception_point_two[0],
        #               obstacle_position[1] - self.perception_point_two[1]) < obstacle_radius:
        #     move_vector = [c * self.speed for c in normalize(add(target_vector, self.force_vector_two))]
        #     self.angle = 1.01 * self.angle
        #     print("avoiding")
        #
        # self.vel = move_vector
        # target_vector = sub(target_position, self.pos)
        # obstacle_vector = sub(obstacle_position, self.pos)
        # move_vector = [c * self.speed for c in normalize(add( target_vector, obstacle_vector))]
        # if direction == 1:
        #     self.angle = 0.5 * self.angle
        #     self.vel = move_vector
        # else:
        #     self.angle = 1.1 * self.angle
        #     self.vel = move_vector


