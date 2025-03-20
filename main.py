import pygame
import cathedral
import graphics
import controls

# Initialising game
pygame.init()

# Defining Variables
width, height = 640, 640
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption('Cathedral')
clock = pygame.time.Clock()
game = cathedral.Game(True)

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
            if event.key == pygame.K_SPACE and not game.playing:
                transitioning = True

            # Check inputs
            controls.check_keys(event.key, game)
        controls.check_mouse(event.type, angle, game)

    # Send piece to mouse
    controls.find_piece_position(pygame.mouse.get_pos(), screen.get_size(), scale, angle, game)

    # Rotate Board
    if pygame.mouse.get_pressed()[2]:
        angle = controls.find_board_angle(pygame.mouse.get_pos(), screen.get_size())

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
