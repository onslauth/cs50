"""
Tic Tac Toe Player
"""

import math
import copy

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

    count = 0
    for r in board:
        for c in r:
            if c == EMPTY:
                count += 1

    if count % 2 != 0:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    options = [ ]
    for i in range( len( board ) ):
        for j in range( len( board[ i ] ) ):
            if board[ i ][ j ] == EMPTY:
                options.append( ( i, j ) )

    return options


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    new_board = copy.deepcopy( board )

    """
    new_board = [ ]
    for r in board:
        row = [ ]
        for c in r:
            if c == X:
                row.append( X )
            elif c == O:
                row.append( O )
            else:
                row.append( EMPTY )
            row.append( c )
        new_board.append( row )
    """


    marker = player( board )
    i = action[ 0 ]
    j = action[ 1 ]
    new_board[ i ][ j ] = marker

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Rows
    if board[ 0 ][ 0 ] == board[ 0 ][ 1 ] == board[ 0 ][ 2] and board[ 0 ][ 0 ] != EMPTY:
        return board[ 0 ][ 0 ]
    elif board[ 1 ][ 0 ] == board[ 1 ][ 1 ] == board[ 1 ][ 2 ] and board[ 1 ][ 0 ] != EMPTY:
        return board[ 1 ][ 0 ]
    elif board[ 2 ][ 0 ] == board[ 2 ][ 1 ] == board[ 2 ][ 2 ] and board[ 2 ][ 0 ] != EMPTY:
        return board[ 2 ][ 0 ]

    # Cols
    elif board[ 0 ][ 0 ] == board[ 1 ][ 0 ] == board[ 2 ][ 0 ] and board[ 0 ][ 0 ] != EMPTY:
        return board[ 0 ][ 0 ]
    elif board[ 0 ][ 1 ] == board[ 1 ][ 1 ] == board[ 2 ][ 1 ] and board[ 0 ][ 1 ] != EMPTY:
        return board[ 0 ][ 1 ]
    elif board[ 0 ][ 2 ] == board[ 1 ][ 2 ] == board[ 2 ][ 2 ] and board[ 0 ][ 2 ] != EMPTY:
        return board[ 0 ][ 2 ]

    # Diagonals
    elif board[ 0 ][ 0 ] == board[ 1 ][ 1 ] == board[ 2 ][ 2 ] and board[ 0 ][ 0 ] != EMPTY:
        return board[ 0 ][ 0 ]
    elif board[ 0 ][ 2 ] == board[ 1 ][ 1 ] == board[ 2 ][ 0 ] and board[ 0 ][ 2 ] != EMPTY:
        return board[ 0 ][ 2 ]

    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner( board ) != None:
        return True

    count = 0
    for r in board:
        for c in r:
            if c == EMPTY:
                count += 1

    return count == 0


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    current = winner( board )
    if current == None:
        return 0
    else:
        if current == X:
            return 1
        else:
            return -1

def print_board( board ):
    print( "| - - - |" )
    print( f"| { board[ 0 ][ 0 ] } { board[ 0 ][ 1 ] } { board[ 0 ][ 2 ] } |" ) 
    print( f"| { board[ 1 ][ 0 ] } { board[ 1 ][ 1 ] } { board[ 1 ][ 2 ] } |" ) 
    print( f"| { board[ 2 ][ 0 ] } { board[ 2 ][ 1 ] } { board[ 2 ][ 2 ] } |" ) 
    print( "| - - - |" )


def max_value( board ):

    if terminal( board ):
        return utility( board )

    possible_actions = actions( board )

    best_value  = -2

    for i in possible_actions:
        x = min_value( result( board, i ) )

        if x > best_value:
            best_value  = x

    return best_value

def min_value( board ):

    if terminal( board ):
        return utility( board )

    possible_actions = actions( board )

    best_value  = 2

    for i in possible_actions:
        x = max_value( result( board, i ) )

        if x < best_value:
            best_value = x

    return best_value

def max_action( board ):
    possible_actions = actions( board )

    best_action = None
    best_value = -2

    for i in possible_actions:
        x = min_value( result( board, i ) )
        if x > best_value:
            best_value = x
            best_action = i

    return best_action

def min_action( board ):
    possible_actions = actions( board )

    best_action = None
    best_value = 2

    for i in possible_actions:
        x = max_value( result( board, i ) )
        if x < best_value:
            best_value = x
            best_action = i

    return best_action

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal( board ):
        return None

    if player( board ) == X:
        return max_action( board )
    else:
        return min_action( board )

    
