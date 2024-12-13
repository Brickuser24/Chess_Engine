import numpy as np
import random

class Board():
    def __init__(self,fen = None,board = None,white_to_move = None,white_king_moved = None,
                 white_kingside_rook_moved = None,white_queenside_rook_moved = None,
                 black_king_moved = None,black_kingside_rook_moved = None,black_queenside_rook_moved = None,
                 en_passant = None,moves_since_capture = None):
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
            #Difference along diagonal = 9
            #Difference along files    = 1
            #Difference along ranks    = 8

            self.white_to_move = True if white_to_move is None else white_to_move

            #Info for Castling
            self.white_king_moved = False if white_king_moved is None else white_king_moved
            self.white_kingside_rook_moved = False if white_kingside_rook_moved is None else white_kingside_rook_moved
            self.white_queenside_rook_moved = False if white_queenside_rook_moved is None else white_queenside_rook_moved

            self.black_king_moved = False if black_king_moved is None else black_king_moved
            self.black_kingside_rook_moved = False if black_kingside_rook_moved is None else black_kingside_rook_moved
            self.black_queenside_rook_moved = False if black_queenside_rook_moved is None else black_queenside_rook_moved

            self.en_passant = None if en_passant is None else en_passant
            
            self.moves_since_capture = 0 if moves_since_capture is None else moves_since_capture
        
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
            #Needs to be properly coded
            self.en_passant = None
            self.moves_since_capture = int(fields[4])

class Move():
    def __init__(self,start_sq,end_sq,type,promote_to = None):
        self.start_sq = start_sq
        self.end_sq = end_sq
        self.type = type
        self.promote_to = promote_to

def get_pawn_moves(board,index,color):
    legal_moves = []
    if color == "W": 
        target = index - 8
        if 1<= target <=7:
            if board[target] == ".":
                for piece in ["N","B","R","Q"]:
                    legal_moves.append(Move(index,target,"Promotion",piece))
            file = (target//8)*8
            for i in [1,-1]:
                if file<= target+i <=file+7:
                    if board[target+i].islower():
                        for piece in ["N","B","R","Q"]:
                            legal_moves.append(Move(index,target+i,"Promotion",piece))
        else:
            if board[target] == ".":
                legal_moves.append(Move(index,target,"Push"))
                if 48<= index <=55 and board[target-8] == ".":
                    legal_moves.append(Move(index,target-8,"Double_Push"))
            file = (target//8)*8
            for i in [1,-1]:
                if file<= target+i <=file+7:
                    if board[target+i].islower():
                        legal_moves.append(Move(index,target+i,"Capture"))
    else:
        target = index + 8
        if 56<= target <=63:
            if board[target] == ".":
                for piece in ["N","B","R","Q"]:
                    legal_moves.append(Move(index,target,"Promotion",piece))
            file = (target//8)*8
            for i in [1,-1]:
                if file<= target+i <=file+7:
                    if board[target+i].isupper():
                        for piece in ["N","B","R","Q"]:
                            legal_moves.append(Move(index,target+i,"Promotion",piece))
        else:
            if board[target] == ".":
                legal_moves.append(Move(index,target,"Push"))
                if 8<= index <=15 and board[target+8] == ".":
                    legal_moves.append(Move(index,target+8,"Push"))
            file = (target//8)*8
            for i in [1,-1]:
                if file<= target+i <=file+7:
                    if board[target+i].isupper():
                        legal_moves.append(Move(index,target+i,"Capture"))
    
    return legal_moves

def get_knight_moves(board,index,color):
    legal_moves = []
    file = index%8
    rank = index//8
    directions = [[1,2],[1,-2],[-1,2],[-1,-2],[2,1],[2,-1],[-2,1],[-2,-1]]
    for d in directions:
        new_file = file + d[0]
        new_rank = rank + d[1]
        if 0<= new_file <=7 and 0<= new_rank <=7:
            target = new_file + new_rank*8
            if board[target]!= ".":
                if color == "W":
                    if board[target].islower():
                        legal_moves.append(Move(index,target,"Capture"))
                else:
                     if board[target].isupper():
                        legal_moves.append(Move(index,target,"Capture"))
            else:
                legal_moves.append(Move(index,target,"Push"))

    return legal_moves

def get_bishop_moves(board,index,color):
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
                if board[target]!= ".":
                    if color == "W":
                        if board[target].islower():
                            legal_moves.append(Move(index,target,"Capture"))
                        break
                    else:
                        if board[target].isupper():
                            legal_moves.append(Move(index,target,"Capture"))
                        break 
                else:
                    legal_moves.append(Move(index,target,"Push"))
            else:
                break
    
    return legal_moves

def get_rook_moves(board,index,color):
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
                if board[target]!= ".":
                    if color == "W":
                        if board[target].islower():
                            legal_moves.append(Move(index,target,"Capture"))
                        break
                    else:
                        if board[target].isupper():
                            legal_moves.append(Move(index,target,"Capture"))
                        break 
                else:
                    legal_moves.append(Move(index,target,"Push"))
            else:
                break

    return legal_moves

def get_queen_moves(board,index,color):
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
                if board[target]!= ".":
                    if color == "W":
                        if board[target].islower():
                            legal_moves.append(Move(index,target,"Capture"))
                        break
                    else:
                        if board[target].isupper():
                            legal_moves.append(Move(index,target,"Capture"))
                        break 
                else:
                    legal_moves.append(Move(index,target,"Push"))
            else:
                break

    return legal_moves

def get_king_moves(board,index,color):
    legal_moves = []
    file = index%8
    rank = index//8
    directions = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
    for d in directions:
        new_file = file + d[0]
        new_rank = rank + d[1]
        if 0<= new_file <=7 and 0<= new_rank <=7:
            target = new_file + new_rank*8
            if board[target]!= ".":
                if color == "W":
                    if board[target].islower():
                        legal_moves.append(Move(index,target,"Capture"))
                else:
                     if board[target].isupper():
                        legal_moves.append(Move(index,target,"Capture")) 
            else:
                legal_moves.append(Move(index,target,"Push"))

    return legal_moves
    
def castling(board,turn):
    legal_moves = []
    if turn == "W":
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

def en_passant(board,turn):
    legal_moves = []
    if board.en_passant is not None:
        square = board.en_passant
        file = (square//8)*8
        if turn =="W":
            for i in (1,-1):
                if file<= square+i <= file+7:
                    if board.board[square+i] == "P":
                        legal_moves.append(Move(square+i,square-8,"EnPassant"))
                       
        else:
            for i in (1,-1):
                if file<= square+i <= file+7:
                    if board.board[square+i] == "P":
                        legal_moves.append(Move(square+i,square+8,"EnPassant"))

    return legal_moves

def get_legal_moves(board,turn):
    legal_moves = []
    if turn == "W":
        for index in range(len(board.board)):
            if board.board[index]!= "." and board.board[index].isupper():
                piece = board.board[index]
                if piece =="P":
                    legal_moves.extend(get_pawn_moves(board.board,index,turn))
                elif piece =="N":
                    legal_moves.extend(get_knight_moves(board.board,index,turn))
                elif piece =="B":
                    legal_moves.extend(get_bishop_moves(board.board,index,turn))
                elif piece =="R":
                    legal_moves.extend(get_rook_moves(board.board,index,turn))
                elif piece =="Q":
                    legal_moves.extend(get_queen_moves(board.board,index,turn))
                else:
                    legal_moves.extend(get_king_moves(board.board,index,turn))

    else:
        for index in range(len(board.board)):
            if board.board[index]!= "." and board.board[index].islower():
                piece = board.board[index]
                if piece =="p":
                    legal_moves.extend(get_pawn_moves(board.board,index,turn))
                elif piece =="n":
                    legal_moves.extend(get_knight_moves(board.board,index,turn))
                elif piece =="b":
                    legal_moves.extend(get_bishop_moves(board.board,index,turn))
                elif piece =="r":
                    legal_moves.extend(get_rook_moves(board.board,index,turn))
                elif piece =="q":
                    legal_moves.extend(get_queen_moves(board.board,index,turn))
                else:
                    legal_moves.extend(get_king_moves(board.board,index,turn))

    legal_moves.extend(castling(board,turn))
    legal_moves.extend(en_passant(board,turn))
    
    return legal_moves

def make_move(board,move,turn):
    board.board[move.end_sq] = board.board[move.start_sq]
    board.board[move.start_sq] = "."
    board.en_passant = None
    if turn == "W":
        if board.board[56] != "R":
            board.white_queenside_rook_moved = True 
        if board.board[63] !="R":
            board.white_kingside_rook_moved = True 
        if board.board[60] != "K":
            board.white_king_moved = True 
    else:
        if board.board[0] != "R":
            board.black_queenside_rook_moved = True 
        if board.board[7] !="R":
            board.black_kingside_rook_moved = True 
        if board.board[4] != "K":
            board.black_king_moved = True 

    board.white_to_move = False if board.white_to_move else True
    board.moves_since_capture = 0 if move.type == "Capture" else board.moves_since_capture + 1
    
def check_legal(board,turn):
    #returns True if legal False if illegal
    if turn == "W":
        index = np.argmax(board.board == "K")
        file = (index//8)*8
        for i in (-9,-7):
            if file<= index + i <=file + 7:
                if board.board[index+i] in "kp":
                    print("King/Pawn found")
                    return False
        for i in (-8,-1,+1,+7,+8,+9):
            if file<= index + i <=file + 7:
                if board.board[index+i] == "k":
                    print("King found")
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
                    print("Knight found")
                    return False
        directions = [[1,1],[1,-1],[-1,1],[-1,-1]]
        for d in directions:
            for i in range(1,8):
                new_file = file + d[0]*i
                new_rank = rank + d[1]*i
                if 0<= new_file <=7 and 0<= new_rank <=7:
                    target = new_file + new_rank*8
                    if board.board[target] in "bq":
                        print("Queen/Bishop found")
                        return False
                    elif board.board[target].isupper():
                        break
        directions = [[1,0],[-1,0],[0,1],[0,-1]]
        for d in directions:
            for i in range(1,8):
                new_file = file + d[0]*i
                new_rank = rank + d[1]*i
                if 0<= new_file <=7 and 0<= new_rank <=7:
                    target = new_file + new_rank*8
                    if board.board[target] in "rq":
                        return print("Rook/Queen found")
                    elif board.board[target].isupper():
                        break
    else:
        index = np.argmax(board.board == "k")
        file = (index//8)*8
        for i in (+9,+7):
            if file<= index + i <=file + 7:
                if board.board[index+i] in "KP":
                    print("King/Pawn found")
                    return False
        for i in (-8,-1,+1,+7,+8,+9):
            if file<= index + i <=file + 7:
                if board.board[index+i] == "K":
                    print("King found")
                    return False
        rank = index//8
        file = index%8
        directions = [[1,2],[1,-2],[-1,2],[-1,-2],[2,1],[2,-1],[-2,1],[-2,-1]]
        for d in directions:
            new_file = file + d[0]
            new_rank = rank + d[1]
            if 0<= new_file <=7 and 0<= new_rank <=7:
                target = new_file + new_rank*8
                if board.board[target]== "N":
                    print("Knight found")
                    return False
        directions = [[1,1],[1,-1],[-1,1],[-1,-1]]
        for d in directions:
            for i in range(1,8):
                new_file = file + d[0]*i
                new_rank = rank + d[1]*i
                if 0<= new_file <=7 and 0<= new_rank <=7:
                    target = new_file + new_rank*8
                    if board.board[target] in "BQ":
                        print("B/Q found")
                        return False
                    elif board.board[target].islower():
                        break
        directions = [[1,0],[-1,0],[0,1],[0,-1]]
        for d in directions:
            for i in range(1,8):
                new_file = file + d[0]*i
                new_rank = rank + d[1]*i
                if 0<= new_file <=7 and 0<= new_rank <=7:
                    target = new_file + new_rank*8
                    if board.board[target] in "RQ":
                        print("R/Q found")
                        return False
                    elif board.board[target].islower():
                        break
        
        return True
                        
            


board = Board("r1bqkbnr/pppppppp/2n5/8/8/2P5/PP1PPPPP/RNBQKBNR w KQkq - 1 2")


#FEN GENERATION

# rows = [board.board[i:i+8] for i in range(0, 64, 8)]
# a=[]
# for row in rows:
#     string = ""
#     empty=0
#     for j in row:
#         if j == ".":
#             empty+=1
#         else:
#             if empty !=0:
#                 string+=str(empty)
#             empty = 0
#             string+=j
#     string+=str(empty)
#     a.append(string)
# fen="/".join(a) +" "
# fen+= "w " if board.white_to_move else "b "
# fen+="K" if board.white_king_moved is False and board.white_kingside_rook_moved is False else ""
# fen+="Q" if board.white_king_moved is False and board.white_queenside_rook_moved is False else ""
# fen+="k" if board.black_king_moved is False and board.black_kingside_rook_moved is False else ""
# fen+="q" if board.black_king_moved is False and board.black_queenside_rook_moved is False else ""
# fen+= " - "
# fen+= f"{board.moves_since_capture} "
# fen+= "6"
# print(fen)



#PERFT TEST

def perft(position,depth):
    if depth == 0:
        return 1
    
    nodes = 0
    turn = "W" if position.white_to_move else "B"
    moves = get_legal_moves(position,turn)
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
        make_move(test_board,move,turn)
        result = check_legal(test_board,turn)
        if result is False:
            continue
        nodes += perft(test_board, depth - 1)
    
    return nodes

d = {
    0: "a8", 1: "b8", 2: "c8", 3: "d8", 4: "e8", 5: "f8", 6: "g8", 7: "h8",
    8: "a7", 9: "b7", 10: "c7", 11: "d7", 12: "e7", 13: "f7", 14: "g7", 15: "h7",
    16: "a6", 17: "b6", 18: "c6", 19: "d6", 20: "e6", 21: "f6", 22: "g6", 23: "h6",
    24: "a5", 25: "b5", 26: "c5", 27: "d5", 28: "e5", 29: "f5", 30: "g5", 31: "h5",
    32: "a4", 33: "b4", 34: "c4", 35: "d4", 36: "e4", 37: "f4", 38: "g4", 39: "h4",
    40: "a3", 41: "b3", 42: "c3", 43: "d3", 44: "e3", 45: "f3", 46: "g3", 47: "h3",
    48: "a2", 49: "b2", 50: "c2", 51: "d2", 52: "e2", 53: "f2", 54: "g2", 55: "h2",
    56: "a1", 57: "b1", 58: "c1", 59: "d1", 60: "e1", 61: "f1", 62: "g1", 63: "h1"
}



moves = get_legal_moves(board,"W" if board.white_to_move else "B")
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
                            board.moves_since_capture
                            )
    make_move(test_board,move,"W" if board.white_to_move else "B")
    num = perft(test_board,1)
    nodes += num
    print(f"{d[move.start_sq]}{d[move.end_sq]}: {num}")
print(nodes)



#CHECK LEGAL MOVE FUNCTION TESTING

# moves = get_legal_moves(board,"B")
# for move in moves:
#     test_board = Board (None, 
#                             board.board.copy(),
#                             board.white_to_move,
#                             board.white_king_moved,
#                             board.white_kingside_rook_moved,
#                             board.white_queenside_rook_moved,
#                             board.black_king_moved,
#                             board.black_kingside_rook_moved,
#                             board.black_queenside_rook_moved,
#                             board.en_passant,
#                             board.moves_since_capture
#                             )
#     make_move(test_board,move,"B")
#     a = check_legal(test_board,"B")
#     if a is False:
#         print(f"{d[move.start_sq]}{d[move.end_sq]}")
