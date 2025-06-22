import sys
import pygame
import os
import random
import argparse

# Agregar el directorio raíz del proyecto al path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_dir)

import utilities.generic as util

parser = argparse.ArgumentParser()
parser.add_argument("user_directory", help="Directorio del usuario")
parser.add_argument("privilege", help="Nivel de privilegio del usuario")
args = parser.parse_args()

user_directory = args.user_directory
privilege = args.privilege

pygame.init()

# Constantes globales
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [
    pygame.image.load(util.get_app_asset_path("lizard", "Lizard", "LizardRun1.png")),
    pygame.image.load(util.get_app_asset_path("lizard", "Lizard", "LizardRun2.png")),
]

JUMPING = pygame.image.load(util.get_app_asset_path("lizard", "Lizard", "LizardJump.png"))

DUCKING = [
    pygame.image.load(util.get_app_asset_path("lizard", "Lizard", "LizardDuck1.png")),
    pygame.image.load(util.get_app_asset_path("lizard", "Lizard", "LizardDuck2.png")),
]

DEAD = pygame.image.load(util.get_app_asset_path("lizard", "Lizard", "LizardDead.png"))

SMALL_CACTUS = [
    pygame.image.load(util.get_app_asset_path("lizard", "Cactus", "SmallCactus1.png")),
    pygame.image.load(util.get_app_asset_path("lizard", "Cactus", "SmallCactus2.png")),
    pygame.image.load(util.get_app_asset_path("lizard", "Cactus", "SmallCactus3.png")),
]

LARGE_CACTUS = [
    pygame.image.load(util.get_app_asset_path("lizard", "Cactus", "LargeCactus1.png")),
    pygame.image.load(util.get_app_asset_path("lizard", "Cactus", "LargeCactus2.png")),
    pygame.image.load(util.get_app_asset_path("lizard", "Cactus", "LargeCactus3.png")),
]

BIRD = [
    pygame.image.load(util.get_app_asset_path("lizard", "Bird", "Bird1.png")),
    pygame.image.load(util.get_app_asset_path("lizard", "Bird", "Bird2.png")),
]

CLOUD = pygame.image.load(util.get_app_asset_path("lizard", "Other", "Cloud.png"))

BACKGROUND = pygame.image.load(util.get_app_asset_path("lizard", "Other", "Track.png"))

START = pygame.image.load(util.get_app_asset_path("lizard", "Lizard", "LizardStart.png"))

GAME_OVER = pygame.image.load(util.get_app_asset_path("lizard", "Other", "GameOver.png"))

POINT_EFFECT = pygame.mixer.Sound(
    util.get_app_sound_path("lizard", "points.wav")
)

HUGE_POINT_EFFECT = pygame.mixer.Sound(
    util.get_app_sound_path("lizard", "huge_points.wav")
)

DEAD_EFFECT = pygame.mixer.Sound(util.get_app_sound_path("lizard", "death.wav"))

SOUNDTRACK = pygame.mixer.Sound(util.get_app_sound_path("lizard", "comedy-detective.wav"))

JUMP_EFFECT = pygame.mixer.Sound(
    util.get_app_sound_path("lizard", "jump.wav")
)

pygame.display.set_icon(
    pygame.image.load(util.get_app_asset_path("lizard", "Lizard", "LizardJump.png"))
)
pygame.display.set_caption("Lizard")


class Lizard:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.lizard_duck = False
        self.lizard_run = True
        self.lizard_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = RUNNING[0]
        self.lizard_rect = self.image.get_rect()
        self.lizard_rect.x = self.X_POS
        self.lizard_rect.y = self.Y_POS

    def update(self, userInput):
        if self.lizard_run:
            self.run()
        if self.lizard_duck:
            self.duck()
        if self.lizard_jump:
            self.jump()

        if self.step_index >= 20:
            self.step_index = 0

        if userInput[pygame.K_DOWN]:
            self.lizard_duck = True
            self.lizard_run = False
        elif userInput[pygame.K_UP] or userInput[pygame.K_SPACE] and not self.lizard_jump:
            self.lizard_duck = False
            self.lizard_run = False
            self.lizard_jump = True
        elif not (self.lizard_jump or userInput[pygame.K_DOWN]):
            self.lizard_duck = False
            self.lizard_run = True
            self.lizard_jump = False

    def duck(self):
        self.image = DUCKING[self.step_index // 10]

        if self.lizard_jump:
            self.jump_vel = self.JUMP_VEL
            self.lizard_jump = False

        self.lizard_rect = self.image.get_rect()
        self.lizard_rect.y = self.Y_POS_DUCK
        self.lizard_rect.x = self.X_POS
        self.step_index += 1

    def run(self):
        self.image = RUNNING[self.step_index // 10]
        self.lizard_rect = self.image.get_rect()
        self.lizard_rect.y = self.Y_POS
        self.lizard_rect.x = self.X_POS
        self.step_index += 1

    def jump(self):
        self.image = JUMPING
        if self.lizard_jump:
            self.lizard_rect.y -= self.jump_vel * 2
            self.jump_vel -= 0.4

        if self.jump_vel < -self.JUMP_VEL:
            self.lizard_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.lizard_rect.x, self.lizard_rect.y))


class Cloud:
    def __init__(self) -> None:
        self.x = SCREEN_WIDTH + random.randint(800, 2800)
        self.y = random.randint(50, 200)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed / 2
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(500, 2500)
            self.y = random.randint(50, 200)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type) -> None:
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed / 2
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        offset_x = 8
        SCREEN.blit(self.image[self.type], (self.rect.x - offset_x, self.rect.y))


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice([200, 270, 330])
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 19:
            self.index = 0

        SCREEN.blit(self.image[self.index // 10], (self.rect.x - 8, self.rect.y))
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, clouds
    run = True
    SOUNDTRACK.play(-1)
    clock = pygame.time.Clock()
    player = Lizard()

    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.SysFont("microsoftphagspa.ttf", 30)
    obstacles = []
    clouds = []
    death_count = 0

    def score():
        global points, game_speed
        points += 0.5
        if points % 200 == 0 and points < 4000:
            game_speed += 2
        if points % 500 == 0:
            POINT_EFFECT.play() if points % 2000 != 0 else HUGE_POINT_EFFECT.play()
            if points >= 4000 and points < 8000:
                game_speed += 1
        if points % 2000 == 0 and points >= 8000:
            game_speed += 1

        text = font.render("Puntaje: " + str(round(points)), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BACKGROUND.get_width()
        SCREEN.blit(BACKGROUND, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BACKGROUND, (image_width + x_pos_bg, y_pos_bg))

        if x_pos_bg <= -image_width:
            SCREEN.blit(BACKGROUND, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed / 2

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        SCREEN.fill((255, 255, 255))

        if clouds == []:
            for _ in range(2):
                clouds.append(Cloud())

        for cloud in clouds:
            cloud.draw(SCREEN)
            cloud.update()

        userInput = pygame.key.get_pressed()
        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()

            if player.lizard_rect.colliderect(obstacle.rect):
                if not player.lizard_jump and not player.lizard_run:
                    player.lizard_rect.y = player.Y_POS
                    player.lizard_rect.x = player.X_POS

                SOUNDTRACK.stop()
                DEAD_EFFECT.play()
                death_count += 1
                menu(death_count)

        background()
        score()

        pygame.display.update()
        clock.tick(60)


def menu(death_count, run=True):
    global points
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.SysFont("microsoftphagspa.ttf", 30)
        bold_font = pygame.font.SysFont("microsoftphagspa.ttf", 40, bold=True)

        if death_count == 0:
            welcome = bold_font.render(("LIZARD"), True, (0, 0, 0))
            welcomeRect = welcome.get_rect()
            welcomeRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
            SCREEN.blit(welcome, welcomeRect)
            text = font.render("Presiona cualquier tecla para empezar", True, (0, 0, 0))

        elif death_count > 0:
            text = font.render(
                "Presiona cualquier tecla para reiniciar", True, (0, 0, 0)
            )
            SCREEN.blit(GAME_OVER, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 - 200))
            score = bold_font.render(
                ("Tu puntaje fue de " + str(int(points)) + " puntos"), True, (0, 0, 0)
            )
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)

        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        if death_count == 0:
            SCREEN.blit(text, textRect)
            SCREEN.blit(START, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50))
        else:
            SCREEN.blit(text, textRect)
            SCREEN.blit(DEAD, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)
