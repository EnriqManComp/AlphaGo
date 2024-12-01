from go.gotypes import Player
import random
from go import agent

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

# MCTS algorithm
""" 
You start by creating a new tree. The root node is the current game
Then you repeatly generate rollouts.

Each round begins by walking down the tree until you find a node where
you can add a child ( any legal move that is not played yet in the tree)

"""

class MCTSAgent(agent.Agent):

    def __init__(self, num_rounds, temperature):
        agent.Agent.__init__(self)
        self.num_rounds = num_rounds
        self.temperature = temperature

    def select_move(self, game_state):
        root = MCTSNode(game_state)

        for i in range(self.num_rounds):
            node = root

            while (not node.can_add_child()) and (not node.is_terminal()):
                node = self.select_child(node)

            if node.can_add_child():
                # Add a new child node 
                node = node.add_random_child()

            # Simulates a random game from this node
            winner = self.simulate_random_game(node.game_state)

            # Propagates the score back up the tree
            while node is not None:
                node.record_win(winner)
                node = node.parent

        # Select a move after completing a MCTS rollouts
        best_move = None
        best_pct = -1.0
        for child in root.children:
            child_pct = child.winning_pct(game_state.next_player)
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
        
        return best_move

            