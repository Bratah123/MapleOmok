import pygame

from components.base_component import BaseComponent
from components.render_priority import RenderPriority
from game.omok_piece import OmokPiece
from text.text import NormalText


class OmokBoard(BaseComponent):
    def __init__(self):
        super().__init__(RenderPriority.VERY_LOW)
        self.my_turn_sign = NormalText(135, 650, "Your Turn", font_size=24)
        self.opponent_turn_sign = NormalText(200, 35, "Opponent's Turn", font_size=24)

        self.my_turn = True

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
        # Check for any clicks on the board
        pass

    def handle_events(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.my_turn:
                self.handle_click_on_board(event.pos)

    def handle_click_on_board(self, position) -> None:
        for index, board_location in enumerate(self.board_locations):
            if board_location.collidepoint(position):
                if self.place_piece(index, "SlimePiece.png"):
                    self.my_turn = not self.my_turn
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
