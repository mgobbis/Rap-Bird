import pygame
import random
import sys
import os

pygame.init()


SCREEN_WIDTH, SCREEN_HEIGHT = 1278, 1111
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Multiplayer")


WHITE, RED, BLUE, GREEN, BLACK = (255,255,255), (255,0,0), (0,0,255), (0,255,0), (0,0,0)


ASSETS_DIR = "assets"
bg_image = pygame.image.load(os.path.join(ASSETS_DIR, "start.png"))
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

bg_game_image = pygame.image.load(os.path.join(ASSETS_DIR, "game_bg.png")).convert()
bg_game_image = pygame.transform.scale(bg_game_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

start_button_img = pygame.image.load(os.path.join(ASSETS_DIR, "start_button.png"))
start_button_img = pygame.transform.scale(start_button_img, (693, 360))
start_button_rect = start_button_img.get_rect(center=(634, 800))

red_win_img = pygame.image.load(os.path.join(ASSETS_DIR, "red_win.png"))
red_win_img = pygame.transform.scale(red_win_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

blue_win_img = pygame.image.load(os.path.join(ASSETS_DIR, "blue_win.png"))
blue_win_img = pygame.transform.scale(blue_win_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

restart_button_img = pygame.image.load(os.path.join(ASSETS_DIR, "restart_button.png"))
restart_button_img = pygame.transform.scale(restart_button_img, (450, 225))
restart_button_rect = restart_button_img.get_rect(center=(1000, 943))


bird_image_red_open = pygame.image.load(os.path.join(ASSETS_DIR, "red_bird_open.png")).convert_alpha()
bird_image_red_open = pygame.transform.scale(bird_image_red_open, (150, 100))

bird_image_red_closed = pygame.image.load(os.path.join(ASSETS_DIR, "red_bird_closed.png")).convert_alpha()
bird_image_red_closed = pygame.transform.scale(bird_image_red_closed, (150, 100))

bird_image_blue = pygame.image.load(os.path.join(ASSETS_DIR, "blue_bird_open.png")).convert_alpha()
bird_image_blue = pygame.transform.scale(bird_image_blue, (150, 100))

bird_image_blue_closed = pygame.image.load(os.path.join(ASSETS_DIR, "blue_bird_closed.png")).convert_alpha()
bird_image_blue_closed = pygame.transform.scale(bird_image_blue_closed, (150, 100))



pipe_image = pygame.image.load(os.path.join(ASSETS_DIR, "pipe.png")).convert_alpha()
pipe_image = pygame.transform.scale(pipe_image, (52, 320))
pipe_top_image = pygame.transform.flip(pipe_image, False, True)

draw_img = pygame.image.load(os.path.join(ASSETS_DIR, "draw.png"))
draw_img = pygame.transform.scale(draw_img, (SCREEN_WIDTH, SCREEN_HEIGHT))


class Bird:
    def __init__(self, color, control_key):
        self.x = 100 if color == RED else 200
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.color = color
        self.control_key = control_key
        self.score = 0
        self.alive = True
        self.flap_animation_timer = 0

    def jump(self):
        self.velocity = self.jump_strength
        self.flap_animation_timer = 5

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        if self.y >= SCREEN_HEIGHT or self.y <= 0:
            self.alive = False
        if self.flap_animation_timer > 0:
            self.flap_animation_timer -= 1

    def draw(self):
        if self.color == RED:
            image = bird_image_red_closed if self.flap_animation_timer > 0 else bird_image_red_open
        else:
            image = bird_image_blue_closed if self.flap_animation_timer > 0 else bird_image_blue
        screen.blit(image, (self.x, self.y))


pipe_img = pygame.image.load(os.path.join(ASSETS_DIR, "pipe.png")).convert_alpha()

class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, 400)
        self.gap = 200
        self.passed_red = False
        self.passed_blue = False

        self.pipe_width = pipe_img.get_width()
        self.pipe_height = pipe_img.get_height()

        self.top_cut = 40
        self.bottom_cut = 40

        self.scale_width_factor = 1.2

    def update(self):
        self.x -= 5

    def draw(self):
        new_width = int(self.pipe_width * self.scale_width_factor)
        top_body_height = self.height - self.top_cut
        top_body_surf = pipe_img.subsurface(pygame.Rect(0, self.top_cut, self.pipe_width, top_body_height))
        top_body_surf = pygame.transform.flip(top_body_surf, False, True)
        top_body_surf = pygame.transform.scale(top_body_surf, (new_width, self.height))
        screen.blit(top_body_surf, (self.x, 0))

        bottom_body_height = SCREEN_HEIGHT - (self.height + self.gap) - self.bottom_cut
        bottom_body_surf = pipe_img.subsurface(pygame.Rect(0, 0, self.pipe_width, bottom_body_height))
        bottom_body_surf = pygame.transform.scale(bottom_body_surf, (new_width, bottom_body_height))
        screen.blit(bottom_body_surf, (self.x, self.height + self.gap + self.bottom_cut))

    def collide(self, bird):
        new_width = int(self.pipe_width * self.scale_width_factor)
        if bird.x + 34 > self.x and bird.x < self.x + new_width:
            if bird.y < self.height or bird.y + 24 > self.height + self.gap:
                bird.alive = False
def show_winner_screen(winner_color):
    if winner_color == RED:
        screen.blit(red_win_img, (0, 0))
    else:
        screen.blit(blue_win_img, (0, 0))

    screen.blit(restart_button_img, restart_button_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    return True
                
def show_draw_screen():
    # Desenha a tela de empate
    screen.blit(draw_img, (0, 0))

    # Centraliza o botão de restart
    restart_rect = restart_button_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 370))
    screen.blit(restart_button_img, restart_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    return True

def show_start_screen():
    while True:
        screen.blit(bg_image, (0, 0))
        screen.blit(start_button_img, start_button_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return

def main():
    while True:
        show_start_screen()

        clock = pygame.time.Clock()
        bird_red = Bird(RED, pygame.K_w)
        bird_blue = Bird(BLUE, pygame.K_UP)
        pipes = []
        frame_count = 0
        running = True
        game_over = False
        restart = False

        while running:
            screen.blit(bg_game_image, (0, 0))
            frame_count += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == bird_red.control_key and bird_red.alive:
                        bird_red.jump()
                    if event.key == bird_blue.control_key and bird_blue.alive:
                        bird_blue.jump()
                    if game_over:
                        if event.key == pygame.K_r:
                            running = False
                        elif event.key == pygame.K_q:
                            pygame.quit(); sys.exit()

            if bird_red.alive or bird_blue.alive:
                if frame_count % 90 == 0:
                    pipes.append(Pipe())

                for pipe in pipes:
                    pipe.update()
                    pipe.draw()
                    if bird_red.alive:
                        pipe.collide(bird_red)
                        if not pipe.passed_red and pipe.x + 52 < bird_red.x:
                            bird_red.score += 1
                            pipe.passed_red = True
                    if bird_blue.alive:
                        pipe.collide(bird_blue)
                        if not pipe.passed_blue and pipe.x + 52 < bird_blue.x:
                            bird_blue.score += 1
                            pipe.passed_blue = True

                pipes = [p for p in pipes if p.x > -52]

                bird_red.update()
                bird_blue.update()
                if bird_red.alive: bird_red.draw()
                if bird_blue.alive: bird_blue.draw()

            if not bird_red.alive and not bird_blue.alive and not game_over:
                if bird_red.score > bird_blue.score:
                    restart = show_winner_screen(RED)
                elif bird_blue.score > bird_red.score:
                    restart = show_winner_screen(BLUE)
                else:
                    restart = show_draw_screen()

                game_over = True
            if not bird_red.alive and not bird_blue.alive and not game_over:
                if bird_red.score > bird_blue.score:
                    restart = show_winner_screen(RED)
                elif bird_blue.score > bird_red.score:
                    restart = show_winner_screen(BLUE)
                else:
                    restart = show_draw_screen()

                game_over = True


            if game_over and not restart:
                pygame.display.flip()

            if restart:
                break

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()
