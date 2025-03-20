from copy import deepcopy
from random import randint

pieces = {'Tavern':     [0, 0, 0, 0, 1, 0, 0, 0, 0],
          'Stable':     [0, 0, 0, 0, 1, 0, 0, 1, 0],
          'Inn':        [0, 0, 0, 0, 1, 1, 0, 0, 1],
          'Bridge':     [0, 1, 0, 0, 1, 0, 0, 1, 0],
          'Square':     [0, 0, 0, 0, 1, 1, 0, 1, 1],
          'Manor':      [0, 0, 0, 1, 1, 1, 0, 1, 0],
          'Abbey':      [0, 0, 0, 0, 1, 1, 1, 1, 0],
          'Academy':    [1, 1, 0, 0, 1, 1, 0, 1, 0],
          'Infirmary':  [0, 1, 0, 1, 1, 1, 0, 1, 0],
          'Castle':     [0, 0, 0, 1, 1, 1, 1, 0, 1],
          'Tower':      [0, 1, 1, 1, 1, 0, 1, 0, 0],
          'Cathedral':  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0]}

piece_names = ['White Tavern', 'White Stable', 'White Inn', 'White Bridge', 'White Square', 'White Manor',
               'White Abbey', 'White Academy', 'White Infirmary', 'White Castle', 'White Tower', 'Cathedral',
               'Black Tavern', 'Black Stable', 'Black Inn', 'Black Bridge', 'Black Square', 'Black Manor',
               'Black Abbey', 'Black Academy', 'Black Infirmary', 'Black Castle', 'Black Tower']


class Piece:
    def __init__(self, piece: list[int], colour_code: int = 1, size: int = 3):
        self.piece = piece
        self.colour_code = colour_code
        self.layers = len(piece)
        self.value = sum(piece)
        self.size = size
        self.rotation = 0

        if colour_code == 2:
            self.mirror()  # Flip piece if black

    def __str__(self):
        string = ''                     # Create the empty string
        for y in range(self.size):      # For each row
            for x in range(self.size):  # And for each column, add it to the string
                string += str(self.piece[x + y * self.size]) + ' '
            string += '\n'              # Add a break between each row

        return string

    def mirror(self) -> None:
        new_piece = []                  # Create new piece
        for y in range(self.size):      # For each cell (x and y as 2d)
            for x in range(self.size):  # Copy next index from the appropriate cell
                new_piece.append(self.piece[(y + 1) * self.size - 1 - x])

        self.piece = new_piece  # Update piece

    def rotate(self) -> None:
        new_piece = []                  # Create new piece
        for x in range(self.size):      # For each cell (x and y as 2d)
            for y in range(self.size):  # Copy next index from the appropriate cell
                new_piece.append(self.piece[(y + 1) * self.size - 1 - x])

        self.piece = new_piece  # Update piece
        self.rotation += 1 if self.rotation != 3 else -3  # Update rotation


class Board:
    def __init__(self):
        self.board = [[0 for _ in range(10)] for _ in range(10)]             # We need a board to distinguish colours
        self.piece_board = [['-' for _ in range(10)] for _ in range(10)]     # One to distinguish different pieces
        self.territory_board = [[0 for _ in range(10)] for _ in range(10)]   # And one to track claimed territory

        self.removed_pieces = []  # List to keep track of pieces that have been taken off the board
        self.piece_removed = False  # Variable to tell if a piece has been removed recently
        self.chars = list('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')  # Char list for piece board

    def print(self, board: list[list] | None = None) -> None:
        if board is None:
            board = self.territory_board

        for y in range(10):         # Then for each row
            string = ''             # Prep an empty string
            for x in range(10):     # And for each column, add it
                string += str(board[x][y]) + ' '  # to the string
            print(string)           # Print the string for that row
        print()                     # Add space below

    def check(self, piece: Piece, position: tuple[int, int], check_boundries_only: bool = False) -> bool:
        for y in range(piece.size):
            for x in range(piece.size):
                if piece.piece[x + y * piece.size]:  # If there is a part of the piece in this tile
                    x_dest, y_dest = position[0] + x - piece.size // 2, position[1] + y - piece.size // 2
                    if not (0 <= x_dest <= 9 and 0 <= y_dest <= 9):
                        return False  # Can't place if out of bounds
                    if self.board[x_dest][y_dest] and not check_boundries_only:
                        return False  # Can't place if on another piece
                    if 0 < self.territory_board[x_dest][y_dest] != piece.colour_code and not check_boundries_only:
                        return False  # Can't place if in another players territory

        return True

    def place(self, piece: Piece, position: tuple[int, int]) -> None:
        for y in range(piece.size):
            for x in range(piece.size):                 # For every cell in the piece list:
                if piece.piece[x + y * piece.size]:     # If it's a part of the piece:
                    x_dest, y_dest = position[0] + x - piece.size // 2, position[1] + y - piece.size // 2  # Get coords
                    self.board[x_dest][y_dest] = piece.colour_code  # Set the board location to the right colour code
                    self.piece_board[x_dest][y_dest] = self.chars[0]  # Set the piece board to a new id for the piece
                    self.claim_territory((x_dest, y_dest), piece.colour_code)  # And try to claim territory

        self.chars.pop(0)  # Remove used id

    def claim_territory(self, position: tuple[int, int], colour_code: int) -> None:
        start_x, start_y = position
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

        self.territory_board[start_x][start_y] = colour_code

        for start_dx, start_dy in directions:
            if 0 <= start_x + start_dx <= 9 and 0 <= start_y + start_dy <= 9:
                piece_found = None
                current_board = deepcopy(self.territory_board)

                if current_board[start_x + start_dx][start_y + start_dy] not in [0, 3, colour_code]:
                    piece_found = self.piece_board[start_x + start_dx][start_y + start_dy]

                current_board[start_x + start_dx][start_y + start_dy] = -1  # Marking moving cells

                searching = True
                while searching:
                    next_board = deepcopy(current_board)
                    for x in range(10):
                        for y in range(10):                                     # For every cell on the board:
                            if current_board[x][y] == -1:                       # If tile is still searching
                                for dx, dy in directions:                       # Then for every direction it can go in
                                    if 0 <= x + dx <= 9 and 0 <= y + dy <= 9:   # If that direction isn't off the board:
                                        tile = current_board[x + dx][y + dy]    # Note down the tile contents
                                        piece_code = self.piece_board[x + dx][y + dy]    # Note down tile piece code
                                        if tile == 0 or piece_code == '-' and 0 < tile:  # If the tile is empty:
                                            next_board[x + dx][y + dy] = -1     # Claim it
                                        elif tile == 3:                         # If the tile is the Cathedral:
                                            searching = False                   # End the search
                                        elif 0 < tile != colour_code:           # If the tile belongs to the enemy:
                                            if piece_found is None:                 # If no pieces have been found:
                                                piece_found = piece_code            # Note the piece
                                                next_board[x + dx][y + dy] = -1     # And claim the tile
                                            elif piece_found == piece_code:         # If it's the found piece:
                                                next_board[x + dx][y + dy] = -1     # Claim the tile
                                            else:                                   # Otherwise it's a new piece
                                                searching = False                   # So end the search

                                next_board[x][y] = -2  # Cell is done searching

                    if next_board != current_board:  # If the board has changed, the search is not done
                        current_board = next_board   # So update the current board

                    else:                            # Else if the board hasn't changed, the search is done
                        if piece_found is not None:  # If a piece has been noted down, it can be removed
                            self.removed_pieces.append(piece_found)
                            self.piece_removed = True

                        for x in range(10):
                            for y in range(10):                               # For every cell on the board:
                                if current_board[x][y] == -2:                 # If it was claimed:
                                    self.territory_board[x][y] = colour_code  # Update the territory boards
                                if self.piece_board[x][y] == piece_found:     # If it's the removed piece:
                                    self.piece_board[x][y] = '-'              # Remove it from the piece board
                                    self.board[x][y] = 0                      # And from the game board

                        searching = False


class Player:
    def __init__(self, colour_code: int):
        self.colour_code = colour_code
        self.piece_numbers = [2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1 if colour_code == 1 else 0]
        self.piece_list = []
        self.placed_piece_calls = {}
        self.selected = 11 if colour_code == 1 else 0  # Select cathedral if white

        for name, piece in pieces.items():
            if name == 'Cathedral':
                self.piece_list.append(Piece(piece, 3, 5))
            else:
                self.piece_list.append(Piece(piece, colour_code))

        self.piece = self.piece_list[self.selected]

    def rotate(self) -> None:
        self.piece.rotate()

    def next(self) -> None:
        if not (self.selected == 11 and self.piece_numbers[11] == 1) and self.has_pieces():
            self.selected += 1 if self.selected != 11 else - 11      # Move to next piece
            while not self.piece_numbers[self.selected]:             # And while there is none of that piece left
                self.selected += 1 if self.selected != 11 else - 11  # Move to the next piece
            self.piece = self.piece_list[self.selected]              # And then update the piece variable

    def prev(self) -> None:
        if not (self.selected == 11 and self.piece_numbers[11] == 1) and self.has_pieces():
            self.selected -= 1 if self.selected != 0 else - 11       # Move to previous piece
            while not self.piece_numbers[self.selected]:             # And while there is none of that piece left
                self.selected -= 1 if self.selected != 0 else - 11   # Move to the next piece
            self.piece = self.piece_list[self.selected]              # And then update the piece variable

    def place(self, board: Board, position) -> None:
        self.placed_piece_calls[board.chars[0]] = self.selected  # Note piece being placed
        self.piece_numbers[self.selected] -= 1                   # Reduce piece numbers
        board.place(self.piece, position)                        # Place piece on board
        if not self.piece_numbers[self.selected]:                # If there's no more of that piece
            self.next()                                          # Move to the next one

    def return_piece(self, call: str) -> None:
        if call in self.placed_piece_calls:             # If the call number is from a piece the player's placed:
            self.piece_numbers[self.placed_piece_calls[call]] += 1  # Add one back to that piece count
            del self.placed_piece_calls[call]                       # Remove the call

    def can_place(self, board: Board) -> bool:
        for x in range(10):
            for y in range(10):  # For every grid on the board, try and place each
                for i, piece in enumerate(self.piece_list):  # remaining piece on it
                    if self.piece_numbers[i] and board.check(piece, (x, y)):
                        return True  # The player still has a move if they can place it
        return False

    def has_pieces(self) -> bool:
        for number in self.piece_numbers:
            if number > 0:
                return True
        return False

    def score(self) -> int:
        score = 0
        for i, num in enumerate(self.piece_numbers):
            score += self.piece_list[i].value * num
        return score


class Game:
    def __init__(self, make_random_board: bool = False):
        self.board = Board()
        self.players = [Player(1), Player(2)]
        self.player = self.players[0]
        self.player_turn = 0
        self.playing = True
        self.winner = 'Game in progress'

        self.x, self.y = 5, 5
        self.placed_pieces = {}

        if make_random_board:  # Create a random boardstate for the title screen
            for _ in range(1000):
                self.x, self.y = randint(0, 9), randint(0, 9)
                for _ in range(randint(0, 5)):
                    self.player.next()
                self.place()
            self.playing = False

    def get_piece_info(self) -> list:
        name = 'Valid ' if self.board.check(self.player.piece, (self.x, self.y)) else 'Invalid '
        name += piece_names[12 * (self.player.colour_code - 1) + self.player.selected]
        rotation = self.player.piece.rotation
        position = (self.x - self.player.piece.size // 2, self.y - self.player.piece.size // 2)

        return [name, rotation, position]

    def place(self):
        if self.board.check(self.player.piece, (self.x, self.y)):                      # Ensure player can place

            self.placed_pieces[self.board.chars[0]] = [                                # Add details to a dictonary
                piece_names[12 * (self.player.colour_code-1) + self.player.selected],  # The piece name
                self.player.piece.rotation,                                            # The number of rotations
                (self.x - self.player.piece.size // 2,                                 # And the piece position
                 self.y - self.player.piece.size // 2)]

            self.player.place(self.board, (self.x, self.y))  # Place the piece on the board
            if self.board.piece_removed:          # If a piece was removed from the board:
                self.board.piece_removed = False  # Return that piece to the player and delete it
                self.players[1 - self.player_turn].return_piece(self.board.removed_pieces[-1])
                del self.placed_pieces[self.board.removed_pieces[-1]]

            if self.players[1 - self.player_turn].can_place(self.board):  # Check if other player can actually go
                self.player_turn = 1 - self.player_turn       # If they can, it's their turn
                self.player = self.players[self.player_turn]  # Update player variable

            elif not self.player.can_place(self.board):       # If both they and the current player can't go:
                self.playing = False                          # The game is over
                scores = [self.players[0].score(), self.players[1].score()]  # Tally the player's scores
                if scores[0] < scores[1]:  # Find winner
                    self.winner = 'White Wins'
                elif scores[1] < scores[0]:
                    self.winner = 'Black Wins'
                else:
                    self.winner = 'Tie'

