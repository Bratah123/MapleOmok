import random
from typing import Tuple


class OpponentAI:
    def __init__(self, difficulty="hard"):
        self.name = "Opponent AI"
        self._difficulty = difficulty

    def make_move(self, pieces, board, last_player_move) -> int:
        if self._difficulty == "easy":
            return self.easy_move(pieces)
        elif self._difficulty == "hard":
            return self.hard_move(board, last_player_move)

    @staticmethod
    def easy_move(pieces):
        available_positions = [i for i in range(225) if i not in [piece.board_position for piece in pieces]]
        random_position = random.choice(available_positions)
        return random_position

    def hard_move(self, board, last_player_move) -> int:
        # Return the best move for the AI with the highest score
        _, best_move = self.minimax(board, last_player_move=last_player_move)
        return best_move

    @staticmethod
    def evaluate(board):
        # Check if we (opponent) won
        if board.check_win("MushroomPiece.png"):
            return 1000
        # Check if the player won
        elif board.check_win("SlimePiece.png"):
            return -1000

        return 0

    def minimax(self, board, alpha=-float("inf"), beta=float("inf"), depth=5, is_maximizer=True,
                last_player_move=None) \
            -> tuple[int, int]:
        # Minimax algorithm to determine the best move and return the highest scoring move
        # Return the best move for the AI
        # For optimizations, the AI will be looking at possible moves AROUND the player's pieces
        # That way we don't have to check every single available move on the board
        best_move = -1
        best_score = -1000 if is_maximizer else 1000
        best = (best_score, best_move)

        if depth == 0 or board.check_winner():
            score = self.evaluate(board)
            return score, best_move
        if is_maximizer:
            for avail_move in board.get_available_moves_near_piece(piece=last_player_move):
                board.place_piece(avail_move, "MushroomPiece.png")
                score, _ = self.minimax(board, alpha, beta, depth - 1, False, last_player_move)
                board.remove_piece(avail_move)
                if score > best_score:
                    best_score = score
                    best_move = avail_move
                    best = (best_score, best_move)

                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break

        else:
            for avail_move in board.get_available_moves_near_piece(piece=last_player_move):
                board.place_piece(avail_move, "SlimePiece.png")
                score, _ = self.minimax(board, alpha, beta, depth - 1, True, last_player_move)
                board.remove_piece(avail_move)
                if score < best_score:
                    best_score = score
                    best_move = avail_move
                    best = (best_score, best_move)

                beta = min(beta, best_score)
                if beta <= alpha:
                    break

        return best
