import random
import array
from BaseMovableObject import *
from vectorCalculator import *


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 200, 200)


class MapElement(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        radius = random.randint(50, 50)

        self.image = pg.Surface((2*radius, 2*radius), pg.SRCALPHA)
        pg.draw.circle(
            self.image,
            pg.Color('white'),
            (radius, radius), radius, 0)
        self.orig_img = self.image
        self.rect = self.image.get_rect(center=pos)
        self.pos = pg.math.Vector2(pos)


def PlaceObjects( obj_number , all_objects ):
    for i in range(obj_number):
        x_obj = random.randint(1, 640)
        y_obj = random.randint(1, 480)
        map_obj_i = MapElement((x_obj, y_obj))
        all_objects.add(map_obj_i)
    # map_obj_i = MapElement((320, 240))
    # all_objects.add(map_obj_i)


class Player(BaseMovableObject):
    def __init__(self, vec_pos, speed):
        self.image = pg.Surface((50, 40), pg.SRCALPHA)
        pg.draw.polygon(
            self.image,
            pg.Color('white'),
            ((1, 1), (49, 20), (1, 39)))
        BaseMovableObject.__init__(self, self.image, vec_pos, speed)

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

    def stop(self):
        self.vel = pg.math.Vector2(0, 0)


class Enemy(BaseMovableObject):
    def __init__(self, vec_pos, speed):
        self.image = pg.Surface((50, 40), pg.SRCALPHA)
        pg.draw.polygon(
            self.image,
            pg.Color('red'),
            ((1, 1), (49, 20), (1, 39)))
        BaseMovableObject.__init__(self, self.image, vec_pos, speed)

    def rotate_enemy(self, player_pos):
        self.rotate(player_pos)

    # def enemy_do_move(self, player_pos):
    #     self.do_move(player_pos)

    def enemy_do_move(self, target_position, obstacle_position, is_collision, direction):
        self.do_move_avoid_obstacle(target_position, obstacle_position, is_collision, direction)



    def stop(self):
        self.vel = pg.math.Vector2(0, 0)


    # def avoid_obstacle(self, enemy_pos, enemy_angle, obstacle_position, obstacle_radius):
    #     self.epos = enemy_pos
    #     self.eang = enemy_angle
    #     self.opos = obstacle_position
    #     self.orad = obstacle_radius
    #
    #     # 1,20    100,1 oraz 100,40 - te punkty sprawdzaj dla kolizji
    #     if (enemy_pos.x


def main():
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    player = Player((640, 0), 3)
    enemy = Enemy((0, 480), 2)
    all_sprites.add(player, enemy)

    all_objects = pg.sprite.Group()
    object_array = []
    direction = 0

    for i in range(5):
        x_obj = random.randint(1, 640)
        y_obj = random.randint(1, 480)
        map_obj = MapElement((x_obj, y_obj))
        object_array.append(map_obj.pos)
        all_objects.add(map_obj)

    #map_obj_1 = MapElement((200,200))
    #all_objects.add(map_obj_1)
    #PlaceObjects(5, all_objects)

    print(len(object_array))
    print(object_array[i][0])
    print(enemy.perception_point_one[0])

    done = False
    while not done:
        is_collision = False
        player.rotate_player()
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            player.do_dodge(1)
        elif keys[pg.K_RIGHT]:
            player.do_dodge(0)
        elif keys[pg.K_UP]:
            player.player_do_move()


        enemy.search_range(15, 40)
        for i in range (len(object_array)):
            if math.sqrt((object_array[i][0] - enemy.perception_point_one[0]) * (
                    object_array[i][0] - enemy.perception_point_one[0]) + (
                                 object_array[i][1] - enemy.perception_point_one[1]) * (
                                 object_array[i][1] - enemy.perception_point_one[1])) < 50:
                is_collision = True
                direction = 0
                break
            elif math.sqrt((object_array[i][0] - enemy.perception_point_two[0]) * (
                    object_array[i][0] - enemy.perception_point_two[0]) + (
                                 object_array[i][1] - enemy.perception_point_two[1]) * (
                                 object_array[i][1] - enemy.perception_point_two[1])) < 50:
                is_collision = True
                direction = 1
                break

        enemy.enemy_do_move(player.pos, (object_array[i][0], object_array[i][1]), is_collision, direction)
        enemy.rotate_enemy(player.pos)

            # elif math.hypot(obstacle_position[0] - self.perception_point_two[0],
            #               obstacle_position[1] - self.perception_point_two[1]) < obstacle_radius:
            #     move_vector = [c * self.speed for c in normalize(add(target_vector, self.force_vector_two))]
            #     self.angle = 1.01 * self.angle
            #     print("avoiding")


        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_DOWN or event.key == pg.K_UP:
                    player.stop()
                elif event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
                    player.stop()

        all_sprites.update()
        screen.fill((30, 30, 30))
        all_sprites.draw(screen)
        all_objects.draw(screen)
        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()