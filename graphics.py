import pygame
from pygame.image import load
import cathedral


def prepare_sheet(surface: pygame.Surface) -> list[pygame.Surface]:
    slices = []
    size = surface.get_height()  # Because all the sprites are confined in squares, the height and width will be equal

    for i in range(surface.get_width() // size):  # For every sprite
        image = pygame.Surface((size, size), pygame.SRCALPHA)  # Create a surface, blit the sprite
        image.blit(surface, (0, 0), (i * size, 0, (i + 1) * size, size))  # onto that surface
        slices.append(image)  # And then add it to the sheet list

    return slices


def paint(surface_list: list[pygame.Surface], colour: tuple[int, int, int]) -> list[pygame.Surface]:
    sheet = []
    r, g, b = colour  # Extract the values from the tuple

    for surface in surface_list:  # For every surface in the list
        painted_surface = surface.copy()  # Copy the surface so that the original is unaffected
        painted_surface.fill((r, g, b, 255), special_flags=pygame.BLEND_MULT)  # Colour it

        sheet.append(painted_surface)  # Then add it to the return list

    return sheet


def mirror(surface_list: list[pygame.Surface]) -> list[pygame.Surface]:
    sheet = []

    for surface in surface_list:  # For every surface in the list
        mirrored_surface = surface.copy()  # Copy the surface so that the original is unaffected
        mirrored_surface = pygame.transform.flip(mirrored_surface, True, False)  # Flip it

        sheet.append(mirrored_surface)  # Then add it to the return list

    return sheet


pygame.init()

card_names = ['Title', 'White Wins', 'Black Wins', 'Tie']

piece_names = ['Tavern', 'Stable', 'Inn',
               'Bridge', 'Square', 'Manor',
               'Abbey', 'Academy', 'Infirmary',
               'Castle', 'Tower', 'Cathedral']

board_colour_codes = ['Board Blues', 'Board Whites', 'Board Blacks', 'Board Blues']
colours = {'White':   (255, 225, 195),
           'Black':   (205, 125, 95),
           'Blue':    (95, 95, 125),
           'Valid':   (95, 255, 95),
           'Invalid': (255, 95, 95),
           'Board Whites': [(255, 240, 225), (255, 235, 215)],
           'Board Blacks': [(205, 140, 125), (205, 135, 115)],
           'Board Blues':  [(115, 115, 130), (110, 110, 130)]}

cards = {}
unpainted_pieces = {'Wall': prepare_sheet(load('Sprites/Wall.png'))}
piece_sprites = {'Wall': paint(unpainted_pieces['Wall'], colours['Blue'])}
piece_shadows = [paint(prepare_sheet(load('Sprites/-Piece Shadows.png')), colours['White']),
                 mirror(paint(prepare_sheet(load('Sprites/-Piece Shadows.png')), colours['Black']))]

for name in card_names:
    cards[name] = load('Sprites/_' + name + ' Card.png')

for name in piece_names:
    unpainted_pieces[name] = prepare_sheet(load('Sprites/' + name + '.png'))

    if name == 'Cathedral':
        piece_sprites[name] = paint(unpainted_pieces[name], colours['Blue'])
        piece_sprites['Valid ' + name] = paint(unpainted_pieces[name], colours['Valid'])
        piece_sprites['Invalid ' + name] = paint(unpainted_pieces[name], colours['Invalid'])
    else:
        piece_sprites['White ' + name] = paint(unpainted_pieces[name], colours['White'])
        piece_sprites['Valid White ' + name] = paint(unpainted_pieces[name], colours['Valid'])
        piece_sprites['Invalid White ' + name] = paint(unpainted_pieces[name], colours['Invalid'])
        piece_sprites['Black ' + name] = mirror(paint(unpainted_pieces[name], colours['Black']))
        piece_sprites['Valid Black ' + name] = mirror(paint(unpainted_pieces[name], colours['Valid']))
        piece_sprites['Invalid Black ' + name] = mirror(paint(unpainted_pieces[name], colours['Invalid']))


def draw_board_sprite(game: cathedral.Game) -> pygame.Surface:
    surface = pygame.Surface((10, 10), pygame.SRCALPHA)  # Create a surface the size of the board

    for x in range(10):
        for y in range(10):  # For every cell in the board, colour it according to the territory
            surface.set_at((x, y), colours[board_colour_codes[game.board.territory_board[x][y]]][(x+y) % 2])

    return pygame.transform.scale_by(surface, (10, 10))  # Returned scaled board


def prepare_image(game: cathedral.Game) -> list[pygame.Surface]:
    sheet_list = [pygame.Surface((120, 120), pygame.SRCALPHA) for _ in range(17)]  # Set up sheet
    pieces = list(game.placed_pieces.values())  # Get pieces list without redundent call characters

    sheet_list[0].blit(draw_board_sprite(game), (10, 10))  # Put the board on the bottom of the stack

    for i, layer in enumerate(piece_sprites['Wall']):  # Paste game walls onto the sheet
        sheet_list[i].blit(layer, (0, 0))

    if game.playing:  # If the games being played, place the selcted piece aswell
        piece = game.get_piece_info()
        pieces.insert(0, piece)

    for piece in pieces:  # For every piece, place every layer in the sheet list
        for i, layer in enumerate(piece_sprites[piece[0]]):  # piece = [name, rotation, position]
            image = pygame.transform.rotate(layer, 90 * piece[1])
            sheet_list[i].blit(image, (10 * piece[2][0] + 10, 10 * piece[2][1] + 10))

    return sheet_list


def draw_select_piece(game: cathedral.Game, angle: float = 45) -> pygame.Surface:
    sheet_list = [pygame.Surface((120, 120), pygame.SRCALPHA) for _ in range(17)]
    piece = game.get_piece_info()

    for i, layer in enumerate(piece_sprites[piece[0]]):  # piece = [name, rotation, position]
        image = pygame.transform.rotate(layer, 90 * piece[1])
        sheet_list[i+1].blit(image, (10 * piece[2][0] + 10, 10 * piece[2][1] + 10))

    surface = pygame.Surface((250, 200), pygame.SRCALPHA)

    for i, layer in enumerate(sheet_list):
        image = pygame.transform.rotate(layer, angle)

        new_rect = image.get_rect(center=(125, 106 - i))
        dest = (round(new_rect.topleft[0]), round(new_rect.topleft[1]))

        surface.blit(image, dest)

    surface.set_alpha(95)

    return surface


def draw_remaining_pieces(game: cathedral.Game) -> list[pygame.Surface]:
    surfaces = [pygame.Surface((10, 150), pygame.SRCALPHA) for _ in range(2)]

    for i in range(2):
        y = 0
        for e, num in enumerate(game.players[i].piece_numbers):
            for o in range(num):
                y += 10
                if e != 11:
                    surfaces[i].blit(piece_shadows[i][e], (0, y))

    return surfaces


def draw_board(game: cathedral.Game, angle: float = 45, layers: int = 16) -> pygame.Surface:
    surface = pygame.Surface((250, 200), pygame.SRCALPHA)

    sprite_sheet = prepare_image(game)  # Prepare the sprite sheet

    for i, layer in enumerate(sprite_sheet):
        if i < layers:
            image = pygame.transform.rotate(layer, angle)

            new_rect = image.get_rect(center=(125, 105 - i))
            dest = (round(new_rect.topleft[0]), round(new_rect.topleft[1]))

            surface.blit(image, dest)

    if game.playing:
        ghost_piece = draw_select_piece(game, angle)
        surface.blit(ghost_piece, (0, 0))

    return surface
