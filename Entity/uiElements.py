from Helpers.vectorCalculator import *
GREEN = (0, 255, 0)


class HpBar(pg.sprite.Sprite):
    def __init__(self, pos, player):
        super().__init__()
        self.image = pg.Surface((300, 50), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
        self.orig_img = self.image
        self.current_hp = player.player_hp
        self.player_max_hp = player.player_hp

    def refresh_player_hp(self, player_hp):
        self.current_hp = player_hp
        if self.player_max_hp - self.current_hp >= 0:
            self.image = pg.Surface(((self.player_max_hp - self.current_hp)*30, 50), pg.SRCALPHA)
            self.rect = self.image.get_rect(center=self.pos)
            self.orig_img = self.image
            pg.draw.rect(
                self.image,
                pg.Color('red'),
                (0, 0, (self.player_max_hp - self.current_hp)*30, 50))

    def set_hp_bar(self, player_hp):
        self.current_hp = player_hp
        self.image = pg.Surface((self.current_hp*30, 50), pg.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)
        self.orig_img = self.image
        pg.draw.rect(
            self.image,
            pg.Color('green'),
            (0, 0, self.current_hp*30, 50))


class Laser(pg.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.head = pg.math.Vector2()
        self.distance = 300
        self.offset = 5
        self.animate_laser = False
        self.last_point = [0, 0]

    def shoot(self, player, enemies):
        self.last_point = add(player.pos, [c * self.distance for c in normalize(sub(player.face_target, player.pos))])
        dir_vec = normalize(sub(player.face_target, player.pos))
        for iter in range(60):
            point = add(player.pos, [c * iter * self.offset for c in dir_vec])
            for enemy in enemies:
                if distance(point, enemy.pos) < 20:
                    self.last_point = point
                    return enemy

    def animate(self, player):
        if self.animate_laser:
            pg.draw.line(
                self.screen, GREEN, player.pos, self.last_point, 5)
