"""Checkers CLI Game - Main module with board representation and player setup."""

from enum import Enum
from typing import Optional


class PieceType(Enum):
    MAN = "man"
    KING = "king"


class PlayerColor(Enum):
    RED = "red"
    WHITE = "white"


class Piece:
    """Represents a checkers piece."""

    def __init__(self, color: PlayerColor, piece_type: PieceType = PieceType.MAN):
        self.color = color
        self.piece_type = piece_type

    def __repr__(self) -> str:
        return f"Piece({self.color.value}, {self.piece_type.value})"

    def promote_to_king(self) -> None:
        """Promote this piece to a king."""
        self.piece_type = PieceType.KING

    def is_king(self) -> bool:
        """Check if this piece is a king."""
        return self.piece_type == PieceType.KING


class Board:
    """Represents the 8x8 checkers board."""

    def __init__(self):
        self.size = 8
        self.grid: list[list[Optional[Piece]]] = [[None for _ in range(self.size)] for _ in range(self.size)]
        self._initialize_pieces()

    def _initialize_pieces(self) -> None:
        """Initialize pieces in their starting positions."""
        for row in range(self.size):
            for col in range(self.size):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.grid[row][col] = Piece(PlayerColor.WHITE)
                    elif row > 4:
                        self.grid[row][col] = Piece(PlayerColor.RED)

    def display(self) -> None:
        """Display the current board state."""
        print("  a b c d e f g h")
        for row in range(self.size):
            row_str = f"{row + 1} "
            for col in range(self.size):
                piece = self.grid[row][col]
                if piece is None:
                    cell = "."
                elif piece.color == PlayerColor.RED:
                    cell = "R" if piece.is_king() else "r"
                else:
                    cell = "W" if piece.is_king() else "w"
                row_str += cell + " "
            print(row_str)

    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        """Get the piece at the given position."""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.grid[row][col]
        return None

    def set_piece(self, row: int, col: int, piece: Optional[Piece]) -> None:
        """Set a piece at the given position."""
        if 0 <= row < self.size and 0 <= col < self.size:
            self.grid[row][col] = piece

    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if the position is within board bounds."""
        return 0 <= row < self.size and 0 <= col < self.size

    def is_empty(self, row: int, col: int) -> bool:
        """Check if the position is empty."""
        return self.get_piece(row, col) is None

    def copy(self) -> "Board":
        """Create a deep copy of the board."""
        new_board = Board()
        new_board.grid = []
        for row in range(self.size):
            new_row = []
            for col in range(self.size):
                piece = self.grid[row][col]
                if piece is not None:
                    new_piece = Piece(piece.color, piece.piece_type)
                    new_row.append(new_piece)
                else:
                    new_row.append(None)
            new_board.grid.append(new_row)
        return new_board


class Player:
    """Represents a player in the game."""

    def __init__(self, color: PlayerColor, name: str):
        self.color = color
        self.name = name
        self.pieces_remaining = 12

    def __repr__(self) -> str:
        return f"Player({self.name}, {self.color.value})"

    def remove_piece(self) -> None:
        """Remove one of this player's pieces."""
        if self.pieces_remaining > 0:
            self.pieces_remaining -= 1

    def has_pieces(self) -> bool:
        """Check if this player has any pieces remaining."""
        return self.pieces_remaining > 0


class CheckersGame:
    """Main game class for Checkers."""

    def __init__(self):
        self.board = Board()
        self.players = {
            PlayerColor.RED: Player(PlayerColor.RED, "Red Player"),
            PlayerColor.WHITE: Player(PlayerColor.WHITE, "White Player"),
        }
        self.current_player = PlayerColor.RED

    def switch_turn(self) -> None:
        """Switch to the other player's turn."""
        self.current_player = PlayerColor.WHITE if self.current_player == PlayerColor.RED else PlayerColor.RED

    def display(self) -> None:
        """Display the current game state."""
        self.board.display()
        print(f"\nCurrent turn: {self.players[self.current_player].name}")
        print(f"Red pieces remaining: {self.players[PlayerColor.RED].pieces_remaining}")
        print(f"White pieces remaining: {self.players[PlayerColor.WHITE].pieces_remaining}")

    def is_game_over(self) -> bool:
        """Check if the game is over."""
        red_player = self.players[PlayerColor.RED]
        white_player = self.players[PlayerColor.WHITE]
        return not red_player.has_pieces() or not white_player.has_pieces()

    def get_winner(self) -> Optional[PlayerColor]:
        """Get the winning player color, if any."""
        if not self.players[PlayerColor.RED].has_pieces():
            return PlayerColor.WHITE
        if not self.players[PlayerColor.WHITE].has_pieces():
            return PlayerColor.RED
        return None

    def get_valid_moves(self, row: int, col: int) -> list[tuple[int, int]]:
        """Get all valid moves for a piece at the given position."""
        piece = self.board.get_piece(row, col)
        if piece is None:
            return []

        moves = []
        directions = self._get_piece_directions(piece)

        for d_row, d_col in directions:
            new_row, new_col = row + d_row, col + d_col
            if self.board.is_valid_position(new_row, new_col) and self.board.is_empty(new_row, new_col):
                moves.append((new_row, new_col))

            jump_row, jump_col = row + 2 * d_row, col + 2 * d_col
            if self.board.is_valid_position(jump_row, jump_col) and self.board.is_empty(jump_row, jump_col):
                mid_row, mid_col = row + d_row, col + d_col
                mid_piece = self.board.get_piece(mid_row, mid_col)
                if mid_piece is not None and mid_piece.color != piece.color:
                    moves.append((jump_row, jump_col))

        return moves

    def _get_piece_directions(self, piece: Piece) -> list[tuple[int, int]]:
        """Get the valid movement directions for a piece."""
        if piece.is_king():
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        elif piece.color == PlayerColor.RED:
            return [(-1, -1), (-1, 1)]
        else:
            return [(1, -1), (1, 1)]

    def get_all_valid_moves(self) -> dict[tuple[int, int], list[tuple[int, int]]]:
        """Get all valid moves for the current player."""
        moves = {}
        for row in range(self.board.size):
            for col in range(self.board.size):
                piece = self.board.get_piece(row, col)
                if piece is not None and piece.color == self.current_player:
                    valid_moves = self.get_valid_moves(row, col)
                    if valid_moves:
                        moves[(row, col)] = valid_moves
        return moves

    def make_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Execute a move from one position to another."""
        piece = self.board.get_piece(from_row, from_col)
        if piece is None:
            return False

        valid_moves = self.get_valid_moves(from_row, from_col)
        if (to_row, to_col) not in valid_moves:
            return False

        self.board.set_piece(to_row, to_col, piece)
        self.board.set_piece(from_row, from_col, None)

        if abs(to_row - from_row) == 2:
            mid_row = (from_row + to_row) // 2
            mid_col = (from_col + to_col) // 2
            captured_piece = self.board.get_piece(mid_row, mid_col)
            if captured_piece is not None:
                self.board.set_piece(mid_row, mid_col, None)
                self.players[captured_piece.color].remove_piece()

        if piece.piece_type == PieceType.MAN:
            if piece.color == PlayerColor.RED and to_row == 0:
                piece.promote_to_king()
            elif piece.color == PlayerColor.WHITE and to_row == 7:
                piece.promote_to_king()

        return True


def parse_move(move_str: str) -> Optional[tuple[int, int, int, int]]:
    """Parse a move string in notation format (e.g., 'e6-d5') into coordinates.
    
    Returns (from_row, from_col, to_row, to_col) or None if invalid.
    """
    try:
        if len(move_str) != 5 or move_str[2] != '-':
            return None
        
        from_col_char = move_str[0].lower()
        from_row_str = move_str[1]
        to_col_char = move_str[3].lower()
        to_row_str = move_str[4]
        
        if not from_col_char.isalpha() or not to_col_char.isalpha():
            return None
        if not from_row_str.isdigit() or not to_row_str.isdigit():
            return None
        
        from_col = ord(from_col_char) - ord('a')
        from_row = int(from_row_str) - 1
        to_col = ord(to_col_char) - ord('a')
        to_row = int(to_row_str) - 1
        
        if not (0 <= from_col <= 7 and 0 <= from_row <= 7 and 
                0 <= to_col <= 7 and 0 <= to_row <= 7):
            return None
        
        return (from_row, from_col, to_row, to_col)
    except (ValueError, IndexError):
        return None


def format_position(row: int, col: int) -> str:
    """Format board coordinates as notation (e.g., 'a1', 'h8')."""
    col_char = chr(ord('a') + col)
    row_char = str(row + 1)
    return f"{col_char}{row_char}"


def format_move(from_row: int, from_col: int, to_row: int, to_col: int) -> str:
    """Format a move as notation string (e.g., 'e6-d5')."""
    return f"{format_position(from_row, from_col)}-{format_position(to_row, to_col)}"


def create_game() -> CheckersGame:
    """Factory function to create a new Checkers game."""
    return CheckersGame()


def play() -> None:
    """Main game loop for Checkers."""
    game = create_game()
    
    while not game.is_game_over():
        game.display()
        
        current_player = game.players[game.current_player]
        print(f"\n{current_player.name}'s turn")
        
        # Get all valid moves for current player
        all_moves = game.get_all_valid_moves()
        
        if not all_moves:
            print(f"No valid moves for {current_player.name}. Game over!")
            winner = game.get_winner()
            if winner:
                print(f"Winner: {game.players[winner].name}")
            return
        
        # Display available moves
        print("Available moves:")
        for (row, col), moves in all_moves.items():
            from_pos = format_position(row, col)
            for to_row, to_col in moves:
                to_pos = format_position(to_row, to_col)
                print(f"  {from_pos} -> {to_pos}")
        
        # Get move from user
        while True:
            move_str = input("Enter your move (e.g., e6-d5): ").strip()
            parsed = parse_move(move_str)
            
            if parsed is None:
                print("Invalid format. Please use format like 'e6-d5'")
                continue
            
            from_row, from_col, to_row, to_col = parsed
            
            # Validate that this is a valid move
            valid_moves = game.get_valid_moves(from_row, from_col)
            if (to_row, to_col) not in valid_moves:
                print("Invalid move. Please try again.")
                continue
            
            # Make the move
            game.make_move(from_row, from_col, to_row, to_col)
            break
        
        # Switch turns
        game.switch_turn()
    
    # Game over
    game.display()
    winner = game.get_winner()
    if winner:
        print(f"\nGame over! Winner: {game.players[winner].name}")
    else:
        print("\nGame over! It's a draw!")


def play_game() -> None:
    """Main game loop for CLI play."""
    game = create_game()
    
    while True:
        print(game.board)
        
        winner = game.get_winner()
        if winner is not None:
            print(f"{winner.name} wins!")
            break
        
        print(f"\n{game.current_player.name}'s turn")
        
        valid_moves = game.get_all_valid_moves()
        if not valid_moves:
            print(f"No valid moves for {game.current_player.name}. Game over!")
            break
        
        print("Valid moves:")
        for (row, col), moves in valid_moves.items():
            for move in moves:
                print(f"  {format_position(row, col)}-{format_position(move[0], move[1])}")
        
        while True:
            move_str = input("Enter your move (e.g., e6-d5): ")
            parsed = parse_move(move_str)
            if parsed is None:
                print("Invalid format. Use e6-d5 format.")
                continue
            
            from_row, from_col, to_row, to_col = parsed
            if game.make_move(from_row, from_col, to_row, to_col):
                break
            else:
                print("Invalid move. Try again.")
        
        game.switch_player()
