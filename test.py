import time
from Entity.Agent import *
from Entity.Player import *
from Entity.NonMovableObject import *
from Entity.uiElements import HpBar
from Helpers.AgentProvider import provide_agent

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 200, 200)


def message(msg, screen, ):
    text = font.render(msg, True, RED)
    screen.blit(text, [640, 320])


def destroy_enemy(enemy, enemies, sprites):
    enemies.remove(enemy)
    for left_enemy in enemies:
        left_enemy.neighbours.remove(enemy)
    sprites.remove(enemy)


def main():
    screen = pg.display.set_mode((1280, 800))
    animate_laser = False
    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    all_obstacles = pg.sprite.Group()
    statistics_ui = pg.sprite.Group()
    all_obstacles_list = []
    for i in range(20):
        x_obj = 100 + 250 * random.randint(0, 5) + random.randint(0, 20)
        y_obj = 100 + 250 * random.randint(0, 2) + random.randint(0, 20)
        radius = random.randint(25, 75)
        map_obj = NonMovableObject((x_obj, y_obj), radius)
        all_obstacles_list.append(map_obj)
        all_obstacles.add(map_obj)

    player = Player((120, 240), 15, screen, 10)
    player_hp_bar = HpBar((270, 0), player)
    player_hp_bar_base = HpBar((0, 0), player)
    statistics_ui.add(player_hp_bar, player_hp_bar_base)
    enemies = provide_agent(50, player, all_obstacles_list)
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
            enemy.attack()
            player_hp_bar_base.set_hp_bar(player.player_hp)
            # player_hp_bar.refresh_player_hp(player.player_hp)
            if enemy.pos.x < 0 or enemy.pos.x > 1280:
                enemy.vel.x = -enemy.vel.x
            if enemy.pos.y < 0 or enemy.pos.y > 800:
                enemy.vel.y = -enemy.vel.y

        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            player.do_dodge(1)
        elif keys[pg.K_d]:
            player.do_dodge(0)
        elif keys[pg.K_w]:
            player.player_do_move()
        elif keys[pg.K_SPACE]:
            if player.attack_cool_down <= 0:
                killed = player.shoot_laser(enemies)
                if killed is not None:
                    destroy_enemy(killed, enemies, all_sprites)
                player.laser.animate_laser = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_s or event.key == pg.K_w:
                    player.stop()
                elif event.key == pg.K_a or event.key == pg.K_d:
                    player.stop()
                elif event.key == pg.K_SPACE:
                    player.laser.animate_laser = False

        all_sprites.update()
        statistics_ui.update()
        screen.fill((30, 30, 30))
        all_sprites.draw(screen)
        all_obstacles.draw(screen)
        statistics_ui.draw(screen)
        player.animate_laser()
        pg.display.flip()
        clock.tick(30)
        player.refresh_cooldown(clock)
        for enemy in enemies:
            enemy.refresh_cooldown(clock)
        if player.player_hp <= 0:
            done = True

    message("Game Over!", screen)
    pg.display.update()
    time.sleep(2)


if __name__ == '__main__':
    pg.init()
    font = pg.font.SysFont(None, 25)
    main()
    pg.quit()
    quit()
