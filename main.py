from enum import Enum
from dataclasses import dataclass

@dataclass
class Board(): 
    position: list
    white_to_move: bool
    white_king_moved: bool
    white_kingside_rook_moved: bool
    white_queenside_rook_moved: bool
    black_king_moved: bool 
    black_kingside_rook_moved: bool
    black_queenside_rook_moved: bool 
    en_passant: int 
    moves_since_capture: int
    moves: int
    in_check: bool

# a1 b1 c1 d1 e1 f1 g1 h1        #  0  1  2  3  4  5  6  7
# a2 b2 c2 d2 e2 f2 g2 h2        #  8  9 10 11 12 13 14 15
# a3 b3 c3 d3 e3 f3 g3 h3        # 16 17 18 19 20 21 22 23
# a4 b4 c4 d4 e4 f4 g4 h4        # 24 25 26 27 28 29 30 31
# a5 b5 c5 d5 e5 f5 g5 h5        # 32 33 34 35 36 37 38 39
# a6 b6 c6 d6 e6 f6 g6 h6        # 40 41 42 43 44 45 46 47
# a7 b7 c7 d7 e7 f7 g7 h7        # 48 49 50 51 52 53 54 55
# a8 b8 c8 d8 e8 f8 g8 h8        # 56 57 58 59 60 61 62 63

@dataclass
class Move():
    start_sq: int 
    end_sq: int 
    promote_to: Enum = None

class pieces (Enum):
    WHITE_PAWN: int = 0
    BLACK_PAWN: int = 1
    WHITE_KNIGHT: int = 2
    BLACK_KNIGHT: int = 3
    WHITE_BISHOP: int = 4
    BLACK_BISHOP: int = 5
    WHITE_ROOK: int = 6
    BLACK_ROOK: int = 7
    WHITE_QUEEN: int = 8
    BLACK_QUEEN: int = 9
    WHITE_KING: int = 10
    BLACK_KING: int = 11

str_to_enum = { "P": pieces.WHITE_PAWN, "p": pieces.BLACK_PAWN,
                "R": pieces.WHITE_ROOK, "r": pieces.BLACK_ROOK,
                "N": pieces.WHITE_KNIGHT, "n": pieces.BLACK_KNIGHT,
                "B": pieces.WHITE_BISHOP, "b": pieces.BLACK_BISHOP,
                "Q": pieces.WHITE_QUEEN, "q": pieces.BLACK_QUEEN,
                "K": pieces.WHITE_KING, "k": pieces.BLACK_KING
                }
enum_to_str = ["P","p","N","n","B","n","R","r","Q","q","K","k"]

def process_fen(fen):
    piece_placement,turn,castling_rights,en_passant,halfmoves,fullmove = fen.split(" ")

    position = [None]*64
    index = -1
    ranks = piece_placement.split("/")
    for rank in ranks:
        for square in rank[-1::-1]:
            if square.isdigit():
                index -= int(square)
            else:
                position[index] = str_to_enum[square]
                index -=1
    
    white_to_move = True if turn == "w" else False

    white_king_moved = False if "K" in castling_rights or "Q" in castling_rights else True
    white_kingside_rook_moved = False if "K" in castling_rights else True
    white_queenside_rook_moved = False if "Q" in castling_rights else True
    black_king_moved = False if "k" in castling_rights or "q" in castling_rights else True
    black_kingside_rook_moved = False if "k" in castling_rights else True
    black_queenside_rook_moved = False if "q" in castling_rights else True
    
    en_passant = square_to_index(en_passant) if en_passant != "-" else None
    moves_since_capture = int(halfmoves)
    moves = int(fullmove)

    return Board(position, white_to_move, white_king_moved, white_kingside_rook_moved, white_queenside_rook_moved, black_king_moved, black_kingside_rook_moved, black_queenside_rook_moved, en_passant, moves_since_capture, moves, False)

#Helper functions

def index_to_square(index):
  file = chr(ord('a') + index % 8)
  rank = str(1+(index // 8))
  return file + rank

def square_to_index(square):
    return ord(square[0]) - 97 + (int(square[1]) - 1)*8

def print_board(board):
    row_start = -1
    row_end = -9

    while row_start > -65:
        rank = board.position[row_start:row_end:-1][-1::-1]
        for square in rank:
            if square is None:
                print(". ",end="")
            else:
                print(f"{enum_to_str[square.value]} ",end="")
        print("")
        row_start-=8
        row_end-=8

board = process_fen("8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 b - - 99 50")
print_board(board)
