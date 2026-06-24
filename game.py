import pygame
import random
import pytmx
import pyscroll
from pytmx.util_pygame import load_pygame

from player import Player


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((800, 415))
        pygame.display.set_caption("The Virtual Border")

        self.font = pygame.font.SysFont("Arial", 40)
        self.big_font = pygame.font.SysFont("Arial", 80)

        # STATE
        self.state = "menu"
        self.selected = 0
        self.options = ["Start Game", "Quit"]

        self.running = True

        # TMX MAP
        tmx_data = load_pygame("assets/desertv68.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, self.screen.get_size()
        )

        # PLAYER
        player_position = tmx_data.get_object_by_name("player_spawn")
        self.player = Player(player_position.x, player_position.y)

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        self.group.add(self.player)

        # BINARY RAIN
        self.binary = []
        for i in range(80):
            self.binary.append(
                [
                    random.randint(0, 1500),
                    random.randint(-1000, 1000),
                    random.choice(["0", "1"]),
                ]
            )

        # GLITCH
        self.glitch_timer = 0

        # LOGO
        self.logo_text = self.big_font.render("THE", True, (0, 255, 120))

    # ======================
    # BINARY RAIN
    # ======================
    def update_binary(self):
        for b in self.binary:
            b[1] += 6
            if b[1] > 1000:
                b[1] = -50
                b[0] = random.randint(0, 1500)

    def draw_binary(self):
        for b in self.binary:
            text = self.font.render(b[2], True, (0, 180, 0))
            self.screen.blit(text, (b[0], b[1]))

    # ======================
    # GLITCH EFFECT
    # ======================
    def trigger_glitch(self):
        if random.randint(0, 200) == 0:
            self.glitch_timer = 10

        if self.glitch_timer > 0:
            self.glitch_timer -= 1
            return random.randint(-10, 10), random.randint(-10, 10)

        return 0, 0

    # ======================
    # MAIN LOOP
    # ======================
    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()

    def run(self):

        clock = pygame.time.Clock()
        running = True

        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:

                    if self.state == "menu":

                        if event.key == pygame.K_UP:
                            self.selected = (self.selected - 1) % len(self.options)

                        if event.key == pygame.K_DOWN:
                            self.selected = (self.selected + 1) % len(self.options)

                        if event.key == pygame.K_RETURN:

                            if self.selected == 0:
                                self.state = "map"

                            elif self.selected == 1:
                                running = False

            keys = pygame.key.get_pressed()

            self.screen.fill((0, 0, 0))

            # MENU
            if self.state == "menu":

                self.update_binary()

                gx, gy = self.trigger_glitch()

                self.draw_binary()

                center_x = self.screen.get_width() // 2
                center_y = self.screen.get_height() // 2

                # LOGO
                logo_rect = self.logo_text.get_rect(center=(center_x + gx, 70 + gy))
                self.screen.blit(self.logo_text, logo_rect)

                # TITLE
                title = self.big_font.render("VIRTUAL BORDER", True, (0, 200, 255))
                title_rect = title.get_rect(center=(center_x + gx, 150 + gy))
                self.screen.blit(title, title_rect)

                # LORE
                lore = self.font.render(
                    "1 min = 1 sec | reality unstable", True, (150, 150, 150)
                )
                lore_rect = lore.get_rect(center=(center_x, 220))
                self.screen.blit(lore, lore_rect)

                # OPTIONS
                for i, option in enumerate(self.options):

                    color = (0, 255, 120) if i == self.selected else (255, 255, 255)

                    text = self.font.render(option, True, color)
                    text_rect = text.get_rect(center=(center_x, 300 + i * 50))
                    self.screen.blit(text, text_rect)

            # MAP
            elif self.state == "map":

                self.handle_input()

                self.group.update()
                self.group.center(self.player.rect.center)
                self.group.draw(self.screen)

            clock.tick(60)
            pygame.display.flip()

        pygame.quit()
