import numpy as np
import time as t

#Notes
#Replace pieces and empty squares with integers

square_to_index = {
  "a8": 0, "b8": 1, "c8": 2, "d8": 3, "e8": 4, "f8": 5, "g8": 6, "h8": 7,
  "a7": 8, "b7": 9, "c7": 10, "d7": 11, "e7": 12, "f7": 13, "g7": 14, "h7": 15,
  "a6": 16, "b6": 17, "c6": 18, "d6": 19, "e6": 20, "f6": 21, "g6": 22, "h6": 23,
  "a5": 24, "b5": 25, "c5": 26, "d5": 27, "e5": 28, "f5": 29, "g5": 30, "h5": 31,
  "a4": 32, "b4": 33, "c4": 34, "d4": 35, "e4": 36, "f4": 37, "g4": 38, "h4": 39,
  "a3": 40, "b3": 41, "c3": 42, "d3": 43, "e3": 44, "f3": 45, "g3": 46, "h3": 47,
  "a2": 48, "b2": 49, "c2": 50, "d2": 51, "e2": 52, "f2": 53, "g2": 54, "h2": 55,
  "a1": 56, "b1": 57, "c1": 58, "d1": 59, "e1": 60, "f1": 61, "g1": 62, "h1": 63
}

index_to_square = {
    0: "a8", 1: "b8", 2: "c8", 3: "d8", 4: "e8", 5: "f8", 6: "g8", 7: "h8",
    8: "a7", 9: "b7", 10: "c7", 11: "d7", 12: "e7", 13: "f7", 14: "g7", 15: "h7",
    16: "a6", 17: "b6", 18: "c6", 19: "d6", 20: "e6", 21: "f6", 22: "g6", 23: "h6",
    24: "a5", 25: "b5", 26: "c5", 27: "d5", 28: "e5", 29: "f5", 30: "g5", 31: "h5",
    32: "a4", 33: "b4", 34: "c4", 35: "d4", 36: "e4", 37: "f4", 38: "g4", 39: "h4",
    40: "a3", 41: "b3", 42: "c3", 43: "d3", 44: "e3", 45: "f3", 46: "g3", 47: "h3",
    48: "a2", 49: "b2", 50: "c2", 51: "d2", 52: "e2", 53: "f2", 54: "g2", 55: "h2",
    56: "a1", 57: "b1", 58: "c1", 59: "d1", 60: "e1", 61: "f1", 62: "g1", 63: "h1"
}

class Board():
    def __init__(self,fen = None,board = None,white_to_move = None,white_king_moved = None,
                 white_kingside_rook_moved = None,white_queenside_rook_moved = None,
                 black_king_moved = None,black_kingside_rook_moved = None,black_queenside_rook_moved = None,
                 en_passant = None,moves_since_capture = None,in_check = None):
        if fen is None:
            self.board = np.array([
            ".",".",".",".",".",".",".",".",        # 16 17 18 19 20 21 22 23
            ".",".",".",".",".",".",".",".",        # 24 25 26 27 28 29 30 31
            ".",".",".",".",".",".",".",".",        # 16 17 18 19 20 21 22 23
            ".",".",".",".",".",".",".",".",        # 24 25 26 27 28 29 30 31
            ".",".",".",".",".",".",".",".",        # 32 33 34 35 36 37 38 39
            ".",".","k",".",".",".",".",".",        # 40 41 42 43 44 45 46 47
            ".",".",".",".",".",".","r",".",        # 16 17 18 19 20 21 22 23
            ".","K",".",".",".",".",".",".",        # 24 25 26 27 28 29 30 31
            ]) if board is None else board
            
            #Starting Board
            # "r","n","b","q","k","b","n","r",        #  0  1  2  3  4  5  6  7
            # "p","p","p","p","p","p","p","p",        #  8  9 10 11 12 13 14 15
            # ".",".",".",".",".",".",".",".",        # 16 17 18 19 20 21 22 23
            # ".",".",".",".",".",".",".",".",        # 24 25 26 27 28 29 30 31
            # ".",".",".",".",".",".",".",".",        # 32 33 34 35 36 37 38 39
            # ".",".",".",".",".",".",".",".",        # 40 41 42 43 44 45 46 47
            # "P","P","P","P","P","P","P","P",        # 48 49 50 51 52 53 54 55
            # "R","N","B","Q","K","B","N","R"         # 56 57 58 59 60 61 62 63

            self.white_to_move = True if white_to_move is None else white_to_move

            #Info for Castling
            self.white_king_moved = False if white_king_moved is None else white_king_moved
            self.white_kingside_rook_moved = False if white_kingside_rook_moved is None else white_kingside_rook_moved
            self.white_queenside_rook_moved = False if white_queenside_rook_moved is None else white_queenside_rook_moved

            self.black_king_moved = False if black_king_moved is None else black_king_moved
            self.black_kingside_rook_moved = False if black_kingside_rook_moved is None else black_kingside_rook_moved
            self.black_queenside_rook_moved = False if black_queenside_rook_moved is None else black_queenside_rook_moved

            self.en_passant = en_passant
            
            self.moves_since_capture = 0 if moves_since_capture is None else moves_since_capture

            self.in_check = False 
        
        else:
            #Load game from FEN
            #eg rnbqkbnr/2p1p1pp/1p3p2/p2p4/Q1P1P3/8/PP1P1PPP/RNB1KBNR b KQkq - 0 1
            self.board = []
            fields = fen.split(" ")
            ranks = fields[0].split("/")
            for rank in ranks:
                formatted_rank=[]
                for char in rank:
                    if char.isdigit():
                        for i in range(int(char)):
                            formatted_rank.append(".")
                    else:
                        formatted_rank.append(char)
                self.board.extend(formatted_rank)
            self.board = np.array(self.board)
            self.white_to_move = True if fields[1] == "w" else False
            self.white_king_moved = False if "K" in fields[2] or "Q" in fields[2] else True
            self.white_kingside_rook_moved = False if "K" in fields[2] else True
            self.white_queenside_rook_moved = False if "Q" in fields[2] else True
            self.black_king_moved = False if "k" in fields[2] or "q" in fields[2] else True
            self.black_kingside_rook_moved = False if "k" in fields[2] else True
            self.black_queenside_rook_moved = False if "q" in fields[2] else True
            self.en_passant = square_to_index[fields[3]] if fields[3] != "-" else None
            self.moves_since_capture = int(fields[4])
            self.in_check = False

class Move():
    def __init__(self,start_sq,end_sq,type,promote_to = ""):
        self.start_sq = start_sq
        self.end_sq = end_sq
        self.type = type
        self.promote_to = promote_to

#Print Board
def print_board(b):
    for row in range(8):
        print(b.board[row*8:(row+1)*8])
    print()

def row(index):
  return (index // 8) + 1
#Note: Row 1 = Rank 8, Row 2 = Rank 7......Row 8 = Rank 1

def is_empty(square):
    return True if square == "." else False
#Check if a square is empty

def is_valid_target(index):
    return True if 0<= index <=63 else False
#Check if a square actually lies on the chessboard

def in_bounds(index):
    return True if 0<= index <= 7 else False
#Check for ranks and files


def get_pawn_moves(board,index):
    legal_moves = []
    if board.white_to_move:
        target = index - 8  #Square one move in front of pawn
        rank = row(target)
        if rank == 1:   #Promotion
            if is_empty(board.board[target]):   
                for piece in ["N","B","R","Q"]:
                    legal_moves.append(Move(index,target,"Promotion",piece))
            for i in [1,-1]:
                if is_valid_target(target+i):  
                    if row(target+i) == 1 and board.board[target+i].islower():  #Check if the square is on the same rank
                        for piece in ["N","B","R","Q"]:
                            legal_moves.append(Move(index,target+i,"Promotion",piece))
        else:
            if is_empty(board.board[target]):
                legal_moves.append(Move(index,target,"Push"))
                if row(index) == 7 and is_empty(board.board[target-8]): #Check if pawn is on the starting square
                    legal_moves.append(Move(index,target-8,"Double_Push"))
            for i in [1,-1]:
                if row(target+i) == rank and board.board[target+i].islower():   #Check if the square is on the same rank and there is a piece to capture
                    legal_moves.append(Move(index,target+i,"Capture"))
    else:
        target = index + 8  #Square one move in front of pawn
        rank = row(target)
        if rank == 8:   #Promotion
            if is_empty(board.board[target]):
                for piece in ["n","b","r","q"]:
                    legal_moves.append(Move(index,target,"Promotion",piece))
            for i in [1,-1]:
                if is_valid_target(target+i):
                    if row(target+i) == 8 and board.board[target+i].isupper():   #Check if square is on the same rank
                        for piece in ["n","b","r","q"]:
                            legal_moves.append(Move(index,target+i,"Promotion",piece))
        else:
            if is_empty(board.board[target]):
                legal_moves.append(Move(index,target,"Push"))
                if row(index) == 2 and is_empty(board.board[target+8]):   #Check if pawn is on starting square
                    legal_moves.append(Move(index,target+8,"Double_Push"))
            for i in [1,-1]:
                if row(target+i) == rank and board.board[target+i].isupper():   #Check if the square is on the same rank and there is a piece to capture
                    legal_moves.append(Move(index,target+i,"Capture"))
    return legal_moves

def en_passant(board):
    legal_moves = []
    if board.en_passant is not None:
        index = board.en_passant    #Square on which pawn will be after en passant capture
        if board.white_to_move:
            for i in (7,9):   #Checking diagonalally in front of square
                if row(index+i) == row(index+8):    #Checking if square on same rank
                    if board.board[index+i] == "P":
                        legal_moves.append(Move(index+i,index,"EnPassant")) 
        else:
            for i in (-7,-9):   #Checking diagonalally in front of square
                if row(index+i) == row(index-8):   #Checking if square on same rank
                    if board.board[index+i] == "p":
                        legal_moves.append(Move(index+i,index,"EnPassant"))     
    return legal_moves

def get_knight_moves(board,index):
    legal_moves = []
    file = index%8
    rank = index//8
    directions = [[1,2],[1,-2],[-1,2],[-1,-2],[2,1],[2,-1],[-2,1],[-2,-1]]
    for d in directions:    #Move in all 8 directions for Knight
        new_file = file + d[0]
        new_rank = rank + d[1]
        if in_bounds(new_file) and in_bounds(new_rank):   #Check if square in board
            target = new_file + new_rank*8
            if is_empty(board.board[target]):
                legal_moves.append(Move(index,target,"Push"))
            else:
                if board.white_to_move:
                    if board.board[target].islower():
                        legal_moves.append(Move(index,target,"Capture"))
                else:
                     if board.board[target].isupper():
                        legal_moves.append(Move(index,target,"Capture"))
                

    return legal_moves

def get_bishop_moves(board,index):
    legal_moves = []
    file = index%8
    rank = index//8
    directions = [[1,1],[1,-1],[-1,1],[-1,-1]]
    for d in directions:    #Move in all 4 directions for Bishop
        for i in range(1,8):
            new_file = file + d[0]*i
            new_rank = rank + d[1]*i
            if in_bounds(new_file) and in_bounds(new_rank): #Check if square in board
                target = new_file + new_rank*8
                if is_empty(board.board[target]):  
                    legal_moves.append(Move(index,target,"Push"))
                else:
                    if board.white_to_move:
                        if board.board[target].islower():   #Square is valid target only if enemy piece lies on it
                            legal_moves.append(Move(index,target,"Capture"))
                        break   #Break on running into a piece
                    else:
                        if board.board[target].isupper():   #Square is valid target only if enemy piece lies on it
                            legal_moves.append(Move(index,target,"Capture"))
                        break   #Break on running into a piece
            else:
                break   #Break if out of bounds
    
    return legal_moves

def get_rook_moves(board,index):
    legal_moves = []
    file = index%8
    rank = index//8
    directions = [[1,0],[-1,0],[0,1],[0,-1]]
    for d in directions:    #Move in all 4 directions for Rook
        for i in range(1,8):
            new_file = file + d[0]*i
            new_rank = rank + d[1]*i
            if in_bounds(new_file) and in_bounds(new_rank): #Check if square in board
                target = new_file + new_rank*8
                if is_empty(board.board[target]):   
                    legal_moves.append(Move(index,target,"Push"))  
                else:
                    if board.white_to_move:
                        if board.board[target].islower():   #Square is valid target only if enemy piece lies on it
                            legal_moves.append(Move(index,target,"Capture"))
                        break
                    else:
                        if board.board[target].isupper():   #Square is valid target only if enemy piece lies on it
                            legal_moves.append(Move(index,target,"Capture"))
                        break 
            else:
                break   #Break if out of bounds

    return legal_moves

def get_queen_moves(board,index):
    legal_moves = []
    file = index%8
    rank = index//8
    directions = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
    for d in directions:    #Move in all 8 directions for Queen
        for i in range(1,8):
            new_file = file + d[0]*i
            new_rank = rank + d[1]*i
            if in_bounds(new_file) and in_bounds(new_rank): #Check if square in board
                target = new_file + new_rank*8
                if is_empty(board.board[target]):
                    legal_moves.append(Move(index,target,"Push"))
                else:
                    if board.white_to_move:
                        if board.board[target].islower():   #Square is valid target only if enemy piece lies on it
                            legal_moves.append(Move(index,target,"Capture"))
                        break
                    else:
                        if board.board[target].isupper():   #Square is valid target only if enemy piece lies on it
                            legal_moves.append(Move(index,target,"Capture"))
                        break 
                    
            else:
                break

    return legal_moves

def get_king_moves(board,index):
    legal_moves = []
    file = index%8
    rank = index//8
    directions = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
    for d in directions:    #Move in all 8 directions for King
        new_file = file + d[0]
        new_rank = rank + d[1]
        if in_bounds(new_file) and in_bounds(new_rank): #Check if square in board
            target = new_file + new_rank*8
            if is_empty(board.board[target]):
                legal_moves.append(Move(index,target,"Push"))
            else:
                if board.white_to_move:
                    if board.board[target].islower():
                        legal_moves.append(Move(index,target,"Capture"))
                else:
                     if board.board[target].isupper():
                        legal_moves.append(Move(index,target,"Capture"))                 

    return legal_moves

def castling(board):
    if board.in_check:
        return []
    legal_moves = []
    if board.white_to_move:
        if board.white_king_moved is False:
            #Kingside Castling Check
            if board.white_kingside_rook_moved is False and board.board[61] == "." and board.board[62] == ".":
                legal_moves.append(Move(60,62,"Castling"))
            #Queenside Castling Check
            if board.white_queenside_rook_moved is False and  board.board[59] == "." and board.board[58] == "." and board.board[57] == ".":
                legal_moves.append(Move(60,58,"Castling"))
    else:
        if board.black_king_moved is False:
            #Kingside Castling Check
            if board.black_kingside_rook_moved is False and board.board[5] == "." and board.board[6] == ".":
                legal_moves.append(Move(4,6,"Castling"))
            #Queenside Castling Check
            if board.black_queenside_rook_moved is False and  board.board[3] == "." and board.board[2] == "." and board.board[1] == ".":
                legal_moves.append(Move(4,2,"Castling"))
    
    return legal_moves

def get_legal_moves(board):
    board.in_check = in_check(board)
    legal_moves = []
    if board.white_to_move:
        for index in range(len(board.board)):
            if is_empty(board.board[index]) is False and board.board[index].isupper():
                piece = board.board[index]
                if piece =="P":
                    legal_moves.extend(get_pawn_moves(board,index))
                elif piece =="N":
                    legal_moves.extend(get_knight_moves(board,index))
                elif piece =="B":
                    legal_moves.extend(get_bishop_moves(board,index))
                elif piece =="R":
                    legal_moves.extend(get_rook_moves(board,index))
                elif piece =="Q":
                    legal_moves.extend(get_queen_moves(board,index))
                else:
                    legal_moves.extend(get_king_moves(board,index))

    else:
        for index in range(len(board.board)):
            if is_empty(board.board[index]) is False and board.board[index].islower():
                piece = board.board[index]
                if piece =="p":
                    legal_moves.extend(get_pawn_moves(board,index))
                elif piece =="n":
                    legal_moves.extend(get_knight_moves(board,index))
                elif piece =="b":
                    legal_moves.extend(get_bishop_moves(board,index))
                elif piece =="r":
                    legal_moves.extend(get_rook_moves(board,index))
                elif piece =="q":
                    legal_moves.extend(get_queen_moves(board,index))
                else:
                    legal_moves.extend(get_king_moves(board,index))

    legal_moves.extend(castling(board))
    legal_moves.extend(en_passant(board))
    
    return legal_moves

def make_move(board,move):
    board.in_check = in_check(board)
    if move.type == "Promotion":
        board.board[move.end_sq] = move.promote_to
        board.board[move.start_sq] = "."
        if board.board[56] != "R":
            board.white_queenside_rook_moved = True 
        if board.board[63] !="R":
            board.white_kingside_rook_moved = True 
        if board.board[0] != "r":
            board.black_queenside_rook_moved = True 
        if board.board[7] !="r":
            board.black_kingside_rook_moved = True 
        board.white_to_move = False if board.white_to_move else True
        board.en_passant = None
        return
    
    board.board[move.end_sq] = board.board[move.start_sq]
    board.board[move.start_sq] = "."

    if move.type == "Castling":
        if move.end_sq == 62:
            board.board[63] = "."
            board.board[61] = "R"
            board.white_king_moved = True 
        elif move.end_sq == 58:
            board.board[56] = "."
            board.board[59] = "R"
            board.white_king_moved = True 
        elif move.end_sq == 6:
            board.board[7] = "."
            board.board[5] = "r"
            board.black_king_moved = True 
        else:
            board.board[0] = "."
            board.board[3] = "r"
            board.black_king_moved = True 
        board.white_to_move = False if board.white_to_move else True
        board.en_passant = None
        return

    if move.type == "EnPassant":
        if board.white_to_move:
            board.board[move.end_sq+8] = "."
        else:
            board.board[move.end_sq-8] = "."
        board.white_to_move = False if board.white_to_move else True 
        board.en_passant = None
        return

    if board.white_to_move:
        board.en_passant = move.end_sq+8 if move.type =="Double_Push" else None
    else:
        board.en_passant = move.end_sq-8 if move.type =="Double_Push" else None
    if board.board[56] != "R":
        board.white_queenside_rook_moved = True 
    if board.board[63] !="R":
        board.white_kingside_rook_moved = True 
    if board.board[60] != "K":
        board.white_king_moved = True 
    if board.board[0] != "r":
        board.black_queenside_rook_moved = True 
    if board.board[7] !="r":
        board.black_kingside_rook_moved = True 
    if board.board[4] != "k":
        board.black_king_moved = True 

    board.white_to_move = False if board.white_to_move else True

def check_legal(board,move):
    if move.type == "Castling":
        if board.white_to_move is False:
            if move.end_sq == 62:
                checks = [61,62]
            else:
                checks = [58,59]
            for index in checks:
                if row(index) != 1:
                    for i in (-9,-7):
                        if row(index+i) == row(index-8) and index+i >=0:
                            if board.board[index+i] in "kp":
                                return False
                    if board.board[index-8] == "k":
                        return False
                if index < 63:
                    if row(index+1) == row(index):
                        if board.board[index+1] == "k":
                            return False       
                if index > 0:
                    if row(index-1) == row(index):
                        if board.board[index-1] == "k":
                            return False
                if row(index) != 8:
                    for i in (7,9):
                        if row(index+i) == row(index+8) and index+i <=63:
                            if board.board[index+i] == "k":
                                return False
                    if board.board[index+8] == "k":
                        return False
                rank = index//8
                file = index%8
                directions = [[1,2],[1,-2],[-1,2],[-1,-2],[2,1],[2,-1],[-2,1],[-2,-1]]
                for d in directions:
                    new_file = file + d[0]
                    new_rank = rank + d[1]
                    if 0<= new_file <=7 and 0<= new_rank <=7:
                        target = new_file + new_rank*8
                        if board.board[target]== "n":
                            return False
                directions = [[1,1],[1,-1],[-1,1],[-1,-1]]
                for d in directions:
                    for i in range(1,8):
                        new_file = file + d[0]*i
                        new_rank = rank + d[1]*i
                        if in_bounds(new_file) and in_bounds(new_rank):
                            target = new_file + new_rank*8
                            if board.board[target] in "bq":
                                return False
                            elif is_empty(board.board[target]) is False:
                                break
                        else:
                            break
                directions = [[1,0],[-1,0],[0,1],[0,-1]]
                for d in directions:
                    for i in range(1,8):
                        new_file = file + d[0]*i
                        new_rank = rank + d[1]*i
                        if in_bounds(new_file) and in_bounds(new_rank):
                            target = new_file + new_rank*8
                            if board.board[target] in "rq":
                                return False
                            elif is_empty(board.board[target]) is False:
                                break
                        else:
                            break
                
        else:
            if move.end_sq == 6:
                checks = [5,6]
            else:
                checks = [2,3]
            for index in checks:
                file = index%8
                if row(index) != 1:
                    for i in (-9,-7):
                        if row(index+i) == row(index-8) and index+i >-1:
                            if board.board[index+i] in "K":
                                return False
                    if board.board[index-8] == "K":
                        return False
                if index < 63:
                    if row(index+1) == row(index):
                        if board.board[index+1] == "K":
                            return False 
                if index > 0:
                    if row(index-1) == row(index):
                        if board.board[index-1] == "K":
                            return False
                if row(index) != 8:
                    for i in (7,9):
                        if row(index+i) == row(index+8) and index+i <64:
                            if board.board[index+i] in "KP":
                                return False
                    if board.board[index+8] == "K":
                        return False
                rank = index//8
                directions = [[1,2],[1,-2],[-1,2],[-1,-2],[2,1],[2,-1],[-2,1],[-2,-1]]
                for d in directions:
                    new_file = file + d[0]
                    new_rank = rank + d[1]
                    if in_bounds(new_file) and in_bounds(new_rank):
                        target = new_file + new_rank*8
                        if board.board[target]== "N":
                            return False
                directions = [[1,1],[1,-1],[-1,1],[-1,-1]]
                for d in directions:
                    for i in range(1,8):
                        new_file = file + d[0]*i
                        new_rank = rank + d[1]*i
                        if in_bounds(new_file) and in_bounds(new_rank):
                            target = new_file + new_rank*8
                            if board.board[target] in "BQ":
                                return False
                            elif is_empty(board.board[target]) is False:
                                break
                        else:
                            break
                directions = [[1,0],[-1,0],[0,1],[0,-1]]
                for d in directions:
                    for i in range(1,8):
                        new_file = file + d[0]*i
                        new_rank = rank + d[1]*i
                        if in_bounds(new_file) and in_bounds(new_rank):
                            target = new_file + new_rank*8
                            if board.board[target] in "RQ":
                                return False
                            elif is_empty(board.board[target]) is False:
                                break
                        else:
                            break

    #returns True if legal False if illegal
    if board.white_to_move is False:
        index = np.argmax(board.board == "K")
        file = index%8
        if row(index) != 1:
            for i in (-9,-7):
                if row(index+i) == row(index-8) and index+i > -1:
                    if board.board[index+i] in "kp":
                        return False
            if board.board[index-8] == "k":
                return False
            
        if index < 63:
            if row(index+1) == row(index):
                if board.board[index+1] == "k":
                    return False
                
        if index > 0:
            if row(index-1) == row(index):
                if board.board[index-1] == "k":
                    return False
        if row(index) != 8:
            for i in (7,9):
                if row(index+i) == row(index+8) and index+i <64:
                    if board.board[index+i] == "k":
                        return False
            if board.board[index+8] == "k":
                return False
        rank = index//8
        directions = [[1,2],[1,-2],[-1,2],[-1,-2],[2,1],[2,-1],[-2,1],[-2,-1]]
        for d in directions:
            new_file = file + d[0]
            new_rank = rank + d[1]
            if in_bounds(new_file) and in_bounds(new_rank):
                target = new_file + new_rank*8
                if board.board[target]== "n":
                    return False
        directions = [[1,1],[1,-1],[-1,1],[-1,-1]]
        for d in directions:
            for i in range(1,8):
                new_file = file + d[0]*i
                new_rank = rank + d[1]*i
                if in_bounds(new_file) and in_bounds(new_rank):
                    target = new_file + new_rank*8
                    if board.board[target] in "bq":
                        return False
                    elif is_empty(board.board[target]) is False:
                        break
                else:
                    break
        directions = [[1,0],[-1,0],[0,1],[0,-1]]
        for d in directions:
            for i in range(1,8):
                new_file = file + d[0]*i
                new_rank = rank + d[1]*i
                if in_bounds(new_file) and in_bounds(new_rank):
                    target = new_file + new_rank*8
                    if board.board[target] in "rq":
                        return False
                    elif is_empty(board.board[target]) is False:
                        break
                else:
                    break
    else:
        index = np.argmax(board.board == "k")
        file = index%8
        if row(index) != 1:
            for i in (-9,-7):
                if row(index+i) == row(index-8) and index+i > -1:
                    if board.board[index+i] in "K":
                        return False
            if board.board[index-8] == "K":
                return False
        if index < 63:
            if row(index+1) == row(index):
                if board.board[index+1] == "K":
                    return False
                
        if index > 0:
            if row(index-1) == row(index):
                if board.board[index-1] == "K":
                    return False
        if row(index) != 8:
            for i in (7,9):
                if row(index+i) == row(index+8) and index+i <64:
                    if board.board[index+i] in "KP":
                        return False
            if board.board[index+8] == "K":
                return False
        rank = index//8
        directions = [[1,2],[1,-2],[-1,2],[-1,-2],[2,1],[2,-1],[-2,1],[-2,-1]]
        for d in directions:
            new_file = file + d[0]
            new_rank = rank + d[1]
            if in_bounds(new_file) and in_bounds(new_rank):
                target = new_file + new_rank*8
                if board.board[target]== "N":
                    return False
        directions = [[1,1],[1,-1],[-1,1],[-1,-1]]
        for d in directions:
            for i in range(1,8):
                new_file = file + d[0]*i
                new_rank = rank + d[1]*i
                if in_bounds(new_file) and in_bounds(new_rank):
                    target = new_file + new_rank*8
                    if board.board[target] in "BQ":
                        return False
                    elif is_empty(board.board[target]) is False:
                        break
                else:
                    break
        directions = [[1,0],[-1,0],[0,1],[0,-1]]
        for d in directions:
            for i in range(1,8):
                new_file = file + d[0]*i
                new_rank = rank + d[1]*i
                if in_bounds(new_file) and in_bounds(new_rank):
                    target = new_file + new_rank*8
                    if board.board[target] in "RQ":
                        return False
                    elif is_empty(board.board[target]) is False:
                        break
                else:
                    break
        
    return True     

def in_check(board):
    #returns True if in check else False
    if board.white_to_move:
        index = np.argmax(board.board == "K")
        file = index%8
        if row(index) != 1:
            for i in (-9,-7):
                if row(index+i) == row(index-8) and index+i > -1:
                    if board.board[index+i] in "kp":
                        return True
            if board.board[index-8] == "k":
                return True
            
        if index < 63:
            if row(index+1) == row(index):
                if board.board[index+1] == "k":
                    return True
                
        if index > 0:
            if row(index-1) == row(index):
                if board.board[index-1] == "k":
                    return True
        if row(index) != 8:
            for i in (7,9):
                if row(index+i) == row(index+8) and index+i <64:
                    if board.board[index+i] == "k":
                        return True
            if board.board[index+8] == "k":
                return True
        rank = index//8
        directions = [[1,2],[1,-2],[-1,2],[-1,-2],[2,1],[2,-1],[-2,1],[-2,-1]]
        for d in directions:
            new_file = file + d[0]
            new_rank = rank + d[1]
            if in_bounds(new_file) and in_bounds(new_rank):
                target = new_file + new_rank*8
                if board.board[target]== "n":
                    return True
        directions = [[1,1],[1,-1],[-1,1],[-1,-1]]
        for d in directions:
            for i in range(1,8):
                new_file = file + d[0]*i
                new_rank = rank + d[1]*i
                if in_bounds(new_file) and in_bounds(new_rank):
                    target = new_file + new_rank*8
                    if board.board[target] in "bq":
                        return True
                    elif is_empty(board.board[target]) is False:
                        break
                else:
                    break
        directions = [[1,0],[-1,0],[0,1],[0,-1]]
        for d in directions:
            for i in range(1,8):
                new_file = file + d[0]*i
                new_rank = rank + d[1]*i
                if in_bounds(new_file) and in_bounds(new_rank):
                    target = new_file + new_rank*8
                    if board.board[target] in "rq":
                        return True
                    elif is_empty(board.board[target]) is False:
                        break
                else:
                    break
    else:
        index = np.argmax(board.board == "k")
        file = index%8
        if row(index) != 1:
            for i in (-9,-7):
                if row(index+i) == row(index-8) and index+i > -1:
                    if board.board[index+i] in "K":
                        return True
            if board.board[index-8] == "K":
                return True
        if index < 63:
            if row(index+1) == row(index):
                if board.board[index+1] == "K":
                    return True
                
        if index > 0:
            if row(index-1) == row(index):
                if board.board[index-1] == "K":
                    return True
        if row(index) != 8:
            for i in (7,9):
                if row(index+i) == row(index+8) and index+i <64:
                    if board.board[index+i] in "KP":
                        return True
            if board.board[index+8] == "K":
                return True
        rank = index//8
        directions = [[1,2],[1,-2],[-1,2],[-1,-2],[2,1],[2,-1],[-2,1],[-2,-1]]
        for d in directions:
            new_file = file + d[0]
            new_rank = rank + d[1]
            if in_bounds(new_file) and in_bounds(new_rank):
                target = new_file + new_rank*8
                if board.board[target]== "N":
                    return True
        directions = [[1,1],[1,-1],[-1,1],[-1,-1]]
        for d in directions:
            for i in range(1,8):
                new_file = file + d[0]*i
                new_rank = rank + d[1]*i
                if in_bounds(new_file) and in_bounds(new_rank):
                    target = new_file + new_rank*8
                    if board.board[target] in "BQ":
                        return True
                    elif is_empty(board.board[target]) is False:
                        break
                else:
                    break
        directions = [[1,0],[-1,0],[0,1],[0,-1]]
        for d in directions:
            for i in range(1,8):
                new_file = file + d[0]*i
                new_rank = rank + d[1]*i
                if in_bounds(new_file) and in_bounds(new_rank):
                    target = new_file + new_rank*8
                    if board.board[target] in "RQ":
                        return True
                    elif is_empty(board.board[target]) is False:
                        break
                else:
                    break
        
        return False   

pst = {"P" : np.array([0, 0, 0, 0, 0, 0, 0, 0, 98, 134, 61, 95, 68, 126, 34, -11, -6, 7, 26, 31, 65, 56, 25, -20, -14, 13, 6, 21, 23, 12, 17, -23, -27, -2, -5, 12, 17, 6, 10, -25, -26, -4, -4, -10, 3, 3, 33, -12, -35, -1, -20, -23, -15, 24, 38, -22, 0, 0, 0, 0, 0, 0, 0, 0]),
          "p" : np.array([0, 0, 0, 0, 0, 0, 0, 0, -35, -1, -20, -23, -15, 24, 38, -22, -26, -4, -4, -10, 3, 3, 33, -12, -27, -2, -5, 12, 17, 6, 10, -25, -14, 13, 6, 21, 23, 12, 17, -23, -6, 7, 26, 31, 65, 56, 25, -20, 98, 134, 61, 95, 68, 126, 34, -11, 0, 0, 0, 0, 0, 0, 0, 0]),
          "N" : np.array([-167, -89, -34, -49, 61, -97, -15, -107, -73, -41, 72, 36, 23, 62, 7, -17, -47, 60, 37, 65, 84, 129, 73, 44, -9, 17, 19, 53, 37, 69, 18, 22, -13, 4, 16, 13, 28, 19, 21, -8, -23, -9, 12, 10, 19, 17, 25, -16, -29, -53, -12, -3, -1, 18, -14, -19, -105, -21, -58, -33, -17, -28, -19, -230]),
          "n" : np.array([-105, -21, -58, -33, -17, -28, -19, -230, -29, -53, -12, -3, -1, 18, -14, -19, -23, -9, 12, 10, 19, 17, 25, -16, -13, 4, 16, 13, 28, 19, 21, -8, -9, 17, 19, 53, 37, 69, 18, 22, -47, 60, 37, 65, 84, 129, 73, 44, -73, -41, 72, 36, 23, 62, 7, -17, -167, -89, -34, -49, 61, -97, -15, -107]),
          "B" : np.array([-29, 4, -82, -37, -25, -42, 7, -8, -26, 16, -18, -13, 30, 59, 18, -47, -16, 37, 43, 40, 35, 50, 37, -2, -4, 5, 19, 50, 37, 37, 7, -2, -6, 13, 13, 26, 34, 12, 10, 4, 0, 15, 15, 15, 14, 27, 18, 10, 4, 15, 16, 0, 7, 21, 33, 1, -33, -3, -14, -21, -13, -12, -39, -21]),
          "b" : np.array([-33, -3, -14, -21, -13, -12, -39, -21, 4, 15, 16, 0, 7, 21, 33, 1, 0, 15, 15, 15, 14, 27, 18, 10, -6, 13, 13, 26, 34, 12, 10, 4, -4, 5, 19, 50, 37, 37, 7, -2, -16, 37, 43, 40, 35, 50, 37, -2, -26, 16, -18, -13, 30, 59, 18, -47, -29, 4, -82, -37, -25, -42, 7, -8]),
          "R" : np.array([32, 42, 32, 51, 63, 9, 31, 43, 27, 32, 58, 62, 80, 67, 26, 44, -5, 19, 26, 36, 17, 45, 61, 16, -24, -11, 7, 26, 24, 35, -8, -20, -36, -26, -12, -1, 9, -7, 6, -23, -45, -25, -16, -17, 3, 0, -5, -33, -44, -16, -20, -9, -1, 11, -6, -71, -19, -13, 1, 17, 16, 7, -37, -26]),
          "r" : np.array([-19, -13, 1, 17, 16, 7, -37, -26, -44, -16, -20, -9, -1, 11, -6, -71, -45, -25, -16, -17, 3, 0, -5, -33, -36, -26, -12, -1, 9, -7, 6, -23, -24, -11, 7, 26, 24, 35, -8, -20, -5, 19, 26, 36, 17, 45, 61, 16, 27, 32, 58, 62, 80, 67, 26, 44, 32, 42, 32, 51, 63, 9, 31, 43]),
          "Q" : np.array([-28, 0, 29, 12, 59, 44, 43, 45, -24, -39, -5, 1, -16, 57, 28, 54, -13, -17, 7, 8, 29, 56, 47, 57, -27, -27, -16, -16, -1, 17, -2, 1, -9, -26, -9, -10, -2, -4, 3, -3, -14, 2, -11, -2, -5, 2, 14, 5, -35, -8, 11, 2, 8, 15, -3, 1, -1, -18, -9, 10, -15, -25, -31, -50]),
          "q" : np.array([-1, -18, -9, 10, -15, -25, -31, -50, -35, -8, 11, 2, 8, 15, -3, 1, -14, 2, -11, -2, -5, 2, 14, 5, -9, -26, -9, -10, -2, -4, 3, -3, -27, -27, -16, -16, -1, 17, -2, 1, -13, -17, 7, 8, 29, 56, 47, 57, -24, -39, -5, 1, -16, 57, 28, 54, -28, 0, 29, 12, 59, 44, 43, 45]),
          "K" : np.array([-65, 23, 16, -15, -56, -34, 2, 13, 29, -1, -20, -7, -8, -4, -38, -29, -9, 24, 2, -16, -20, 6, 22, -22, -17, -20, -12, -27, -30, -25, -14, -36, -49, -1, -27, -39, -46, -44, -33, -51, -14, -14, -22, -46, -44, -30, -15, -27, 1, 7, -8, -64, -43, -16, 9, 8, -15, 36, 12, -54, 8, -28, 24, 14]),
          "k" : np.array([-15, 36, 12, -54, 8, -28, 24, 14, 1, 7, -8, -64, -43, -16, 9, 8, -14, -14, -22, -46, -44, -30, -15, -27, -49, -1, -27, -39, -46, -44, -33, -51, -17, -20, -12, -27, -30, -25, -14, -36, -9, 24, 2, -16, -20, 6, 22, -22, 29, -1, -20, -7, -8, -4, -38, -29, -65, 23, 16, -15, -56, -34, 2, 13])
          }

piece_value = {"p" : 82, "n": 337, "b" : 365, "r" : 477, "q" : 1025, "k" : 1000000}
def evaluate(board):
    white_score = 0
    black_score = 0
    for i in range(0,64):
        if is_empty(board.board[i]) is False:
            if board.board[i].isupper():
                white_score += piece_value[board.board[i].lower()]
                white_score += pst[board.board[i]][i]
            else:
                black_score += piece_value[board.board[i]]
                black_score += pst[board.board[i]][i]
    return (white_score-black_score)/100

board = Board("rnb1k1nr/ppp2ppp/8/4P3/1BP5/3q4/PP2KpPP/RN1Q1BNR w kq - 0 1")

def negamax(board,depth,ply,alpha,beta):
    if depth == 0:
        return evaluate(board),None

    max_eval = -10000000000 
    best_move = None
    searched = 0
    moves = get_legal_moves(board)
    for move in moves:
        test_board = Board(None,
                            board.board.copy(),
                            board.white_to_move,
                            board.white_king_moved,
                            board.white_kingside_rook_moved,
                            board.white_queenside_rook_moved,
                            board.black_king_moved,
                            board.black_kingside_rook_moved,
                            board.black_queenside_rook_moved,
                            board.en_passant,
                            board.moves_since_capture,
                            board.in_check)
        make_move(test_board, move)
        result = check_legal(test_board, move)
        if not result:
            continue
        searched += 1
        eval, _ =  negamax(test_board, depth-1, ply+1, -beta, -alpha)
        eval = -eval

        if eval > max_eval:
            max_eval = eval
            best_move = move
        
        alpha = max(alpha, max_eval)
        if beta <= alpha:
            break 
    if searched == 0:
        if not board.in_check:
            return 0, None
        else:
            return -10000000000+ply,None
    return max_eval, best_move

# types = ["Push","Double_Push","Capture","Castling","En_Passant"]
# while True:
#     a = negamax(board,4,-float('inf'),float('inf'))
#     print(a[0],index_to_square[a[1].start_sq]+index_to_square[a[1].end_sq])
#     make_move(board,a[1])
#     print()
#     start_sq = input("Start_sq: ")
#     end_sq = input("End_sq: ")
#     type = int(input("1: Push\n2: Double_Push\n3: Capture\n4: Castling\n5: En_Passant\n"))
#     type_ = types[type-1]
#     promote_to = input("Promote to: ")
#     make_move(board,Move(square_to_index[start_sq],square_to_index[end_sq],type_,promote_to))
#     print()


a = negamax(board,4,0,-10000000000,10000000000)
print(a[0],index_to_square[a[1].start_sq]+index_to_square[a[1].end_sq])
