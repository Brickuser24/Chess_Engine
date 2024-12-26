from enum import Enum
from dataclasses import dataclass

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
    EMPTY_SQUARE: int = 12

def Parse_FEN(fen):
    fields: list = fen.split(" ")
    position: list = [pieces.EMPTY_SQUARE] * 64 
    index: int = 0
    ranks: list = fields[0].split("/")[-1::-1]
    for rank in ranks:
        for char in rank:
            if char == "/":
                continue
            elif char.isdigit():
                index+= int(char)
                continue
            elif char == "P":
                position[index] = pieces.WHITE_PAWN
            elif char == "p":
                position[index] = pieces.BLACK_PAWN
            elif char == "N":
                position[index] = pieces.WHITE_KNIGHT
            elif char == "n":
                position[index] = pieces.BLACK_KNIGHT
            elif char == "B":
                position[index] = pieces.WHITE_BISHOP
            elif char == "b":
                position[index] = pieces.BLACK_BISHOP
            elif char == "R":
                position[index] = pieces.WHITE_ROOK
            elif char == "r":
                position[index] = pieces.BLACK_ROOK
            elif char == "Q":
                position[index] = pieces.WHITE_QUEEN
            elif char == "q":
                position[index] = pieces.BLACK_QUEEN
            elif char == "K":
                position[index] = pieces.WHITE_KING
            else:
                position[index] = pieces.BLACK_KING
            index +=1

    return position, fields[1], fields[2], fields[3], fields[4]

def create_board(fen):
    position, turn, castling_rights, en_passant, moves_since_capture = Parse_FEN(fen)
    white_to_move = True if turn == "w" else False
    white_king_moved = False if "K" in castling_rights or "Q" in castling_rights else True
    white_kingside_rook_moved = False if "K" in castling_rights else True
    white_queenside_rook_moved = False if "Q" in castling_rights else True
    black_king_moved = False if "k" in castling_rights or "q" in castling_rights else True
    black_kingside_rook_moved = False if "k" in castling_rights else True
    black_queenside_rook_moved = False if "q" in castling_rights else True
    en_passant = square_to_index(en_passant) if en_passant != "-" else None
    moves_since_capture = moves_since_capture
    in_check = False
    return Board(position, white_to_move, white_king_moved, white_kingside_rook_moved, white_queenside_rook_moved, black_king_moved, black_kingside_rook_moved, black_queenside_rook_moved, en_passant, moves_since_capture, in_check)

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
    in_check: bool

    #Starting Board
    # "R","N","B","Q","K","B","N","R",        #  0  1  2  3  4  5  6  7
    # "P","P","P","P","P","P","P","P",        #  8  9 10 11 12 13 14 15
    # ".",".",".",".",".",".",".",".",        # 16 17 18 19 20 21 22 23
    # ".",".",".",".",".",".",".",".",        # 24 25 26 27 28 29 30 31
    # ".",".",".",".",".",".",".",".",        # 32 33 34 35 36 37 38 39
    # ".",".",".",".",".",".",".",".",        # 40 41 42 43 44 45 46 47
    # "p","p","p","p","p","p","p","p",        # 48 49 50 51 52 53 54 55
    # "r","n","b","q","k","b","n","r"         # 56 57 58 59 60 61 62 63

def index_to_square(index):
  file = chr(ord('a') + index % 8)
  rank = str(1+(index // 8))
  return file + rank

@dataclass
class Move():
    start_sq: int 
    end_sq: int 
    promote_to: Enum = None

def row(index):
  return (index // 8) + 1

def is_valid_target(index):
    return 0<= index <=63 

def in_bounds(index):
    return 0<= index <= 7 

def is_empty(square):
    return square == pieces.EMPTY_SQUARE

def is_white_piece(square):
    return square.value%2 == 0 and not is_empty(square)

def is_black_piece(square):
    return square.value%2 != 0

def square_to_index(square):
    return ord(square[0]) - ord("a") + (int(square[1]) - 1)*8

def get_pawn_moves(board,index):
    moves = []
    if board.white_to_move:
        target = index + 8
        rank = row(target)
        if rank == 8:   
            if is_empty(board.position[target]):   
                for piece in [pieces.WHITE_KNIGHT,pieces.WHITE_BISHOP,pieces.WHITE_ROOK,pieces.WHITE_QUEEN]:
                    moves.append(Move(index,target,piece))
            for i in [1,-1]:
                if (is_valid_target(target+i)) and (row(target+i) == 8) and (is_black_piece(board.position[target+i])):  
                    for piece in [pieces.WHITE_KNIGHT,pieces.WHITE_BISHOP,pieces.WHITE_ROOK,pieces.WHITE_QUEEN]:
                        moves.append(Move(index,target+i,piece))
        else:
            if is_empty(board.position[target]):
                moves.append(Move(index,target))
                if (row(index) == 2) and (is_empty(board.position[target+8])): 
                    moves.append(Move(index,target+8))
            for i in [1,-1]:
                if (is_valid_target(target+i)) and (row(target+i) == rank) and (is_black_piece(board.position[target+i])):  
                    moves.append(Move(index,target+i))
    else:
        target = index - 8
        rank = row(target)
        if rank == 1:   
            if is_empty(board.position[target]):   
                for piece in [pieces.BLACK_KNIGHT,pieces.BLACK_BISHOP,pieces.BLACK_ROOK,pieces.BLACK_QUEEN]:
                    moves.append(Move(index,target,piece))
            for i in [1,-1]:
                if (is_valid_target(target+i)) and (row(target+i) == 1) and (is_white_piece(board.position[target+i])):  
                    for piece in [pieces.BLACK_KNIGHT,pieces.BLACK_BISHOP,pieces.BLACK_ROOK,pieces.BLACK_QUEEN]:
                        moves.append(Move(index,target+i,piece))
        else:
            if is_empty(board.position[target]):
                moves.append(Move(index,target))
                if row(index) == 7 and is_empty(board.position[target-8]): 
                    moves.append(Move(index,target-8))
            for i in [1,-1]:
                if (is_valid_target(target+i)) and (row(target+i) == rank) and (is_white_piece(board.position[target+i])):  
                    moves.append(Move(index,target+i))

    return moves

def en_passant(board):
    if board.en_passant is None:
        return []
    moves = []
    index = board.en_passant
    if board.white_to_move:
        for i in (-7,-9):
            if (row(index+i) == row(index-8)) and (board.position[index+i] == pieces.WHITE_PAWN):
                moves.append(Move(index+i,index)) 
    else:
        for i in (7,9):
            if (row(index+i) == row(index+8)) and (board.position[index+i] == pieces.BLACK_PAWN):
                moves.append(Move(index+i,index))    
 
    return moves

def get_knight_moves(board,index):
    moves = []
    file = index%8
    rank = index//8
    directions = ((1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1))
    for dx,dy in directions:   
        new_file = file + dx
        new_rank = rank + dy
        if (not in_bounds(new_file)) or (not in_bounds(new_rank)): 
            continue
        target = new_file + new_rank*8
        if is_empty(board.position[target]):
            moves.append(Move(index,target))
        elif (board.white_to_move) and (is_black_piece(board.position[target])) or (not board.white_to_move) and (is_white_piece(board.position[target])):
            moves.append(Move(index,target)) 
                
    return moves

def get_slider_moves(board,index,directions):
    moves = []
    file = index%8
    rank = index//8
    for dx,dy in directions:    
        for i in range(1,8):
            new_file = file + dx*i
            new_rank = rank + dy*i
            if (not in_bounds(new_file)) or (not in_bounds(new_rank)):
                break 
            target = new_file + new_rank*8
            if is_empty(board.position[target]):   
                moves.append(Move(index,target))  
            else:
                if (board.white_to_move) and (is_black_piece(board.position[target])) or (not board.white_to_move) and (is_white_piece(board.position[target])):
                    moves.append(Move(index,target)) 
                break    

    return moves

def get_bishop_moves(board,index):
    directions = ((1,1),(1,-1),(-1,1),(-1,-1))
    return get_slider_moves(board,index,directions)

def get_rook_moves(board,index):
    directions = ((1,0),(-1,0),(0,1),(0,-1))
    return get_slider_moves(board,index,directions)

def get_queen_moves(board,index):
    directions = ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1))
    return get_slider_moves(board,index,directions)

def get_king_moves(board,index):
    moves = []
    file = index%8
    rank = index//8
    directions = ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1))
    for dx,dy in directions:   
        new_file = file + dx
        new_rank = rank + dy
        if (not in_bounds(new_file)) or (not in_bounds(new_rank)): 
            continue
        target = new_file + new_rank*8
        if is_empty(board.position[target]):
            moves.append(Move(index,target))
        elif (board.white_to_move) and (is_black_piece(board.position[target])) or (not board.white_to_move) and (is_white_piece(board.position[target])):
            moves.append(Move(index,target)) 
 
    return moves

def castling(board):
    if board.in_check:
        return []
    moves = []
    if board.white_to_move:
        if board.white_king_moved:
            return []
        if (not board.white_kingside_rook_moved) and (is_empty(board.position[5])) and (is_empty(board.position[6])):
            moves.append(Move(4,6))
        if (not board.white_queenside_rook_moved) and (is_empty(board.position[3])) and (is_empty(board.position[2])) and (is_empty(board.position[1])):
            moves.append(Move(4,2))
    else:
        if board.black_king_moved:
            return []
        if (not board.black_kingside_rook_moved) and (is_empty(board.position[61])) and (is_empty(board.position[62])):
            moves.append(Move(60,62))
        if (not board.black_queenside_rook_moved) and (is_empty(board.position[59])) and (is_empty(board.position[58])) and (is_empty(board.position[57])):
            moves.append(Move(60,58))

    return moves

def get_moves(board):
    board.in_check = in_check(board)
    moves = []
    if board.white_to_move:
        for index in range(64):
            if (is_empty(board.position[index])) or (is_black_piece(board.position[index])):
                continue
            piece = board.position[index]
            if piece == pieces.WHITE_PAWN:
                moves.extend(get_pawn_moves(board,index))
            elif piece == pieces.WHITE_KNIGHT:
                moves.extend(get_knight_moves(board,index))
            elif piece == pieces.WHITE_BISHOP:
                moves.extend(get_bishop_moves(board,index))
            elif piece == pieces.WHITE_ROOK:
                moves.extend(get_rook_moves(board,index))
            elif piece == pieces.WHITE_QUEEN:
                moves.extend(get_queen_moves(board,index))
            else:
                moves.extend(get_king_moves(board,index))

    else:
        for index in range(64):
            if (is_empty(board.position[index])) or (is_white_piece(board.position[index])):
                continue
            piece = board.position[index]
            if piece == pieces.BLACK_PAWN:
                moves.extend(get_pawn_moves(board,index))
            elif piece == pieces.BLACK_KNIGHT:
                moves.extend(get_knight_moves(board,index))
            elif piece == pieces.BLACK_BISHOP:
                moves.extend(get_bishop_moves(board,index))
            elif piece == pieces.BLACK_ROOK:
                moves.extend(get_rook_moves(board,index))
            elif piece == pieces.BLACK_QUEEN:
                moves.extend(get_queen_moves(board,index))
            else:
                moves.extend(get_king_moves(board,index))

    moves.extend(castling(board))
    moves.extend(en_passant(board))
    return moves

def make_move(board,move):
    if move.promote_to is not None:
        board.position[move.end_sq] = move.promote_to
        board.position[move.start_sq] = pieces.EMPTY_SQUARE
        if board.white_to_move and not board.black_king_moved:
            if board.position[63] != pieces.BLACK_ROOK:
                board.black_kingside_rook_moved = True
            if board.position[56] != pieces.BLACK_ROOK:
                board.black_queenside_rook_moved = True
        elif not board.white_to_move and not board.white_king_moved:
            if board.position[7] != pieces.WHITE_ROOK:
                board.white_kingside_rook_moved = True
            if board.position[0] != pieces.WHITE_ROOK:
                board.white_queenside_rook_moved = True
        board.white_to_move = False if board.white_to_move else True
        board.en_passant = None
        return check_legal(board,[])  
    piece = board.position[move.start_sq]
    board.position[move.end_sq] = piece
    board.position[move.start_sq] = pieces.EMPTY_SQUARE
    if board.en_passant is not None:
        if (piece == pieces.WHITE_PAWN) and (row(move.end_sq) == 6):
            board.position[move.end_sq-8] = pieces.EMPTY_SQUARE
        elif (piece == pieces.BLACK_PAWN) and (row(move.end_sq) == 3):
           board.position[move.end_sq+8] = pieces.EMPTY_SQUARE 
    if (piece == pieces.WHITE_KING) and (move.start_sq == 4) and (move.end_sq == 6):
        board.position[7] = pieces.EMPTY_SQUARE
        board.position[5] = pieces.WHITE_ROOK
        board.white_king_moved = True
        board.en_passant = None
        board.white_to_move = False if board.white_to_move else True
        return check_legal(board,[5,6])
    elif (piece == pieces.WHITE_KING) and (move.start_sq == 4) and (move.end_sq == 2):
        board.position[0] = pieces.EMPTY_SQUARE
        board.position[3] = pieces.WHITE_ROOK
        board.white_king_moved = True
        board.en_passant = None
        board.white_to_move = False if board.white_to_move else True
        return check_legal(board,[3])
    elif (piece == pieces.BLACK_KING) and (move.start_sq == 60) and (move.end_sq == 62):
        board.position[63] = pieces.EMPTY_SQUARE
        board.position[61] = pieces.BLACK_ROOK
        board.black_king_moved = True
        board.en_passant = None
        board.white_to_move = False if board.white_to_move else True
        return check_legal(board,[61,62])
    elif (piece == pieces.BLACK_KING) and (move.start_sq == 60) and (move.end_sq == 58):
        board.position[56] = pieces.EMPTY_SQUARE
        board.position[59] = pieces.BLACK_ROOK
        board.black_king_moved = True
        board.en_passant = None
        board.white_to_move = False if board.white_to_move else True
        return check_legal(board,[59])
    if (piece == pieces.WHITE_PAWN) and (move.end_sq-move.start_sq) == 16:
        board.en_passant = move.end_sq - 8
        board.white_to_move = False if board.white_to_move else True
        return check_legal(board,[])
    elif (piece == pieces.BLACK_PAWN) and (move.end_sq-move.start_sq) == -16:
        board.en_passant = move.end_sq + 8 
        board.white_to_move = False if board.white_to_move else True
        return check_legal(board,[])
    if not board.white_king_moved:
        if board.position[0] != pieces.WHITE_ROOK:
            board.white_queenside_rook_moved = True 
        if board.position[7] != pieces.WHITE_ROOK:
            board.white_kingside_rook_moved = True 
        if board.position[4] != pieces.WHITE_KING:
            board.white_king_moved = True 
    if not board.black_king_moved:
        if board.position[56] != pieces.BLACK_ROOK:
            board.black_queenside_rook_moved = True 
        if board.position[63] != pieces.BLACK_ROOK:
            board.black_kingside_rook_moved = True 
        if board.position[60] != pieces.BLACK_KING:
            board.black_king_moved = True  
    board.en_passant = None
    board.white_to_move = False if board.white_to_move else True
    return check_legal(board,[])

def under_attack_white(board,squares):
    for index in squares:
        file = index%8
        if row(index) != 8:
            for i in (9,7):
                if (row(index+i) == row(index+8)) and (index+i < 64) and (board.position[index+i] in (pieces.BLACK_PAWN,pieces.BLACK_KING)):
                    return True
            if board.position[index+8] == pieces.BLACK_KING:
                return True     
        if index < 63:
            if (row(index+1) == row(index)) and (board.position[index+1] == pieces.BLACK_KING):
                return True          
        if index > 0:
            if (row(index-1) == row(index)) and (board.position[index-1] == pieces.BLACK_KING):
                return True
        if row(index) != 1:
            for i in (-7,-9):
                if (row(index+i) == row(index-8)) and (index+i > -1) and (board.position[index+i] == pieces.BLACK_KING):
                    return True
            if board.position[index-8] == pieces.BLACK_KING:
                return True
        rank = index//8
        directions = ((1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1))
        for dx,dy in directions:
            new_file = file + dx
            new_rank = rank + dy
            if (not in_bounds(new_file)) or (not in_bounds(new_rank)): 
                continue
            target = new_file + new_rank*8
            if board.position[target]== pieces.BLACK_KNIGHT:
                return True
                
        checks = (((pieces.BLACK_BISHOP,pieces.BLACK_QUEEN),((1,1),(1,-1),(-1,1),(-1,-1))),
                ((pieces.BLACK_ROOK,pieces.BLACK_QUEEN),((1,0),(-1,0),(0,1),(0,-1))))
        for threats,directions in checks:
            for dx,dy in directions:
                for i in range(1,8):
                    new_file = file + dx*i
                    new_rank = rank + dy*i
                    if (not in_bounds(new_file)) or (not in_bounds(new_rank)):
                        break
                    target = new_file + new_rank*8
                    if board.position[target] in threats:
                        return True
                    elif not is_empty(board.position[target]):
                        break
    return False

def under_attack_black(board,squares):
    for index in squares:
        file = index%8
        if row(index) != 1:
            for i in (-9,-7):
                if (row(index+i) == row(index-8)) and (index+i > -1) and (board.position[index+i] in (pieces.WHITE_PAWN,pieces.WHITE_KING)):
                    return True
            if board.position[index-8] == pieces.WHITE_KING:
                return True     
        if index < 63:
            if (row(index+1) == row(index)) and (board.position[index+1] == pieces.WHITE_KING):
                return True          
        if index > 0:
            if (row(index-1) == row(index)) and (board.position[index-1] == pieces.WHITE_KING):
                return True
        if row(index) != 8:
            for i in (7,9):
                if (row(index+i) == row(index+8)) and (index+i < 64) and (board.position[index+i] == pieces.WHITE_KING):
                    return True
            if board.position[index+8] == pieces.WHITE_KING:
                return True
        rank = index//8
        directions = ((1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1))
        for dx,dy in directions:
            new_file = file + dx
            new_rank = rank + dy
            if (not in_bounds(new_file)) or (not in_bounds(new_rank)): 
                continue
            target = new_file + new_rank*8
            if board.position[target]== pieces.WHITE_KNIGHT:
                return True
                
        checks = (((pieces.WHITE_BISHOP,pieces.WHITE_QUEEN),((1,1),(1,-1),(-1,1),(-1,-1))),
                ((pieces.WHITE_ROOK,pieces.WHITE_QUEEN),((1,0),(-1,0),(0,1),(0,-1))))
        for threats,directions in checks:
            for dx,dy in directions:
                for i in range(1,8):
                    new_file = file + dx*i
                    new_rank = rank + dy*i
                    if (not in_bounds(new_file)) or (not in_bounds(new_rank)):
                        break
                    target = new_file + new_rank*8
                    if board.position[target] in threats:
                        return True
                    elif not is_empty(board.position[target]):
                        break
    return False

def check_legal(board,squares):
    if not board.white_to_move:
        k_square = board.position.index(pieces.WHITE_KING)
        return not under_attack_white(board,squares+[k_square])
        
    else:
        k_square = board.position.index(pieces.BLACK_KING)
        return not under_attack_black(board,squares+[k_square])
        
def in_check(board):
    if board.white_to_move:
        k_square = board.position.index(pieces.WHITE_KING)
        return under_attack_white(board,[k_square])

    else:
        k_square = board.position.index(pieces.BLACK_KING)
        return under_attack_black(board,[k_square])

def copy_board(board):
    return Board(
            board.position.copy(), 
            board.white_to_move, 
            board.white_king_moved, 
            board.white_kingside_rook_moved, 
            board.white_queenside_rook_moved, 
            board.black_king_moved, 
            board.black_kingside_rook_moved, 
            board.black_queenside_rook_moved, 
            board.en_passant, 
            board.moves_since_capture, 
            board.in_check
        ) 

piece_square_tables = ((0, 0, 0, 0, 0, 0, 0, 0, 98, 134, 61, 95, 68, 126, 34, -11, -6, 7, 26, 31, 65, 56, 25, -20, -14, 13, 6, 21, 23, 12, 17, -23, -27, -2, -5, 12, 17, 6, 10, -25, -26, -4, -4, -10, 3, 3, 33, -12, -35, -1, -20, -23, -15, 24, 38, -22, 0, 0, 0, 0, 0, 0, 0, 0),
                       (0, 0, 0, 0, 0, 0, 0, 0, -35, -1, -20, -23, -15, 24, 38, -22, -26, -4, -4, -10, 3, 3, 33, -12, -27, -2, -5, 12, 17, 6, 10, -25, -14, 13, 6, 21, 23, 12, 17, -23, -6, 7, 26, 31, 65, 56, 25, -20, 98, 134, 61, 95, 68, 126, 34, -11, 0, 0, 0, 0, 0, 0, 0, 0),
                       (-167, -89, -34, -49, 61, -97, -15, -107, -73, -41, 72, 36, 23, 62, 7, -17, -47, 60, 37, 65, 84, 129, 73, 44, -9, 17, 19, 53, 37, 69, 18, 22, -13, 4, 16, 13, 28, 19, 21, -8, -23, -9, 12, 10, 19, 17, 25, -16, -29, -53, -12, -3, -1, 18, -14, -19, -105, -21, -58, -33, -17, -28, -19, -230),
                       (-105, -21, -58, -33, -17, -28, -19, -230, -29, -53, -12, -3, -1, 18, -14, -19, -23, -9, 12, 10, 19, 17, 25, -16, -13, 4, 16, 13, 28, 19, 21, -8, -9, 17, 19, 53, 37, 69, 18, 22, -47, 60, 37, 65, 84, 129, 73, 44, -73, -41, 72, 36, 23, 62, 7, -17, -167, -89, -34, -49, 61, -97, -15, -107),
                       (-29, 4, -82, -37, -25, -42, 7, -8, -26, 16, -18, -13, 30, 59, 18, -47, -16, 37, 43, 40, 35, 50, 37, -2, -4, 5, 19, 50, 37, 37, 7, -2, -6, 13, 13, 26, 34, 12, 10, 4, 0, 15, 15, 15, 14, 27, 18, 10, 4, 15, 16, 0, 7, 21, 33, 1, -33, -3, -14, -21, -13, -12, -39, -21),
                       (-33, -3, -14, -21, -13, -12, -39, -21, 4, 15, 16, 0, 7, 21, 33, 1, 0, 15, 15, 15, 14, 27, 18, 10, -6, 13, 13, 26, 34, 12, 10, 4, -4, 5, 19, 50, 37, 37, 7, -2, -16, 37, 43, 40, 35, 50, 37, -2, -26, 16, -18, -13, 30, 59, 18, -47, -29, 4, -82, -37, -25, -42, 7, -8),
                       (32, 42, 32, 51, 63, 9, 31, 43, 27, 32, 58, 62, 80, 67, 26, 44, -5, 19, 26, 36, 17, 45, 61, 16, -24, -11, 7, 26, 24, 35, -8, -20, -36, -26, -12, -1, 9, -7, 6, -23, -45, -25, -16, -17, 3, 0, -5, -33, -44, -16, -20, -9, -1, 11, -6, -71, -19, -13, 1, 17, 16, 7, -37, -26),
                       (-19, -13, 1, 17, 16, 7, -37, -26, -44, -16, -20, -9, -1, 11, -6, -71, -45, -25, -16, -17, 3, 0, -5, -33, -36, -26, -12, -1, 9, -7, 6, -23, -24, -11, 7, 26, 24, 35, -8, -20, -5, 19, 26, 36, 17, 45, 61, 16, 27, 32, 58, 62, 80, 67, 26, 44, 32, 42, 32, 51, 63, 9, 31, 43),
                       (-28, 0, 29, 12, 59, 44, 43, 45, -24, -39, -5, 1, -16, 57, 28, 54, -13, -17, 7, 8, 29, 56, 47, 57, -27, -27, -16, -16, -1, 17, -2, 1, -9, -26, -9, -10, -2, -4, 3, -3, -14, 2, -11, -2, -5, 2, 14, 5, -35, -8, 11, 2, 8, 15, -3, 1, -1, -18, -9, 10, -15, -25, -31, -50),
                       (-1, -18, -9, 10, -15, -25, -31, -50, -35, -8, 11, 2, 8, 15, -3, 1, -14, 2, -11, -2, -5, 2, 14, 5, -9, -26, -9, -10, -2, -4, 3, -3, -27, -27, -16, -16, -1, 17, -2, 1, -13, -17, 7, 8, 29, 56, 47, 57, -24, -39, -5, 1, -16, 57, 28, 54, -28, 0, 29, 12, 59, 44, 43, 45),
                       (-65, 23, 16, -15, -56, -34, 2, 13, 29, -1, -20, -7, -8, -4, -38, -29, -9, 24, 2, -16, -20, 6, 22, -22, -17, -20, -12, -27, -30, -25, -14, -36, -49, -1, -27, -39, -46, -44, -33, -51, -14, -14, -22, -46, -44, -30, -15, -27, 1, 7, -8, -64, -43, -16, 9, 8, -15, 36, 12, -54, 8, -28, 24, 14),
                       (-15, 36, 12, -54, 8, -28, 24, 14, 1, 7, -8, -64, -43, -16, 9, 8, -14, -14, -22, -46, -44, -30, -15, -27, -49, -1, -27, -39, -46, -44, -33, -51, -17, -20, -12, -27, -30, -25, -14, -36, -9, 24, 2, -16, -20, 6, 22, -22, 29, -1, -20, -7, -8, -4, -38, -29, -65, 23, 16, -15, -56, -34, 2, 13)
)

piece_value = (82,82,337,337,365,365,477,477,1025,1025,0,0)

def evaluate(board):
    white_score = 0
    black_score = 0
    for i in range(64):
        if is_empty(board.position[i]):
            continue
        if is_black_piece(board.position[i]):   #Black Piece is faster to check
            black_score += piece_value[board.position[i].value]
            black_score += piece_square_tables[board.position[i].value][i]
        else:
            white_score += piece_value[board.position[i].value]
            white_score += piece_square_tables[board.position[i].value][i]
    return (white_score-black_score)/100 if board.white_to_move else -(white_score-black_score)/100

def search(board):
    moves = get_moves(board)
    best_eval = -float("inf")
    best_move = None
    for move in moves:
        calculation_board = copy_board(board)
        legal = make_move(calculation_board,move)
        if not legal:
            continue
        evaluation = evaluate(calculation_board)
        if evaluation > best_eval:
            best_eval = evaluation
            best_move = move
    return best_move

str_to_enum = {
    "P": pieces.WHITE_PAWN,
    "p": pieces.BLACK_PAWN,
    "R": pieces.WHITE_ROOK,
    "r": pieces.BLACK_ROOK,
    "N": pieces.WHITE_KNIGHT,
    "n": pieces.BLACK_KNIGHT,
    "B": pieces.WHITE_BISHOP,
    "b": pieces.BLACK_BISHOP,
    "Q": pieces.WHITE_QUEEN,
    "q": pieces.BLACK_QUEEN,
    "K": pieces.WHITE_KING,
    "k": pieces.BLACK_KING,
}

enum_to_str = ["P","p","N","n","B","n","R","r","Q","q","K","k","."]

def UCI():
    board = create_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    while True:
        uci_input = input()
        fields = uci_input.split(" ")
        command = fields[0]
        if command == "uci":
            print("id name Ralph")
            print("id author Brick")
            print("uciok")
        elif command == "isready":
            print("readyok")
        elif command == "position":
            if fields[1] == "fen":
                board = create_board(fields[2])
                if len(fields) > 3:
                    for move in fields[4:]:
                        if len(move) == 5:
                            if move[-2] == "8":
                                make_move(board,Move(square_to_index(move[0:2]),square_to_index(move[2:4]),str_to_enum[move[4].upper()]))
                            else:
                                make_move(board,Move(square_to_index(move[0:2]),square_to_index(move[2:4]),str_to_enum[move[4]]))
                        else:
                            make_move(board,Move(square_to_index(move[0:2]),square_to_index(move[2:4]),None))

            else:
                board = create_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
                if len(fields) > 2:
                    for move in fields[3:]:
                        if len(move) == 5:
                            if move[-2] == "8":
                                make_move(board,Move(square_to_index(move[0:2]),square_to_index(move[2:4]),str_to_enum[move[4].upper()]))
                            else:
                                make_move(board,Move(square_to_index(move[0:2]),square_to_index(move[2:4]),str_to_enum[move[4]]))
                        else:
                            make_move(board,Move(square_to_index(move[0:2]),square_to_index(move[2:4]),None))

        elif command == "go":
            move = search(board)
            output = index_to_square(move.start_sq)+index_to_square(move.end_sq)
            if move.promote_to is not None:
                output += enum_to_str[move.promote_to.value] 
            print("bestmove",output)

        #Command for personal UCI Testing
        #Not a part of UCI Protocol
        elif command == "printboard":
            for i in range(0,64,8):
                for j in board.position[i:i+8]:
                    print(enum_to_str[j], end = " ")
                print("")
        else:
            pass    

UCI()
