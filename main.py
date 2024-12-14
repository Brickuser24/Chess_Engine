import numpy as np
import time as t

#Note
#ADD PROMOTIONS IN MAKE MOVE

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
                "r","n","b","q","k","b","n","r",        #  0  1  2  3  4  5  6  7
                "p","p","p","p","p","p","p","p",        #  8  9 10 11 12 13 14 15
                ".",".",".",".",".",".",".",".",        # 16 17 18 19 20 21 22 23
                ".",".",".",".",".",".",".",".",        # 24 25 26 27 28 29 30 31
                ".",".",".",".",".",".",".",".",        # 32 33 34 35 36 37 38 39
                ".",".",".",".",".",".",".",".",        # 40 41 42 43 44 45 46 47
                "P","P","P","P","P","P","P","P",        # 48 49 50 51 52 53 54 55
                "R","N","B","Q","K","B","N","R"         # 56 57 58 59 60 61 62 63
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
                        spaces=[]
                        for i in range(int(char)):
                            spaces.append(".")
                        formatted_rank.extend(spaces)
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

def row(index):
    if 0<= index <= 7:
        return 1
    elif 8<= index <= 15:
        return 2
    elif 16<= index <= 23:
        return 3
    elif 24<= index <= 31:
        return 4
    elif 32<= index <= 39:
        return 5
    elif 40<= index <= 47:
        return 6
    elif 48<= index <= 55:
        return 7
    else:
        return 8

def get_pawn_moves(board,index):
    legal_moves = []
    if board.white_to_move: 
        target = index - 8
        if row(target) == 1:
            if board.board[target] == ".":
                for piece in ["N","B","R","Q"]:
                    legal_moves.append(Move(index,target,"Promotion",piece))
            rank = row((target//8)*8)
            for i in [1,-1]:
                if 0<= target+i <=63:
                    if row(target+i) == rank:
                        if board.board[target+i].islower():
                            for piece in ["N","B","R","Q"]:
                                legal_moves.append(Move(index,target+i,"Promotion",piece))
        else:
            if board.board[target] == ".":
                legal_moves.append(Move(index,target,"Push"))
                if row(index) == 7 and board.board[target-8] == ".":
                    legal_moves.append(Move(index,target-8,"Double_Push"))
            rank = row((target//8)*8)
            for i in [1,-1]:
                if 0<= target+i <=63:
                    if row(target+i) == rank:
                        if board.board[target+i].islower():
                            legal_moves.append(Move(index,target+i,"Capture"))
    else:
        target = index + 8
        if row(target) == 8:
            if board.board[target] == ".":
                for piece in ["n","b","r","q"]:
                    legal_moves.append(Move(index,target,"Promotion",piece))
            rank = row((target//8)*8)
            for i in [1,-1]:
                if 0<= target+i <=63:
                    if row(target+i) == rank:
                        if board.board[target+i].isupper():
                            for piece in ["n","b","r","q"]:
                                legal_moves.append(Move(index,target+i,"Promotion",piece))
        else:
            if board.board[target] == ".":
                legal_moves.append(Move(index,target,"Push"))
                if row(index) == 2 and board.board[target+8] == ".":
                    legal_moves.append(Move(index,target+8,"Double_Push"))
            rank = row((target//8)*8)
            for i in [1,-1]:
                if 0<= target+i <=63:
                    if row(target+i) == rank:
                        if board.board[target+i].isupper():
                            legal_moves.append(Move(index,target+i,"Capture"))
    
    return legal_moves

def en_passant(board):
    legal_moves = []
    if board.en_passant is not None:
        square = board.en_passant
        file = (square//8)*8
        if board.white_to_move:
            for i in (7,9):
                if row(file+8) == row(square+i):
                    if board.board[square+i] == "P":
                        legal_moves.append(Move(square+i,square,"EnPassant"))
                       
        else:
            for i in (-7,-9):
                if row(file-8) == row(square+i):
                    if board.board[square+i] == "p":
                        legal_moves.append(Move(square+i,square,"EnPassant"))

    return legal_moves

def get_knight_moves(board,index):
    legal_moves = []
    file = index%8
    rank = index//8
    directions = [[1,2],[1,-2],[-1,2],[-1,-2],[2,1],[2,-1],[-2,1],[-2,-1]]
    for d in directions:
        new_file = file + d[0]
        new_rank = rank + d[1]
        if 0<= new_file <=7 and 0<= new_rank <=7:
            target = new_file + new_rank*8
            if board.board[target]!= ".":
                if board.white_to_move:
                    if board.board[target].islower():
                        legal_moves.append(Move(index,target,"Capture"))
                else:
                     if board.board[target].isupper():
                        legal_moves.append(Move(index,target,"Capture"))
            else:
                legal_moves.append(Move(index,target,"Push"))

    return legal_moves

def get_bishop_moves(board,index):
    legal_moves = []
    file = index%8
    rank = index//8
    directions = [[1,1],[1,-1],[-1,1],[-1,-1]]
    for d in directions:
        for i in range(1,8):
            new_file = file + d[0]*i
            new_rank = rank + d[1]*i
            if 0<= new_file <=7 and 0<= new_rank <=7:
                target = new_file + new_rank*8
                if board.board[target]!= ".":
                    if board.white_to_move:
                        if board.board[target].islower():
                            legal_moves.append(Move(index,target,"Capture"))
                        break
                    else:
                        if board.board[target].isupper():
                            legal_moves.append(Move(index,target,"Capture"))
                        break 
                else:
                    legal_moves.append(Move(index,target,"Push"))
            else:
                break
    
    return legal_moves

def get_rook_moves(board,index):
    legal_moves = []
    file = index%8
    rank = index//8
    directions = [[1,0],[-1,0],[0,1],[0,-1]]
    for d in directions:
        for i in range(1,8):
            new_file = file + d[0]*i
            new_rank = rank + d[1]*i
            if 0<= new_file <=7 and 0<= new_rank <=7:
                target = new_file + new_rank*8
                if board.board[target]!= ".":
                    if board.white_to_move:
                        if board.board[target].islower():
                            legal_moves.append(Move(index,target,"Capture"))
                        break
                    else:
                        if board.board[target].isupper():
                            legal_moves.append(Move(index,target,"Capture"))
                        break 
                else:
                    legal_moves.append(Move(index,target,"Push"))
            else:
                break

    return legal_moves

def get_queen_moves(board,index):
    legal_moves = []
    file = index%8
    rank = index//8
    directions = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
    for d in directions:
        for i in range(1,8):
            new_file = file + d[0]*i
            new_rank = rank + d[1]*i
            if 0<= new_file <=7 and 0<= new_rank <=7:
                target = new_file + new_rank*8
                if board.board[target]!= ".":
                    if board.white_to_move:
                        if board.board[target].islower():
                            legal_moves.append(Move(index,target,"Capture"))
                        break
                    else:
                        if board.board[target].isupper():
                            legal_moves.append(Move(index,target,"Capture"))
                        break 
                else:
                    legal_moves.append(Move(index,target,"Push"))
            else:
                break

    return legal_moves

def get_king_moves(board,index):
    legal_moves = []
    file = index%8
    rank = index//8
    directions = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
    for d in directions:
        new_file = file + d[0]
        new_rank = rank + d[1]
        if 0<= new_file <=7 and 0<= new_rank <=7:
            target = new_file + new_rank*8
            if board.board[target]!= ".":
                if board.white_to_move:
                    if board.board[target].islower():
                        legal_moves.append(Move(index,target,"Capture"))
                else:
                     if board.board[target].isupper():
                        legal_moves.append(Move(index,target,"Capture")) 
            else:
                legal_moves.append(Move(index,target,"Push"))

    return legal_moves

def castling(board):
    legal_moves = []
    if board.in_check:
        return legal_moves
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
    legal_moves = []
    if board.white_to_move:
        for index in range(len(board.board)):
            if board.board[index]!= "." and board.board[index].isupper():
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
            if board.board[index]!= "." and board.board[index].islower():
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
    if move.type == "Promotion":
        board.board[move.end_sq] = move.promote_to
    else:
        board.board[move.end_sq] = board.board[move.start_sq]
    board.board[move.start_sq] = "."
    if move.type == "Castling":
        if move.end_sq == 62:
            board.board[63] = "."
            board.board[61] = "R"
        elif move.end_sq == 58:
            board.board[56] = "."
            board.board[59] = "R"
        elif move.end_sq == 6:
            board.board[7] = "."
            board.board[5] = "r"
        else:
            board.board[0] = "."
            board.board[3] = "r"
    if move.type == "EnPassant":
        if board.white_to_move:
            board.board[move.end_sq+8] = "."
        else:
            board.board[move.end_sq-8] = "."
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
    board.moves_since_capture = 0 if move.type == "Capture" else board.moves_since_capture + 1

def check_legal(board,move):
    if move.type == "Castling":
        if board.white_to_move is False:
            if move.end_sq == 62:
                checks = [61,62]
            else:
                checks = [58,59]
            for index in checks:
                file = index%8
                if row(index) != 1:
                    for i in (-9,-7):
                        if row(index+i) == row(index-8) and index+i >-1:
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
                    if 0<= new_file <=7 and 0<= new_rank <=7:
                        target = new_file + new_rank*8
                        if board.board[target]== "n":
                            return False
                directions = [[1,1],[1,-1],[-1,1],[-1,-1]]
                for d in directions:
                    for i in range(1,8):
                        new_file = file + d[0]*i
                        new_rank = rank + d[1]*i
                        if 0<= new_file <=7 and 0<= new_rank <=7:
                            target = new_file + new_rank*8
                            if board.board[target] in "bq":
                                return False
                            elif board.board[target] != ".":
                                break
                directions = [[1,0],[-1,0],[0,1],[0,-1]]
                for d in directions:
                    for i in range(1,8):
                        new_file = file + d[0]*i
                        new_rank = rank + d[1]*i
                        if 0<= new_file <=7 and 0<= new_rank <=7:
                            target = new_file + new_rank*8
                            if board.board[target] in "rq":
                                return False
                            elif board.board[target] != ".":
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
                    if 0<= new_file <=7 and 0<= new_rank <=7:
                        target = new_file + new_rank*8
                        if board.board[target]== "N":
                            return False
                directions = [[1,1],[1,-1],[-1,1],[-1,-1]]
                for d in directions:
                    for i in range(1,8):
                        new_file = file + d[0]*i
                        new_rank = rank + d[1]*i
                        if 0<= new_file <=7 and 0<= new_rank <=7:
                            target = new_file + new_rank*8
                            if board.board[target] in "BQ":
                                return False
                            elif board.board[target] != ".":
                                break
                directions = [[1,0],[-1,0],[0,1],[0,-1]]
                for d in directions:
                    for i in range(1,8):
                        new_file = file + d[0]*i
                        new_rank = rank + d[1]*i
                        if 0<= new_file <=7 and 0<= new_rank <=7:
                            target = new_file + new_rank*8
                            if board.board[target] in "RQ":
                                return False
                            elif board.board[target] != ".":
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
            if 0<= new_file <=7 and 0<= new_rank <=7:
                target = new_file + new_rank*8
                if board.board[target]== "n":
                    return False
        directions = [[1,1],[1,-1],[-1,1],[-1,-1]]
        for d in directions:
            for i in range(1,8):
                new_file = file + d[0]*i
                new_rank = rank + d[1]*i
                if 0<= new_file <=7 and 0<= new_rank <=7:
                    target = new_file + new_rank*8
                    if board.board[target] in "bq":
                        return False
                    elif board.board[target] != ".":
                        break
        directions = [[1,0],[-1,0],[0,1],[0,-1]]
        for d in directions:
            for i in range(1,8):
                new_file = file + d[0]*i
                new_rank = rank + d[1]*i
                if 0<= new_file <=7 and 0<= new_rank <=7:
                    target = new_file + new_rank*8
                    if board.board[target] in "rq":
                        return False
                    elif board.board[target] != ".":
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
            if 0<= new_file <=7 and 0<= new_rank <=7:
                target = new_file + new_rank*8
                if board.board[target]== "N":
                    return False
        directions = [[1,1],[1,-1],[-1,1],[-1,-1]]
        for d in directions:
            for i in range(1,8):
                new_file = file + d[0]*i
                new_rank = rank + d[1]*i
                if 0<= new_file <=7 and 0<= new_rank <=7:
                    target = new_file + new_rank*8
                    if board.board[target] in "BQ":
                        return False
                    elif board.board[target] != ".":
                        break
        directions = [[1,0],[-1,0],[0,1],[0,-1]]
        for d in directions:
            for i in range(1,8):
                new_file = file + d[0]*i
                new_rank = rank + d[1]*i
                if 0<= new_file <=7 and 0<= new_rank <=7:
                    target = new_file + new_rank*8
                    if board.board[target] in "RQ":
                        return False
                    elif board.board[target] != ".":
                        break
        
        return True

def in_check(board):
        #returns True if legal False if illegal
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
            if 0<= new_file <=7 and 0<= new_rank <=7:
                target = new_file + new_rank*8
                if board.board[target]== "n":
                    return True
        directions = [[1,1],[1,-1],[-1,1],[-1,-1]]
        for d in directions:
            for i in range(1,8):
                new_file = file + d[0]*i
                new_rank = rank + d[1]*i
                if 0<= new_file <=7 and 0<= new_rank <=7:
                    target = new_file + new_rank*8
                    if board.board[target] in "bq":
                        return True
                    elif board.board[target] != ".":
                        break
        directions = [[1,0],[-1,0],[0,1],[0,-1]]
        for d in directions:
            for i in range(1,8):
                new_file = file + d[0]*i
                new_rank = rank + d[1]*i
                if 0<= new_file <=7 and 0<= new_rank <=7:
                    target = new_file + new_rank*8
                    if board.board[target] in "rq":
                        return True
                    elif board.board[target] != ".":
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
            if 0<= new_file <=7 and 0<= new_rank <=7:
                target = new_file + new_rank*8
                if board.board[target]== "N":
                    return True
        directions = [[1,1],[1,-1],[-1,1],[-1,-1]]
        for d in directions:
            for i in range(1,8):
                new_file = file + d[0]*i
                new_rank = rank + d[1]*i
                if 0<= new_file <=7 and 0<= new_rank <=7:
                    target = new_file + new_rank*8
                    if board.board[target] in "BQ":
                        return True
                    elif board.board[target] != ".":
                        break
        directions = [[1,0],[-1,0],[0,1],[0,-1]]
        for d in directions:
            for i in range(1,8):
                new_file = file + d[0]*i
                new_rank = rank + d[1]*i
                if 0<= new_file <=7 and 0<= new_rank <=7:
                    target = new_file + new_rank*8
                    if board.board[target] in "RQ":
                        return True
                    elif board.board[target] != ".":
                        break
        
        return False



#Print Board
def print_board(b):
    for row in range(8):
        print(b.board[row*8:(row+1)*8])
    print()


#PERFT TEST

def perft(position,depth):
    if depth == 0:
        return 1
    
    nodes = 0
    turn = "W" if position.white_to_move else "B"
    position.in_check = in_check(position)
    moves = get_legal_moves(position)
    for move in moves:
        test_board = Board (None, 
                            position.board.copy(),
                            position.white_to_move,
                            position.white_king_moved,
                            position.white_kingside_rook_moved,
                            position.white_queenside_rook_moved,
                            position.black_king_moved,
                            position.black_kingside_rook_moved,
                            position.black_queenside_rook_moved,
                            position.en_passant,
                            position.moves_since_capture
                            )
        make_move(test_board,move)
        result = check_legal(test_board,move)
        if result is False:
            # print(move.start_sq,move.end_sq)
            # print_board(test_board)
            # t.sleep(3)
            continue
        nodes += perft(test_board, depth - 1)
    
    return nodes


#FENS TEST

# fens = {'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1': 197281, 'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1': 4085603, '4k3/8/8/8/8/8/8/4K2R w K - 0 1': 7059, '4k3/8/8/8/8/8/8/R3K3 w Q - 0 1': 7626, '4k2r/8/8/8/8/8/8/4K3 w k - 0 1': 8290, 'r3k3/8/8/8/8/8/8/4K3 w q - 0 1': 8897, '4k3/8/8/8/8/8/8/R3K2R w KQ - 0 1': 17945, 'r3k2r/8/8/8/8/8/8/4K3 w kq - 0 1': 22180, '8/8/8/8/8/8/6k1/4K2R w K - 0 1': 2219, '8/8/8/8/8/8/1k6/R3K3 w Q - 0 1': 4573, '4k2r/6K1/8/8/8/8/8/8 w k - 0 1': 2073, 'r3k3/1K6/8/8/8/8/8/8 w q - 0 1': 3991, 'r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1': 314346, 'r3k2r/8/8/8/8/8/8/1R2K2R w Kkq - 0 1': 328965, 'r3k2r/8/8/8/8/8/8/2R1K2R w Kkq - 0 1': 312835, 'r3k2r/8/8/8/8/8/8/R3K1R1 w Qkq - 0 1': 316214, '1r2k2r/8/8/8/8/8/8/R3K2R w KQk - 0 1': 334705, '2r1k2r/8/8/8/8/8/8/R3K2R w KQk - 0 1': 317324, 'r3k1r1/8/8/8/8/8/8/R3K2R w KQq - 0 1': 320792, '4k3/8/8/8/8/8/8/4K2R b K - 0 1': 8290, '4k3/8/8/8/8/8/8/R3K3 b Q - 0 1': 8897, '4k2r/8/8/8/8/8/8/4K3 b k - 0 1': 7059, 'r3k3/8/8/8/8/8/8/4K3 b q - 0 1': 7626, '4k3/8/8/8/8/8/8/R3K2R b KQ - 0 1': 22180, 'r3k2r/8/8/8/8/8/8/4K3 b kq - 0 1': 17945, '8/8/8/8/8/8/6k1/4K2R b K - 0 1': 2073, '8/8/8/8/8/8/1k6/R3K3 b Q - 0 1': 3991, '4k2r/6K1/8/8/8/8/8/8 b k - 0 1': 2219, 'r3k3/1K6/8/8/8/8/8/8 b q - 0 1': 4573, 'r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 1': 314346, 'r3k2r/8/8/8/8/8/8/1R2K2R b Kkq - 0 1': 334705, 'r3k2r/8/8/8/8/8/8/2R1K2R b Kkq - 0 1': 317324, 'r3k2r/8/8/8/8/8/8/R3K1R1 b Qkq - 0 1': 320792, '1r2k2r/8/8/8/8/8/8/R3K2R b KQk - 0 1': 328965, '2r1k2r/8/8/8/8/8/8/R3K2R b KQk - 0 1': 312835, 'r3k1r1/8/8/8/8/8/8/R3K2R b KQq - 0 1': 316214, '8/1n4N1/2k5/8/8/5K2/1N4n1/8 w - - 0 1': 38675, '8/1k6/8/5N2/8/4n3/8/2K5 w - - 0 1': 20534, '8/8/4k3/3Nn3/3nN3/4K3/8/8 w - - 0 1': 73584, 'K7/8/2n5/1n6/8/8/8/k6N w - - 0 1': 5301, 'k7/8/2N5/1N6/8/8/8/K6n w - - 0 1': 5910, '8/1n4N1/2k5/8/8/5K2/1N4n1/8 b - - 0 1': 40039, '8/1k6/8/5N2/8/4n3/8/2K5 b - - 0 1': 24640, '8/8/3K4/3Nn3/3nN3/4k3/8/8 b - - 0 1': 16199, 'K7/8/2n5/1n6/8/8/8/k6N b - - 0 1': 5910, 'k7/8/2N5/1N6/8/8/8/K6n b - - 0 1': 5301, 'B6b/8/8/8/2K5/4k3/8/b6B w - - 0 1': 76778, '8/8/1B6/7b/7k/8/2B1b3/7K w - - 0 1': 93338, 'k7/B7/1B6/1B6/8/8/8/K6b w - - 0 1': 32955, 'K7/b7/1b6/1b6/8/8/8/k6B w - - 0 1': 31787, 'B6b/8/8/8/2K5/5k2/8/b6B b - - 0 1': 31151, '8/8/1B6/7b/7k/8/2B1b3/7K b - - 0 1': 93603, 'k7/B7/1B6/1B6/8/8/8/K6b b - - 0 1': 31787, 'K7/b7/1b6/1b6/8/8/8/k6B b - - 0 1': 32955, '7k/RR6/8/8/8/8/rr6/7K w - - 0 1': 104342, 'R6r/8/8/2K5/5k2/8/8/r6R w - - 0 1': 771461, '7k/RR6/8/8/8/8/rr6/7K b - - 0 1': 104342, 'R6r/8/8/2K5/5k2/8/8/r6R b - - 0 1': 771368, '6kq/8/8/8/8/8/8/7K w - - 0 1': 3637, '6KQ/8/8/8/8/8/8/7k b - - 0 1': 3637, 'K7/8/8/3Q4/4q3/8/8/7k w - - 0 1': 8349, '6qk/8/8/8/8/8/8/7K b - - 0 1': 4167, 'K7/8/8/3Q4/4q3/8/8/7k b - - 0 1': 8349, '8/8/8/8/8/K7/P7/k7 w - - 0 1': 199, '8/8/8/8/8/7K/7P/7k w - - 0 1': 199, 'K7/p7/k7/8/8/8/8/8 w - - 0 1': 80, '7K/7p/7k/8/8/8/8/8 w - - 0 1': 80, '8/2k1p3/3pP3/3P2K1/8/8/8/8 w - - 0 1': 1091, '8/8/8/8/8/K7/P7/k7 b - - 0 1': 80, '8/8/8/8/8/7K/7P/7k b - - 0 1': 80, 'K7/p7/k7/8/8/8/8/8 b - - 0 1': 199, '7K/7p/7k/8/8/8/8/8 b - - 0 1': 199, '8/2k1p3/3pP3/3P2K1/8/8/8/8 b - - 0 1': 1091, '8/8/8/8/8/4k3/4P3/4K3 w - - 0 1': 282, '4k3/4p3/4K3/8/8/8/8/8 b - - 0 1': 282, '8/8/7k/7p/7P/7K/8/8 w - - 0 1': 360, '8/8/k7/p7/P7/K7/8/8 w - - 0 1': 360, '8/8/3k4/3p4/3P4/3K4/8/8 w - - 0 1': 1294, '8/3k4/3p4/8/3P4/3K4/8/8 w - - 0 1': 3213, '8/8/3k4/3p4/8/3P4/3K4/8 w - - 0 1': 3213, 'k7/8/3p4/8/3P4/8/8/7K w - - 0 1': 534, '8/8/7k/7p/7P/7K/8/8 b - - 0 1': 360, '8/8/k7/p7/P7/K7/8/8 b - - 0 1': 360, '8/8/3k4/3p4/3P4/3K4/8/8 b - - 0 1': 1294, '8/3k4/3p4/8/3P4/3K4/8/8 b - - 0 1': 3213, '8/8/3k4/3p4/8/3P4/3K4/8 b - - 0 1': 3213, 'k7/8/3p4/8/3P4/8/8/7K b - - 0 1': 537, '7k/3p4/8/8/3P4/8/8/K7 w - - 0 1': 720, '7k/8/8/3p4/8/8/3P4/K7 w - - 0 1': 716, 'k7/8/8/7p/6P1/8/8/K7 w - - 0 1': 877, 'k7/8/7p/8/8/6P1/8/K7 w - - 0 1': 637, 'k7/8/8/6p1/7P/8/8/K7 w - - 0 1': 877, 'k7/8/6p1/8/8/7P/8/K7 w - - 0 1': 637, 'k7/8/8/3p4/4p3/8/8/7K w - - 0 1': 573, 'k7/8/3p4/8/8/4P3/8/7K w - - 0 1': 637, '7k/3p4/8/8/3P4/8/8/K7 b - - 0 1': 720, '7k/8/8/3p4/8/8/3P4/K7 b - - 0 1': 712, 'k7/8/8/7p/6P1/8/8/K7 b - - 0 1': 877, 'k7/8/7p/8/8/6P1/8/K7 b - - 0 1': 637, 'k7/8/8/6p1/7P/8/8/K7 b - - 0 1': 877, 'k7/8/6p1/8/8/7P/8/K7 b - - 0 1': 637, 'k7/8/8/3p4/4p3/8/8/7K b - - 0 1': 569, 'k7/8/3p4/8/8/4P3/8/7K b - - 0 1': 637, '7k/8/8/p7/1P6/8/8/7K w - - 0 1': 877, '7k/8/p7/8/8/1P6/8/7K w - - 0 1': 637, '7k/8/8/1p6/P7/8/8/7K w - - 0 1': 877, '7k/8/1p6/8/8/P7/8/7K w - - 0 1': 637, 'k7/7p/8/8/8/8/6P1/K7 w - - 0 1': 1035, 'k7/6p1/8/8/8/8/7P/K7 w - - 0 1': 1035, '3k4/3pp3/8/8/8/8/3PP3/3K4 w - - 0 1': 2902, '7k/8/8/p7/1P6/8/8/7K b - - 0 1': 877, '7k/8/p7/8/8/1P6/8/7K b - - 0 1': 637, '7k/8/8/1p6/P7/8/8/7K b - - 0 1': 877, '7k/8/1p6/8/8/P7/8/7K b - - 0 1': 637, 'k7/7p/8/8/8/8/6P1/K7 b - - 0 1': 1035, 'k7/6p1/8/8/8/8/7P/K7 b - - 0 1': 1035, '3k4/3pp3/8/8/8/8/3PP3/3K4 b - - 0 1': 2902, '8/Pk6/8/8/8/8/6Kp/8 w - - 0 1': 8048, 'n1n5/1Pk5/8/8/8/8/5Kp1/5N1N w - - 0 1': 124608, '8/PPPk4/8/8/8/8/4Kppp/8 w - - 0 1': 79355, 'n1n5/PPPk4/8/8/8/8/4Kppp/5N1N w - - 0 1': 182838, '8/Pk6/8/8/8/8/6Kp/8 b - - 0 1': 8048, 'n1n5/1Pk5/8/8/8/8/5Kp1/5N1N b - - 0 1': 124608, '8/PPPk4/8/8/8/8/4Kppp/8 b - - 0 1': 79355, 'n1n5/PPPk4/8/8/8/8/4Kppp/5N1N b - - 0 1': 182838}
# with open("FEN Testing Results.txt","w") as f:
#     for fen in fens:
#         board = Board(fen)
#         board.in_check = in_check(board)
#         moves = get_legal_moves(board)
#         nodes = 0
#         for move in moves:
#             test_board = Board (None, 
#                                     board.board.copy(),
#                                     board.white_to_move,
#                                     board.white_king_moved,
#                                     board.white_kingside_rook_moved,
#                                     board.white_queenside_rook_moved,
#                                     board.black_king_moved,
#                                     board.black_kingside_rook_moved,
#                                     board.black_queenside_rook_moved,
#                                     board.en_passant,
#                                     board.moves_since_capture,
#                                     board.in_check
#                                     )
#             make_move(test_board,move)
#             result = check_legal(test_board,move)
#             if result is False:
#                 continue
#             num = perft(test_board,3)
#             nodes += num
#             #print(f"{index_to_square[move.start_sq]}{index_to_square[move.end_sq]}{move.promote_to}: {num}")
#         if nodes != fens[fen]:
#             f.write(fen+": Error\n")
#             f.flush()
#         else:
#             f.write(fen+": Success\n")
#             f.flush()
#     f.close()





t1 = t.perf_counter()
board = Board("rnbqkb1r/ppppp1pp/7n/4Pp2/8/8/PPPP1PPP/RNBQKBNR w KQkq f6 0 3")
board.in_check = in_check(board)
moves = get_legal_moves(board)
nodes = 0
for move in moves:
    test_board = Board (None, 
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
                            board.in_check
                            )
    make_move(test_board,move)
    result = check_legal(test_board,move)
    if result is False:
        continue
    num = perft(test_board,4)
    nodes += num

    #print(f"{index_to_square[move.start_sq]}{index_to_square[move.end_sq]}{move.promote_to}: {num}")

t2=t.perf_counter()
print(nodes)
print(nodes/(t2-t1))
