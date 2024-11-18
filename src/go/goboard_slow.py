import copy
from go.gotypes import Player

# Move represents the possible options that a player can choose (play a stone, pass or resign)
# You call Move.play, Move.pass_turn, Move.resign to contruct an instance of a move
class Move():
    def __init__(self, point=None, is_pass:bool=False, is_resign:bool=False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point):
        """
        This place a stone in the board
        """
        return Move(point=point)

    @classmethod
    def pass_turn(cls):
        """
        This pass
        """
        return Move(is_pass=True)

    @classmethod
    def resign(cls):
        """
        This resign the current game
        """
        return Move(is_resign=True) 

# Track number of liberties of each group of stones
class GoString():
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    def remove_liberty(self, point):
        self.liberties.remove(point)

    def add_liberty(self, point):
        self.liberties.add(point)

    # Case of place one stone that joint two different groups
    def merged_with(self, go_string):
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | go_string.liberties) - combined_stones
        )
    
    @property
    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self, other):
        return isinstance(other, GoString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties

# Go Board
class Board():
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}

    def place_stone(self, player, point):
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None

        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []
        
        for neighbor in point.neighbors():
            if not self.is_on_grid(neighbor):
                continue
            neighbor_string = self._grid.get(neighbor)
            if neighbor_string is None:
                liberties.append(neighbor)
            elif neighbor_string.color == player:
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            else:
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)
            
        new_string = GoString(player, [point], liberties)
