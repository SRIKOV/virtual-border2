import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.sprite_sheet = pygame.image.load(
            "assets/player1.png"
        ).convert_alpha()

        self.animations = {
            "down1": self.get_image(0, 0),
            "down2": self.get_image(32, 0),
            "down3": self.get_image(64, 0),

            "left1": self.get_image(0, 32),
            "left2": self.get_image(32, 32),
            "left3": self.get_image(64, 32),

            "right1": self.get_image(0, 64),
            "right2": self.get_image(32, 64),
            "right3": self.get_image(64, 64),

            "up1": self.get_image(0, 96),
            "up2": self.get_image(32, 96),
            "up3": self.get_image(64, 96)
        }

        self.image = self.animations["down1"]
        self.rect = self.image.get_rect()

        self.position = [x, y]
        self.rect.topleft = self.position
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.speed = 2
        self.frame = 1
        self.direction = "down"
        
    def move_up(self):
        self.position[1] -= self.speed
        self.direction = "up"
        self.animate()

    def move_down(self):
        self.position[1] += self.speed
        self.direction = "down"
        self.animate()

    def move_left(self):
        self.position[0] -= self.speed
        self.direction = "left"
        self.animate()

    def move_right(self):
        self.position[0] += self.speed
        self.direction = "right"
        self.animate()

    def animate(self):
        self.frame += 1

        if self.frame > 3:
            self.frame = 1

        self.image = self.animations[
            f"{self.direction}{self.frame}"
        ]

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        image = pygame.Surface(
            (32, 32),
            pygame.SRCALPHA
        )

        image.blit(
            self.sprite_sheet,
            (0, 0),
            (x, y, 32, 32)
        )

        return image
