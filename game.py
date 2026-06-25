import pygame
import random
import pytmx
import pyscroll
from pytmx.util_pygame import load_pygame

from player import Player


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((800, 415))
        pygame.display.set_caption("The Virtual Border")

        self.font = pygame.font.SysFont("Arial", 40)
        self.big_font = pygame.font.SysFont("Arial", 80)

        # ======================
        # STATES
        # ======================
        self.state = "menu"

        self.selected = 0
        self.options = [
            "Start Game",
            "Settings",
            "Quit"
        ]

        # ======================
        # SETTINGS
        # ======================
        self.volume = 50

        self.controls = {
            "up": pygame.K_UP,
            "down": pygame.K_DOWN,
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT
        }

        self.settings_selected = 0
        self.waiting_key = None

        self.settings_options = [
            "Volume",
            "Move Up",
            "Move Down",
            "Move Left",
            "Move Right",
            "Back"
        ]

        # ======================
        # TMX MAP
        # ======================
        tmx_data = load_pygame("assets/desertv70.tmx")

        map_data = pyscroll.data.TiledMapData(tmx_data)

        map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data,
            self.screen.get_size()
        )
        #généner un joueur
        player_position = tmx_data.get_object_by_name("player_spawn")
        self.player = Player(player_position.x, player_position.y)
        self.player._layer = 2

        #définir une liste contenant les rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:

            print("DEBUG OBJ:", obj.name, "| type:", obj.type, "| class:", getattr(obj, "class_", None))

    # ✔️ accepte plusieurs cas possibles
            if obj.type == "collision" or getattr(obj, "class_", None) == "collision":

                rect = pygame.Rect(
                    obj.x,
                    obj.y,
                    obj.width,
                    obj.height
                )

                self.walls.append(rect)

        print("WALLS TOTAL =", len(self.walls))  # debug

  

        #dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer)

        self.group.add(self.player)

        # ======================
        # BINARY RAIN
        # ======================
        self.binary = []

        for i in range(80):
            self.binary.append([
                random.randint(0, 1500),
                random.randint(-1000, 1000),
                random.choice(["0", "1"])
            ])

        # ======================
        # GLITCH
        # ======================
        self.glitch_timer = 0

        # ======================
        # LOGO
        # ======================
        self.logo_text = self.big_font.render(
            "THE",
            True,
            (0, 255, 120)
        )

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

            text = self.font.render(
                b[2],
                True,
                (0, 180, 0)
            )

            self.screen.blit(
                text,
                (b[0], b[1])
            )

    # ======================
    # GLITCH
    # ======================
    def trigger_glitch(self):

        if random.randint(0, 200) == 0:
            self.glitch_timer = 10

        if self.glitch_timer > 0:

            self.glitch_timer -= 1

            return (
                random.randint(-10, 10),
                random.randint(-10, 10)
            )

        return (0, 0)

    # ======================
    # PLAYER INPUT
    # ======================
    def handle_input(self):

        old_position = self.player.position.copy()

        pressed = pygame.key.get_pressed()

        if pressed[self.controls["up"]]:
            self.player.move_up()

        elif pressed[self.controls["down"]]:
            self.player.move_down()

        elif pressed[self.controls["left"]]:
            self.player.move_left()

        elif pressed[self.controls["right"]]:
            self.player.move_right()

        self.player.update()

        for wall in self.walls:
            if self.player.rect.colliderect(wall):
                self.player.position = old_position
                self.player.update()
                break

    def update(self):
        self.group.update()

        # verification collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    # ======================
    # MAIN LOOP
    # ======================
    def run(self):

        clock = pygame.time.Clock()
        running = True

        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:

                    # ======================
                    # MENU
                    # ======================
                    if self.state == "menu":

                        if event.key == pygame.K_UP:
                            self.selected = (
                                self.selected - 1
                            ) % len(self.options)

                        elif event.key == pygame.K_DOWN:
                            self.selected = (
                                self.selected + 1
                            ) % len(self.options)

                        elif event.key == pygame.K_RETURN:

                            if self.selected == 0:
                                self.state = "map"

                            elif self.selected == 1:
                                self.state = "settings"

                            elif self.selected == 2:
                                running = False

                    # ======================
                    # SETTINGS
                    # ======================
                    elif self.state == "settings":

                        if self.waiting_key:

                            self.controls[
                                self.waiting_key
                            ] = event.key

                            self.waiting_key = None

                        else:

                            if event.key == pygame.K_UP:

                                self.settings_selected = (
                                    self.settings_selected - 1
                                ) % len(
                                    self.settings_options
                                )

                            elif event.key == pygame.K_DOWN:

                                self.settings_selected = (
                                    self.settings_selected + 1
                                ) % len(
                                    self.settings_options
                                )

                            elif event.key == pygame.K_LEFT:

                                if self.settings_selected == 0:

                                    self.volume = max(
                                        0,
                                        self.volume - 5
                                    )

                                    pygame.mixer.music.set_volume(
                                        self.volume / 100
                                    )

                            elif event.key == pygame.K_RIGHT:

                                if self.settings_selected == 0:

                                    self.volume = min(
                                        100,
                                        self.volume + 5
                                    )

                                    pygame.mixer.music.set_volume(
                                        self.volume / 100
                                    )

                            elif event.key == pygame.K_RETURN:

                                if self.settings_selected == 1:
                                    self.waiting_key = "up"

                                elif self.settings_selected == 2:
                                    self.waiting_key = "down"

                                elif self.settings_selected == 3:
                                    self.waiting_key = "left"

                                elif self.settings_selected == 4:
                                    self.waiting_key = "right"

                                elif self.settings_selected == 5:
                                    self.state = "menu"

                            elif event.key == pygame.K_ESCAPE:
                                self.state = "menu"

                    # ======================
                    # MAP
                    # ======================
                    elif self.state == "map":

                        if event.key == pygame.K_ESCAPE:
                            self.state = "menu"

            self.screen.fill((0, 0, 0))

            # ======================
            # MENU
            # ======================
            if self.state == "menu":

                self.update_binary()

                gx, gy = self.trigger_glitch()

                self.draw_binary()

                center_x = self.screen.get_width() // 2

                logo_rect = self.logo_text.get_rect(
                    center=(center_x + gx, 70 + gy)
                )

                self.screen.blit(
                    self.logo_text,
                    logo_rect
                )

                title = self.big_font.render(
                    "VIRTUAL BORDER",
                    True,
                    (0, 200, 255)
                )

                title_rect = title.get_rect(
                    center=(center_x + gx, 150 + gy)
                )

                self.screen.blit(
                    title,
                    title_rect
                )

                for i, option in enumerate(self.options):

                    color = (
                        (0, 255, 120)
                        if i == self.selected
                        else (255, 255, 255)
                    )

                    text = self.font.render(
                        option,
                        True,
                        color
                    )

                    text_rect = text.get_rect(
                        center=(
                            center_x,
                            250 + i * 50
                        )
                    )

                    self.screen.blit(
                        text,
                        text_rect
                    )

            # ======================
            # SETTINGS
            # ======================
            elif self.state == "settings":

                title = self.big_font.render(
                    "SETTINGS",
                    True,
                    (0, 200, 255)
                )

                self.screen.blit(
                    title,
                    (150, 40)
                )

                for i, option in enumerate(
                    self.settings_options
                ):

                    color = (
                        (0, 255, 120)
                        if i == self.settings_selected
                        else (255, 255, 255)
                    )

                    if option == "Volume":

                        text = (
                            f"Volume : {self.volume}"
                        )

                    elif option == "Move Up":

                        text = (
                            "Up : "
                            + pygame.key.name(
                                self.controls["up"]
                            )
                        )

                    elif option == "Move Down":

                        text = (
                            "Down : "
                            + pygame.key.name(
                                self.controls["down"]
                            )
                        )

                    elif option == "Move Left":

                        text = (
                            "Left : "
                            + pygame.key.name(
                                self.controls["left"]
                            )
                        )

                    elif option == "Move Right":

                        text = (
                            "Right : "
                            + pygame.key.name(
                                self.controls["right"]
                            )
                        )

                    else:
                        text = option

                    render = self.font.render(
                        text,
                        True,
                        color
                    )

                    self.screen.blit(
                        render,
                        (100, 140 + i * 45)
                    )

                if self.waiting_key:

                    waiting = self.font.render(
                        "Press a key...",
                        True,
                        (255, 80, 80)
                    )

                    self.screen.blit(
                        waiting,
                        (220, 380)
                    )

            # ======================
            # MAP
            # ======================
            elif self.state == "map":
                
                self.handle_input()

                self.update()

                self.group.center(
                    self.player.rect.center
                )

                self.group.draw(
                    self.screen
                )

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
