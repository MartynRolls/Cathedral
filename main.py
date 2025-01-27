from random import randint
from math import sin, cos, radians
import pygame
import cathedral
import graphics

# Initialising game
pygame.init()

# Defining Variables
width, height = 640, 640
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption('Cathedral')
clock = pygame.time.Clock()
game = cathedral.Game()

# Create a random board state
for _ in range(1000):
    game.x, game.y = randint(0, 9), randint(0, 9)
    for _ in range(randint(0, 5)):
        game.player.next()
    game.place()
game.playing = False

angle = 36
layers = 17
scale = 3
transitioning = False
title_screen = True

# Main loop
while True:
    keys = pygame.key.get_pressed()

    # Checking events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.WINDOWRESIZED:
            scale = min(screen.get_width(), screen.get_height()) // 180
        if event.type == pygame.KEYDOWN:
            # If shift is being held down, use alternative keybinds
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                if event.key == pygame.K_a or event.key == pygame.K_j:
                    game.player.prev()
                if event.key == pygame.K_d or event.key == pygame.K_l:
                    game.player.next()

            # Otherwise if the shift key isn't held down, use normal key binds
            else:
                # Piece movement, using trig functions to ensure the piece moves acording to what's seen
                # 0.75 multiplier ensures that the piece doesn't move on the x-axis and y-axis simultaniously
                if event.key == pygame.K_a or event.key == pygame.K_j:
                    game.x -= round(0.75 * cos(radians(angle)))
                    game.y -= round(0.75 * sin(radians(angle)))
                if event.key == pygame.K_d or event.key == pygame.K_l:
                    game.x += round(0.75 * cos(radians(angle)))
                    game.y += round(0.75 * sin(radians(angle)))
                if event.key == pygame.K_w or event.key == pygame.K_i:
                    game.x += round(0.75 * sin(radians(angle)))
                    game.y -= round(0.75 * cos(radians(angle)))
                if event.key == pygame.K_s or event.key == pygame.K_k:
                    game.x -= round(0.75 * sin(radians(angle)))
                    game.y += round(0.75 * cos(radians(angle)))

                game.x = max(min(game.x, 9), 0)  # Ensure position is still inbounds
                game.y = max(min(game.y, 9), 0)

                # Piece rotations
                if event.key == pygame.K_q or event.key == pygame.K_u:
                    game.player.rotate()
                if event.key == pygame.K_e or event.key == pygame.K_o:
                    game.player.rotate()
                    game.player.rotate()
                    game.player.rotate()

            # If the space key is pressed, place the piece or start a new game
            if event.key == pygame.K_SPACE:
                if game.playing:
                    game.place()
                else:
                    transitioning = True

    # Rotate the board
    if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and (keys[pygame.K_q] or keys[pygame.K_u]) and game.playing:
        angle += 4.5
    if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and (keys[pygame.K_e] or keys[pygame.K_o]) and game.playing:
        angle -= 4.5

    # Draw the game board
    screen.fill('white')
    surface = graphics.draw_board(game, angle, int(layers))

    if title_screen:  # Draw infomatic card
        surface.blit(graphics.cards['Title'], (29, 75))
    elif game.winner != 'Game in progress':
        surface.blit(graphics.cards[game.winner], (7, 75))

    surface = pygame.transform.scale_by(surface, (scale, scale))
    dest = ((screen.get_width() - surface.get_width()) // 2, (screen.get_height() - surface.get_height()) // 2)
    screen.blit(surface, dest)  # Place image onto the window

    if game.playing:  # Place image of remaining pieces on window sides
        pieces = graphics.draw_remaining_pieces(game)
        pieces = [pygame.transform.scale_by(pieces[i], (scale, scale)) for i in range(2)]
        screen.blit(pieces[0], (0, 0))
        screen.blit(pieces[1], (screen.get_width() - 10 * scale, 0))
    else:  # Otherwise rotate the board as a display
        angle += 0.5

    if transitioning:  # Remove layers from the board for a smooth transition
        if game.playing:
            layers += 0.2
            if layers > 17:
                layers = 17
                transitioning = False
        else:
            layers -= 0.2
            if layers < 0:
                angle = 36
                game = cathedral.Game()
                title_screen = False

    pygame.display.flip()
    clock.tick(60)
