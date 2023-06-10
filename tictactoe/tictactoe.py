"""
Tic Tac Toe Player
"""

import math
import copy
from random import randint
X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    Xs = 0
    Os = 0
    for row in board:
        Xs += row.count(X)
        Os += row.count(O)
    if(Xs == Os): return X
    else: return O
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    #stores all Possible actions
    PA = set()

    for r in range(3):
        for c in range(3):
            if board[r][c] == EMPTY:
                PA.add((r,c))

    return PA
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    New_board = copy.deepcopy(board)
    turn = player(board)
    if(New_board[action[0]][action[1]] != EMPTY):
        raise Exception("Invalid Move")

    New_board[action[0]][action[1]] = turn
    return New_board
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #List of all winning combinations
   
    #checking rows and columns
    for i in range(3): 
        # row check
        if (board[i][0] == board[i][1] == board[i][2] != EMPTY):
            return board[i][0]
        # column check
        if (board[0][i] == board[1][i] == board[2][i] != EMPTY):
            return board[0][i]
    
    # diagonals check  
    if (board[0][0] == board[1][1] == board[2][2] != EMPTY):
        return board[1][1]
    if  (board[0][2] == board[1][1] == board[2][0] != EMPTY):
        return board[1][1]
    
    
    return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    if winner(board) != None:       # A player won
        return True
    elif len(actions(board)) == 0:  # game tied
        return True
    else: return False              # Not a terminal state
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    #get Winner
    Win_player = winner(board)

    #return corresponing utility
    if(Win_player == X):
        return 1
    elif(Win_player == O):
        return -1
    else: return 0

    raise NotImplementedError

def min_player(board):
    """
    Return Minimum possible utility with current board
    """
    #(board state == terminal state) -> return utility
    if terminal(board):
        return utility(board)
    
    val = math.inf
    #minimize val by choosing optimal move
    for action in actions(board):
        val = min(val,max_player(result(board,action)))
        #pruning
        if(val == -1):
            return val

    #return minimum utility
    return val

def max_player(board):
    """
    Return Maximum possible utility with current board
    """

    # return utility of terminal state
    if terminal(board):
        return utility(board)
    
    
    val = -math.inf

    #maximize val by choosing optimal move
    for action in actions(board):
        val = max(val,min_player(result(board,action)))
        #pruning
        if(val == 1):
            return val 
    
    #return maximum utility
    return val
        
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #Game Over
    if terminal(board):
        return None
    
    #Optimal Move
    move = None

    #first move - Random
    if len(actions(board)) == 9 :
        move = (randint(0,2),randint(0,2))
        return move
    
    #Maximizing player's turn
    if player(board) == X:
        max_val = -math.inf

        #iterate over possible actions - get the best move
        for action in actions(board):
            val = min_player(result(board,action))
            
            #Update to better a move 
            if(val > max_val):
                max_val = val
                move = action 
                #pruning
                if(max_val == 1):
                    return move
        
        #return best move
        return move
    
    #Minimizing player's turn
    elif player(board) == O:
        min_val = math.inf

        #iterate over possible actions - get the best move
        for action in actions(board):
            val = max_player(result(board,action))

            #Update to better a move 
            if(val <= min_val):
                min_val = val
                move = action
                #pruning
                if(min_val == -1):
                    return move 
       
        #return best move
        return move
    
    raise NotImplementedError
