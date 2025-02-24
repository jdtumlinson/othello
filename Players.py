class Player:
    """Base player class"""
    def __init__(self, symbol):
        self.symbol = symbol

    def get_symbol(self):
        return self.symbol
    
    def get_move(self, board):
        raise NotImplementedError()



class HumanPlayer(Player):
    """Human subclass with text input in command line"""
    def __init__(self, symbol):
        Player.__init__(self, symbol)
        self.total_nodes_seen = 0

    def clone(self):
        return HumanPlayer(self.symbol)
        
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)


class AlphaBetaPlayer(Player):
    """Class for Alphabeta AI: implement functions minimax, eval_board, get_successors, get_move
    eval_type: int
        0 for H0, 1 for H1, 2 for H2
    prune: bool
        1 for alpha-beta, 0 otherwise
    max_depth: one move makes the depth of a position to 1, search should not exceed depth
    total_nodes_seen: used to keep track of the number of nodes the algorithm has seearched through
    symbol: X for player 1 and O for player 2
    """
    def __init__(self, symbol, eval_type, prune, max_depth):
        Player.__init__(self, symbol)
        self.eval_type = eval_type
        self.prune = prune
        self.max_depth = int(max_depth) 
        self.max_depth_seen = 0
        self.total_nodes_seen = 0
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'


    def terminal_state(self, board):
        # If either player can make a move, it's not a terminal state
        for c in range(board.cols):
            for r in range(board.rows):
                if board.is_legal_move(c, r, "X") or board.is_legal_move(c, r, "O"):
                    return False 
        return True 


    def terminal_value(self, board):
        # Regardless of X or O, a win is float('inf')
        state = board.count_score(self.symbol) - board.count_score(self.oppSym)
        if state == 0:
            return 0
        elif state > 0:
            return float('inf')
        else:
            return -float('inf')


    def flip_symbol(self, symbol):
        # Short function to flip a symbol
        if symbol == "X":
            return "O"
        else:
            return "X"


    def alphabeta(self, board):
        # Write minimax function here using eval_board and get_successors
        # type:(board) -> (int, int)
        best_move = None
        best_value = -float('inf')

        alpha = -float('inf')
        beta = float('inf')

        for successor, move in self.get_successors_info(board, self.symbol):
            value = self.min_value(successor, 1, alpha, beta)

            if value > best_value:
                best_value = value
                best_move = move
            
            if self.prune:
                alpha = max(alpha, best_value)
            
            self.max_depth_seen += 1

        return best_move if best_move else (0, 0)  # Default move if no legal move found
    

    def max_value(self, board, depth, alpha, beta):
            """Maximizing player function with Alpha-Beta Pruning."""
            if depth >= self.max_depth or self.terminal_state(board):
                return self.eval_board(board)
            
            value = -float('inf')

            for successor, _ in self.get_successors_info(board, self.oppSym):
                value = max(value, self.min_value(successor, depth + 1, alpha, beta))

                self.total_nodes_seen += 1

                if self.prune:
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break  # Beta cutoff
            
            if value == -float('inf'): return self.eval_board(board)
            return value

    def min_value(self, board, depth, alpha, beta):
        """Minimizing player function with Alpha-Beta Pruning."""
        if depth >= self.max_depth or self.terminal_state(board):
            return self.eval_board(board)

        value = float('inf')
        
        for successor, _ in self.get_successors_info(board, self.oppSym):
            value = min(value, self.max_value(successor, depth + 1, alpha, beta))

            self.total_nodes_seen += 1

            if self.prune:
                beta = min(beta, value)
                if beta <= alpha:
                    break  # Alpha cutoff
        
        if value == float('inf'): return self.eval_board(board)
        return value


    def eval_board(self, board):
        # Write eval function here
        # type:(board) -> (float)
        value = 0
        if self.eval_type == 0 or self.eval_type == '0':
            # # of my pieces - # of ops piece
            for n in range(board.cols): # cols loop
                for i in range(board.rows): # rows loop
                    cellVal = board.get_cell(n, i)
                    if cellVal == self.oppSym: 
                        value = value - 1
                    elif cellVal == self.symbol: 
                        value = value + 1
        elif self.eval_type == 1 or self.eval_type == '1':
            # # of legal moves - # of opps legal moves
            # check for my legal moves
            for n in range(board.cols): # cols loop
                for i in range(board.rows): # rows loop
                    if board.is_legal_move(n, i, self.symbol):
                        value = value + 1
            # check for opps legal moves
            for n in range(board.cols): # cols loop
                for i in range(board.rows): # rows loop
                    if board.is_legal_move(n, i, self.oppSym):
                        value = value - 1
        elif self.eval_type == 2 or self.eval_type == '2':
            for n in range(board.cols): # cols loop
                for i in range(board.rows): # rows loop
                    cellVal = board.get_cell(n, i)
                    if cellVal == self.oppSym: 
                        value = value - 1
                    elif cellVal == self.symbol: 
                        value = value + 1
                        
            if board.get_cell(0, 0) == self.symbol or board.is_legal_move(0, 0, self.symbol): value += 10
            if board.get_cell(0, board.rows) == self.symbol or board.is_legal_move(0, board.rows, self.symbol): value += 10
            if board.get_cell(board.cols, 0) == self.symbol or board.is_legal_move(board.cols, 0, self.symbol): value += 10
            if board.get_cell(board.cols, board.rows) == self.symbol or board.is_legal_move(board.cols, board.rows, self.symbol): value += 10
        
        return value


    def get_successors_info(self, board, player_symbol):
        # Write function that takes the current state and generates all successors obtained by legal moves
        # type:(board, player_symbol) -> (list)
        successors = []
        for n in range(board.cols): # cols loop
            for i in range(board.rows): # rows loop
                if board.is_legal_move(n, i, player_symbol):
                    newBoard = board.cloneOBoard()
                    newBoard.play_move(n, i, player_symbol)
                    successors.append((newBoard, (n, i)))
        
        # print(successors)
        return successors 
    
    def get_successors(self, board, player_symbol):
        # Write function that takes the current state and generates all successors obtained by legal moves
        # type:(board, player_symbol) -> (list)
        successors = []
        for n in range(board.cols): # cols loop
            for i in range(board.rows): # rows loop
                if board.is_legal_move(n, i, player_symbol):
                    newBoard = board.cloneOBoard()
                    newBoard.play_move(n, i, player_symbol)
                    successors.append(newBoard)
    
        # print(successors)
        return successors 


    def get_move(self, board):
        # Write function that returns a move (column, row) here using minimax
        # type:(board) -> (int, int)
        return self.alphabeta(board)