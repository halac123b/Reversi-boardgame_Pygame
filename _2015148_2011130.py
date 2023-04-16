import time
import random as rd

DEPTH = 4
def make_move(board, row, col, turn):
    new_board = [row[:] for row in board]
            
    new_board[row][col] = turn
            
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
                    
            r = row + i
            c = col + j
            flipped = False
            to_flip = []
                    
            while r >= 0 and r < 8 and c >= 0 and c < 8:
                if new_board[r][c] == 0:
                    break
                if new_board[r][c] == turn:
                    flipped = True
                    break
                to_flip.append((r, c))
                r += i
                c += j
                    
            if flipped:
                for (r, c) in to_flip:
                    new_board[r][c] = turn
            
    return new_board

def is_valid_move(board, row, col, turn):
    if board[row][col] != 0:
        return False
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            r = row + i
            c = col + j
            found_opponent = False
            while r >= 0 and r < 8 and c >= 0 and c < 8:
                if board[r][c] == 0:
                    break
                if board[r][c] == turn:
                    if found_opponent:
                        return True
                    break
                found_opponent = True
                r += i
                c += j
    return False
def get_valid_moves(board, turn):
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if is_valid_move(board, row, col, turn):
                valid_moves.append((row, col))
    return valid_moves

def random_agent(cur_state, player_to_move, remain_time):
    valid_moves = get_valid_moves(cur_state,player_to_move)
    if valid_moves == []: return None
    else: return rd.choice(valid_moves)
    
def move_by_yourself(cur_state, player_to_move, remain_time):
    valid_moves = get_valid_moves(cur_state,player_to_move)
    if valid_moves == []: return None
    print(valid_moves)
    a = int(input())
    return valid_moves[a]

#This is my code (Hoai)
def getMove(array):
    moves = 0
    for x in range(8):
        for y in range(8):
            if array[x][y] != 0:
                moves += 1   
    return moves

# def dumbScore(array,player):
#     score = 0
#     for x in range(8):
#         for y in range(8):
#             if array[x][y] == player:
#                 score += 1
#             elif array[x][y] == -player:
#                 score -= 1
#     return score   

# def slightlyLessDumbScore(array, player):
#     score = 0
#     for x in range(8):
#         for y in range(8):
#             #setting up normal tile is 1 score
#             add = 1

#             #Edge tiles worth 3
#             if (x==0 and 1<y<6) or (x==7 and 1<y<6) or (y==0 and 1<x<6) or (y==7 and 1<x<6):
#                 add=3
# 			#Corner tiles worth 5
#             elif (x==0 and y==0) or (x==0 and y==7) or (x==7 and y==0) or (x==7 and y==7):
#                 add = 5

#             if array[x][y] == player:
#                 score += add
#             elif array[x][y] == -player:
#                 score -= add
#     return score   

def decentHeuristic(array,player):
    #setting up intial score for the game heuristic
    score = 0
    cornerVal = 25
    adjacentVal = 5
    sideVal = 5
    
    for x in range(8):
        for y in range(8):
            add = 1
            #Adjacent to corners are worth -3
            if (x==0 and y==1) or (x==1 and 0<=y<=1):
                if array[0][0]==player:
                    add = sideVal
                else:
                    add = -adjacentVal
                    
            elif (x==0 and y==6) or (x==1 and 6<=y<=7):
                if array[7][0]==player:
                    add = sideVal
                else:
                    add = -adjacentVal

            elif (x==7 and y==1) or (x==6 and 0<=y<=1):
                if array[0][7]==player:
                    add = sideVal
                else:
                    add = -adjacentVal

            elif (x==7 and y==6) or (x==6 and 6<=y<=7):
                if array[7][7]==player:
                    add = sideVal
                else:
                    add = -adjacentVal
                    
			#Edge tiles worth 3
            elif (x==0 and 1<y<6) or (x==7 and 1<y<6) or (y==0 and 1<x<6) or (y==7 and 1<x<6):
                add=sideVal
			#Corner tiles worth 15
            elif (x==0 and y==0) or (x==0 and y==7) or (x==7 and y==0) or (x==7 and y==7):
                add = cornerVal
			#Add or subtract the value of the tile corresponding to the colour
            if array[x][y] == player:
                score+=add
            elif array[x][y] == -player:
                score-=add
    return score

def finalHeuristic(array,player):
    # moves = getMove(array)
    # if moves <=8:
    #     valid_moves = get_valid_moves(array,player)
    #     return len(valid_moves) + decentHeuristic(array,player)
    # elif moves <= 52:
    #     return decentHeuristic(array,player)
    # elif moves <= 58:
    #     return slightlyLessDumbScore(array,player)
    # else:
    #     return dumbScore(array,player)
    
    #Đống code ở trên chủ yếu là tăng hiệu suất của A.I, nhưng do tôi thấy A.I nó tính toán chưa đến 3s nên không cần tăng hiệu suất
    #Ta có tỉ lệ nghịch: tăng hiệu suất sẽ là giảm khả năng ra quyết định của AI nên cần phải lưu ý vấn đề này
    
    return decentHeuristic(array,player)
        


#We write a code of alpha-beta cutter here
def alphaBeta(cur_state, player_to_move, alpha, beta, remain_time, depth, time_start):
    boards = []
    choices = []

    if time.perf_counter() - time_start >= 2.99:
        return None
    for x in range(8):
        for y in range(8):
            if is_valid_move(cur_state, x, y, player_to_move):
                test = make_move(cur_state, x, y, player_to_move)
                boards.append(test)
                choices.append([x,y])

    if (depth == 0 or len(choices) == 0):
        return [finalHeuristic(cur_state, player_to_move),cur_state, None]  #phai return dong nay

    if player_to_move == 1:
        v = -float("inf")
        bestBoard = []
        bestChoice = []
        for board in boards:
            boardValueArray = alphaBeta(board, -player_to_move, alpha, beta, remain_time, depth - 1, time_start)
            if boardValueArray == None:
                return None
            boardValue = boardValueArray[0]
            if boardValue>v:
                v = boardValue
                bestBoard = board
                bestChoice = (choices[boards.index(board)][0], choices[boards.index(board)][1])
            alpha = max(alpha,v)
            if beta <= alpha:
                break
        return([v,bestBoard,bestChoice])
    
    elif player_to_move == -1:
        v = -float("inf")
        bestBoard = []
        bestChoice = []
        for board in boards:
            boardValueArray = alphaBeta(board, -player_to_move, alpha, beta, remain_time, depth - 1, time_start)
            if boardValueArray == None:
                return None
            boardValue = boardValueArray[0]
            if boardValue>v:
                v = boardValue
                bestBoard = board
                bestChoice = (choices[boards.index(board)][0], choices[boards.index(board)][1])
            alpha = min(alpha,v)
            if beta <= alpha:
                break
        return([v,bestBoard,bestChoice])




def select_move(cur_state, player_to_move, remain_time):
    result = alphaBeta(cur_state, player_to_move, -float("inf"), float("inf"), remain_time, DEPTH, time.perf_counter())

    if result == None:
        print("None")
        return random_agent(cur_state, player_to_move, remain_time)
    return result[2]

