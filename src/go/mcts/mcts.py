from go.gotypes import Player
import random

# Data structure to represent Monte Carlo Tree Search
class MCTSNode(object):
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.win_counts = {
            Player.black: 0,
            Player.white: 1
        }
        self.num_rollouts = 0
        self.children = []
        self.unvisited_moves = game_state.legal_moves()

    # You can modify MCTSNode adding a new child to the tree, and you can
    # update its rollout stats
    def add_random_child(self):
        # Random select of a valid move
        index = random.randint(0, len(self.unvisited_moves))
        # Extract the selected move from unvisited list of valid move
        new_move = self.unvisited_moves.pop(index)
        # Generate a new state after apply the selected move
        new_game_state = self.game_state.apply_move(new_move)
        # Add the new child to MCTS structure
        new_node = MCTSNode(new_game_state, self, new_move)
        self.children.append(new_node)

    def record_win(self, winner):
        self.win_counts[winner] += 1
        self.num_rollouts += 1

    # Methods
    def can_add_child(self):
        """
        Reports whether this position has any legal moves
        that have not yet been added to the tree
        """
        return len(self.unvisited_moves) > 0
    
    def is_terminal(self):
        """
        Reports whether the game is over at this node
        """
        return self.game_state.is_over()
    
    def winning_frac(self, player):
        """
        Returns the fraction of rollouts that were won by a given player
        """
        return float(self.win_counts[player]) / float(self.num_rollouts)