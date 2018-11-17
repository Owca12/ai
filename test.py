import random
from Entity.Agent import *
from Entity.Player import *


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
        radius = random.randint(5, 50)

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


def main():
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    player = Player((320, 240), 2)
    enemy = Agent((300, 200), 1)
    all_sprites.add(player, enemy)

    all_objects = pg.sprite.Group()
    PlaceObjects(20, all_objects)

    done = False
    while not done:
        player.rotate_player()
        # enemy.apply_pursuit(player)
        # enemy.apply_seek(player.pos)
        enemy.apply_wander()
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