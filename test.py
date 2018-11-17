import random
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

    def enemy_do_move(self, target_position, obstacle_position, is_collision, direction):
        self.do_move_avoid_obstacle(target_position, obstacle_position, is_collision, direction)

    def stop(self):
        self.vel = pg.math.Vector2(0, 0)


def main():
    screen = pg.display.set_mode((1024, 780))
    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    player = Player((640, 0), 3)
    enemy = Enemy((0, 480), 5)
    all_sprites.add(player, enemy)
    all_obstacles = pg.sprite.Group()
    obstacle_position_array = []
    direction = 0
    for i in range(10):
        x_obj = 200 * random.randint(1, 4)
        y_obj = 200 * random.randint(1, 3)
        map_obj = MapElement((x_obj, y_obj))
        obstacle_position_array.append(map_obj.pos)
        all_obstacles.add(map_obj)

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

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_DOWN or event.key == pg.K_UP:
                    player.stop()
                elif event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
                    player.stop()

        enemy.search_range(15, 40)
        for i in range(len(obstacle_position_array)):
            if Distance(obstacle_position_array[i], enemy.perception_point_one) < 50:
                is_collision = True
                direction = 0
                break

            elif Distance(obstacle_position_array[i], enemy.perception_point_two) < 50:
                is_collision = True
                direction = 1
                break

        enemy.enemy_do_move(player.pos, (obstacle_position_array[i][0], obstacle_position_array[i][1]), is_collision, direction)
        enemy.rotate_enemy(player.pos)

        all_sprites.update()
        screen.fill((30, 30, 30))
        all_sprites.draw(screen)
        all_obstacles.draw(screen)
        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()