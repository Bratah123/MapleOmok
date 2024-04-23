import pygame

from components.base_component import BaseComponent
from components.render_priority import RenderPriority
from game.omok_piece import OmokPiece
from text.text import NormalText
from game.opponent_ai import OpponentAI

PIECE_UP_OFFSET = -1
PIECE_LEFT_OFFSET = -15
PIECE_RIGHT_OFFSET = 15
PIECE_DOWN_OFFSET = 1

# The index of the board is as follows:
COLUMN_INDEX = [(0, 14), (15, 29), (30, 44), (45, 59), (60, 74), (75, 89), (90, 104), (105, 119), (120, 134),
                (135, 149), (150, 164), (165, 179), (180, 194), (195, 209), (210, 224)]


class OmokBoard(BaseComponent):
    def __init__(self, screen: pygame.Surface):
        super().__init__(RenderPriority.VERY_LOW)
        self.my_turn_sign = NormalText(135, 650, "Your Turn", font_size=24)
        self.opponent_turn_sign = NormalText(200, 35, "Opponent's Turn", font_size=24)
        self.opponent = OpponentAI()

        self._screen = screen
        self.my_turn = True

        self.winner = False
        self._winning_pieces = []

        self._turns = 1
        self._last_player_move = None

        self._pieces = []
        self._opponent_pieces = []
        self._player_pieces = []

        self._available_moves = [
            i for i in range(225)
        ]

        self._rect = pygame.Rect(0, 0, 0, 0)
        self._board_size = 15  # Default Gomoku board size is 15x15
        self._board_x = 255
        self._board_y = 110

        self.board_locations = []

        for i in range(self._board_size):
            for j in range(self._board_size):
                # Draw the board on the current board location
                self.board_locations.append(pygame.Rect((i * 30) + self._board_x, (j * 30) + self._board_y, 30, 30))

    @property
    def image(self) -> pygame.Surface | None:
        return None

    @property
    def rect(self) -> pygame.Rect | None:
        return self._rect

    def draw(self, screen: pygame.Surface) -> None:
        # Draw the 15x15 board with each tile being a square
        for board_location in self.board_locations:
            pygame.draw.rect(screen, (255, 255, 255), board_location, 1)

        # Draw the pieces on the board based on its board index
        for piece in self._pieces:
            screen.blit(piece.image, self.board_locations[piece.board_position].topleft)

        if self.winner:
            self.draw_winning_line()
        # Draw the turn sign
        self.draw_turn_signs(screen)

    def draw_turn_signs(self, screen: pygame.Surface) -> None:
        """
        Draw the turn signs on the screen,
        indicating whose turn it is.
        :param screen:
        :return:
        """
        if self.my_turn:
            self.my_turn_sign.update_color((255, 255, 255))
            self.opponent_turn_sign.update_color((80, 80, 80))
        else:
            self.my_turn_sign.update_color((80, 80, 80))
            self.opponent_turn_sign.update_color((255, 255, 255))

        self.my_turn_sign.draw(screen)
        self.opponent_turn_sign.draw(screen)

    def update(self) -> None:
        # If it is opponent's turn, play a random move
        if not self.my_turn and not self.winner:
            self.opponent_turn()
            self.my_turn = True
            self._turns += 1
            if self.check_winner():
                self.winner = True

    def handle_events(self, event) -> None:
        if self.winner:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.my_turn:
                self.handle_click_on_board(event.pos)

    def handle_click_on_board(self, position) -> None:
        for index, board_location in enumerate(self.board_locations):
            if board_location.collidepoint(position):
                if self.place_piece(index, "SlimePiece.png"):
                    self.my_turn = not self.my_turn
                    self._turns += 1
                    self._last_player_move = self._pieces[-1]
                    if self.check_winner():
                        self.winner = True
                    pass
                break

    def place_piece(self, board_position: int, piece_type: str) -> bool:
        """
        Place a piece on the board at the given board position.
        :param board_position:
        :param piece_type:
        :return:
        """
        # Check if board position is already occupied
        for piece in self._pieces:
            if piece.board_position == board_position:
                return False
        piece = OmokPiece(piece_type)
        piece.board_position = board_position
        self._pieces.append(piece)
        self._available_moves.remove(board_position)

        if piece_type == "SlimePiece.png":
            self._player_pieces.append(board_position)
        else:
            self._opponent_pieces.append(board_position)
        return True

    def remove_piece(self, board_position: int) -> None:
        """
        Remove a piece from the board at the given board position.
        :param board_position:
        :return:
        """
        for piece in self._pieces:
            if piece.board_position == board_position:
                self._pieces.remove(piece)
                self._available_moves.append(board_position)
                if piece.piece_type == "SlimePiece.png":
                    self._player_pieces.remove(board_position)
                else:
                    self._opponent_pieces.remove(board_position)
                break

    def check_winner(self) -> bool:
        """
        Check if there is a winner on the board.
        :return:
        """
        for piece in self._pieces:
            # Check separately for horizontal, vertical, and diagonal so that we can draw the winning line
            if self.check_horizontal(piece):
                return True
            if self.check_vertical(piece):
                return True
            if self.check_left_down_right_diagonal(piece):
                return True
            if self.check_left_up_right_diagonal(piece):
                return True
        return False

    def draw_winning_line(self) -> None:
        """
        Draw a red line connecting the winning pieces.
        :return:
        """
        for i in range(len(self._winning_pieces) - 1):
            pygame.draw.line(self._screen, (255, 0, 0),
                             self.board_locations[self._winning_pieces[i]].center,
                             self.board_locations[self._winning_pieces[i + 1]].center, 3)

    def check_horizontal(self, piece: OmokPiece) -> bool:
        """
        Check if there are five consecutive pieces of the same type horizontally.
        :param piece:
        :return:
        """
        count = 0
        self._winning_pieces = [piece.board_position]

        if piece.piece_type == "SlimePiece.png":
            board_positions = self._player_pieces
        else:
            board_positions = self._opponent_pieces

        for i in range(1, 5):
            if piece.board_position + i * PIECE_RIGHT_OFFSET in board_positions:
                # Check if the piece is the same type
                count += 1
                self._winning_pieces.append(piece.board_position + i * PIECE_RIGHT_OFFSET)
            else:
                break
        for i in range(1, 5):
            if piece.board_position + i * PIECE_LEFT_OFFSET in board_positions:
                count += 1
                self._winning_pieces.append(piece.board_position + i * PIECE_LEFT_OFFSET)
            else:
                break
        return count >= 4

    def check_vertical(self, piece: OmokPiece) -> bool:
        """
        Check if there are five consecutive pieces vertically.
        :param piece:
        :return:
        """
        count = 0
        column_range = ()
        self._winning_pieces = [piece.board_position]
        if piece.piece_type == "SlimePiece.png":
            board_positions = self._player_pieces
        else:
            board_positions = self._opponent_pieces

        for column in COLUMN_INDEX:
            if piece.board_position in range(column[0], column[1] + 1):
                column_range = column
                break

        for i in range(1, 5):
            if piece.board_position + i * PIECE_DOWN_OFFSET in board_positions:
                if piece.board_position + i * PIECE_DOWN_OFFSET in range(column_range[0], column_range[1] + 1):
                    count += 1
                    self._winning_pieces.append(piece.board_position + i * PIECE_DOWN_OFFSET)
            else:
                break
        for i in range(1, 5):
            if piece.board_position + i * PIECE_UP_OFFSET in board_positions:
                if piece.board_position + i * PIECE_UP_OFFSET in range(column_range[0], column_range[1] + 1):
                    count += 1
                    self._winning_pieces.append(piece.board_position + i * PIECE_UP_OFFSET)
            else:
                break

        return count >= 4

    def check_left_down_right_diagonal(self, piece: OmokPiece) -> bool:
        """
        Check if there are five consecutive pieces diagonally.
        :param piece:
        :return:
        """
        count = 0
        self._winning_pieces = [piece.board_position]
        if piece.piece_type == "SlimePiece.png":
            board_positions = self._player_pieces
        else:
            board_positions = self._opponent_pieces

        for i in range(1, 5):
            if piece.board_position + i * PIECE_DOWN_OFFSET + i * PIECE_RIGHT_OFFSET in board_positions:
                count += 1
                self._winning_pieces.append(piece.board_position + i * PIECE_DOWN_OFFSET + i * PIECE_RIGHT_OFFSET)
            else:
                break
        for i in range(1, 5):
            if piece.board_position + i * PIECE_UP_OFFSET + i * PIECE_LEFT_OFFSET in board_positions:
                count += 1
                self._winning_pieces.append(piece.board_position + i * PIECE_UP_OFFSET + i * PIECE_LEFT_OFFSET)
            else:
                break
        return count >= 4

    def check_left_up_right_diagonal(self, piece: OmokPiece) -> bool:
        """
        Check if there are five consecutive pieces diagonally.
        :param piece:
        :return:
        """
        count = 0
        self._winning_pieces = [piece.board_position]
        if piece.piece_type == "SlimePiece.png":
            board_positions = self._player_pieces
        else:
            board_positions = self._opponent_pieces

        for i in range(1, 5):
            if piece.board_position + i * PIECE_UP_OFFSET + i * PIECE_RIGHT_OFFSET in board_positions:
                count += 1
                self._winning_pieces.append(piece.board_position + i * PIECE_UP_OFFSET + i * PIECE_RIGHT_OFFSET)
            else:
                break
        for i in range(1, 5):
            if piece.board_position + i * PIECE_DOWN_OFFSET + i * PIECE_LEFT_OFFSET in board_positions:
                count += 1
                self._winning_pieces.append(piece.board_position + i * PIECE_DOWN_OFFSET + i * PIECE_LEFT_OFFSET)
            else:
                break
        return count >= 4

    def opponent_turn(self) -> None:
        """
        Make a random move for the opponent.
        :return:
        """
        move = self.opponent.make_move(self._pieces, self, self._last_player_move)
        self.place_piece(move, "MushroomPiece.png")

    def reset_board(self) -> None:
        """
        Reset the board to its initial state.
        :return:
        """
        self._pieces = []
        self._available_moves = [
            i for i in range(225)
        ]
        self._opponent_pieces = []
        self._player_pieces = []
        self._last_player_move = None
        self.my_turn = True
        self.winner = False
        self.my_turn_sign.update_color((255, 255, 255))
        self.opponent_turn_sign.update_color((80, 80, 80))

    def check_win(self, piece_type: str) -> bool:
        """
        Check if the player has won the game.
        :param piece_type:
        :return:
        """
        for piece in self._pieces:
            if piece.piece_type == piece_type:
                if self.check_horizontal(piece) or self.check_vertical(piece) or self.check_left_down_right_diagonal(
                        piece) or self.check_left_up_right_diagonal(piece):
                    return True
        return False

    def check_player_win(self):
        """
        Check player moves in the player pieces list.
        The player pieces list contains a list of board positions where the player has placed a piece.
        :return:
        """
        for piece in self._player_pieces:
            if self.check_horizontal(piece) or self.check_vertical(piece) or self.check_left_down_right_diagonal(
                    piece) or self.check_left_up_right_diagonal(piece):
                return True
        return False

    def get_available_moves(self):
        """
        Get all available moves on the board.
        :return:
        """
        return self._available_moves

    def get_available_moves_near_piece(self, piece=None, search_size=5):
        """
        Get all available moves from a given piece and search size.
        :return:
        """
        grid_size = search_size
        if piece is None:
            return self._available_moves
        available_moves = []
        for i in range(-grid_size // 2, grid_size // 2 + 1):
            for j in range(-grid_size // 2, grid_size // 2 + 1):
                if piece.board_position + i * PIECE_UP_OFFSET + j * PIECE_LEFT_OFFSET in self._available_moves:
                    available_moves.append(piece.board_position + i * PIECE_UP_OFFSET + j * PIECE_LEFT_OFFSET)
        return available_moves
