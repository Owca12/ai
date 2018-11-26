import random
from Entity.Agent import *
from Entity.Player import *
from Entity.NonMovableObject import *


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 200, 200)


def main():
    screen = pg.display.set_mode((1800, 800))
    laser_size = 0
    end_point_position = [0, 0]
    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    all_obstacles = pg.sprite.Group()
    all_obstacles_list = []
    for i in range(20):
        x_obj = 200 * random.randint(1, 8) + random.randint(0, 20)
        y_obj = 200 * random.randint(1, 5) + random.randint(0, 20)
        radius = random.randint(25, 75)
        map_obj = NonMovableObject((x_obj, y_obj), radius)
        all_obstacles_list.append(map_obj)
        all_obstacles.add(map_obj)


    player = Player((120, 240), 4)
    enemy1 = Agent((50, 50), 8, player, all_obstacles_list, 150)
    enemy2 = Agent((1000, 50), 8, player, all_obstacles_list, 150)
    enemy3 = Agent((50, 500), 8, player, all_obstacles_list, 150)
    enemy4 = Agent((1800, 500), 8, player, all_obstacles_list, 150)
    enemy5 = Agent((1800, 700), 8, player, all_obstacles_list, 150)
    enemy1.add_neighbours([enemy2, enemy3, enemy4, enemy5])
    enemy2.add_neighbours([enemy1, enemy3, enemy4, enemy5])
    enemy3.add_neighbours([enemy1, enemy2, enemy4, enemy5])
    enemy4.add_neighbours([enemy1, enemy2, enemy3, enemy5])
    enemy5.add_neighbours([enemy1, enemy2, enemy3, enemy4])
    enemies = [enemy4, enemy3, enemy1, enemy2, enemy5]
    for enemy in enemies:
        enemy.on_cohesion()
        enemy.on_persuit()
        enemy.on_wander()
        enemy.on_avoid()
        enemy.on_hide()
        all_sprites.add(enemy)

    all_sprites.add(player)
    done = False

    while not done:
        player.rotate_player()
        for enemy in enemies:
            enemy.apply_steering_force()
            enemy.pack_is_ready()
            if enemy.pos.x < 0 or enemy.pos.x > 1800:
                enemy.vel.x = -enemy.vel.x
            if enemy.pos.y < 0 or enemy.pos.y > 800:
                enemy.vel.y = -enemy.vel.y



        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            player.do_dodge(1)
        elif keys[pg.K_RIGHT]:
            player.do_dodge(0)
        elif keys[pg.K_UP]:
            player.player_do_move()
        elif pg.mouse.get_pressed()[0]:
            end_point_position = player.shoot_laser(enemies)
            laser_size = 5

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
        all_obstacles.draw(screen)
        if laser_size > 0:
            pg.draw.line(screen, GREEN, player.pos, end_point_position, laser_size)
        pg.display.flip()
        clock.tick(30)
        laser_size = 0


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()