import pygame
import random

from components.base_component import BaseComponent
from components.render_priority import RenderPriority
from game.omok_piece import OmokPiece
from text.text import NormalText

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

        self._screen = screen
        self.my_turn = True

        self.winner = False
        self._winning_pieces = []

        self._pieces = []

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
        return True

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
        board_positions = [p.board_position for p in self._pieces if piece.piece_type.lower() == p.piece_type.lower()]

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
        board_positions = [p.board_position for p in self._pieces if piece.piece_type.lower() == p.piece_type.lower()]

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
        board_positions = [p.board_position for p in self._pieces if piece.piece_type.lower() == p.piece_type.lower()]

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
        board_positions = [p.board_position for p in self._pieces if piece.piece_type.lower() == p.piece_type.lower()]

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
        # TODO: Add minimax algorithm for the opponent
        available_positions = [i for i in range(225) if i not in [piece.board_position for piece in self._pieces]]
        random_position = random.choice(available_positions)
        self.place_piece(random_position, "MushroomPiece.png")

    def reset_board(self) -> None:
        """
        Reset the board to its initial state.
        :return:
        """
        self._pieces = []
        self.my_turn = True
        self.winner = False
        self.my_turn_sign.update_color((255, 255, 255))
        self.opponent_turn_sign.update_color((80, 80, 80))
