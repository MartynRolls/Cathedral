from math import sin, cos, radians, degrees, sqrt
from numpy import arctan2
from pygame import K_SPACE, K_LEFT, K_RIGHT, K_a, K_d, MOUSEBUTTONDOWN, MOUSEBUTTONUP, mouse


def find_piece_position(mouse_pos: tuple, screen_size: tuple, scale: int, angle: float, game) -> None:
    mouse_x, mouse_y = mouse_pos
    width, height = screen_size

    mouse_x, mouse_y = (mouse_x - width * 0.5,
                        mouse_y - height * 0.5)              # Calculate the centre as the origin
    distance = sqrt(mouse_x ** 2 + mouse_y ** 2)             # Find the mouses distance from the centre
    mouse_angle = arctan2(mouse_y, mouse_x)                  # Find the mouses angle from the centre
    true_angle = mouse_angle + radians(angle)                # Add the board angle
    mouse_x, mouse_y = (cos(true_angle) * distance / scale,
                        sin(true_angle) * distance / scale)  # Calculate the mouses position on the board
    mouse_x, mouse_y = (int((mouse_x + 50) * 0.1),
                        int((mouse_y + 50) * 0.1))           # Normalize
    mouse_x, mouse_y = (max(min(mouse_x, 9), 0),
                        max(min(mouse_y, 9), 0))             # Apply board limits

    directions = [(0, 0), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (2, 0), (0, 2),
                  (-2, 0), (0, -2), (2, 1), (1, 2), (-2, 1), (1, -2), (2, -1), (-1, 2), (-2, -1), (-1, -2)]

    for dx, dy in directions:  # Shuffle the piece around until it's completely on the board
        if (0 <= mouse_x + dx <= 9 and 0 <= mouse_y + dy <= 9 and
                game.board.check(game.player.piece, (mouse_x + dx, mouse_y + dy), True)):
            game.x, game.y = mouse_x + dx, mouse_y + dy
            break


start_pos = (0, 0)
old_angle = 0


def find_board_angle(mouse_pos: tuple, screen_size: tuple) -> float:
    mouse_x, mouse_y = mouse_pos
    start_x, start_y = start_pos
    width, height = screen_size

    mouse_x, mouse_y = (mouse_x - width * 0.5,
                        mouse_y - height * 0.5)              # Calculate the centre as the origin
    mouse_angle = arctan2(mouse_y, mouse_x)                  # Find the mouses angle from the centre

    start_x, start_y = (start_x - width * 0.5,
                        start_y - height * 0.5)              # Calculate the centre as the origin
    start_angle = arctan2(start_y, start_x)                  # Find the mouses origanal angle from the centre

    return old_angle + degrees(start_angle) - degrees(mouse_angle)


def check_mouse(event_type: int, angle: float, game) -> None:
    global start_pos, old_angle

    if event_type == MOUSEBUTTONDOWN:
        if mouse.get_pressed()[0]:       # If left mouse clicked
            game.place()                 # Place a piece
        if mouse.get_pressed()[2]:       # If right mouse clicked
            start_pos = mouse.get_pos()  # Note mouse position
            old_angle = angle            # Note angle

    if event_type == MOUSEBUTTONUP:      # If right mouse released
        if mouse.get_just_released()[2] and mouse.get_pos() == start_pos:  # If mouse hasn't been moved, it's a click
            game.player.rotate()         # So rotate current piece


def check_keys(event_key: int, game) -> None:
    # Change selected piece
    if event_key == K_a or event_key == K_LEFT:
        game.player.prev()
    if event_key == K_d or event_key == K_RIGHT:
        game.player.next()

    # Place current piece
    if event_key == K_SPACE:
        if game.playing:
            game.place()
