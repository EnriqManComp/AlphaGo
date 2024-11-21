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

        # Group of adjacent stones with the same color
        adjacent_same_color = []
        # Group of adjacent stones with the opposite color
        adjacent_opposite_color = []
        # Liberties around the group
        liberties = []
        # Examine the neighbor of the point "point"
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

        for same_color_string in adjacent_same_color:
            # Merge any adjacent strings of the same color
            new_string = new_string.merged_with(same_color_string)
        for new_string_point in new_string.stones:
            # Update grid
            self._grid[new_string_point] = new_string
        for other_color_string in adjacent_opposite_color:
            # Reduce liberties of any adjacent strings of opposite color
            other_color_string.remove_liberty(point)
        for other_color_string in adjacent_opposite_color:
            # if any opposite color string have zero liberties, remove them
            ####
            # Note that when a stone, or a group of stones, is captured the opposite
            # color gain additional liberties
            ####
            if other_color_string.num_liberties == 0:
                self._remove_string(other_color_string)
        
             



    # Utility methods
    
    def is_on_grid(self, point):
        return 1 <= point.row <= self.num_rows and \
            1 <= point.col <= self.num_cols

    def get(self, point):
        """
        Returns if a stone is placed at point "point"
        """
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color

    def get_on_string(self, point):
        """
        Returns the entire string of stones at a point
        
        """
        string = self._grid.get(point)
        if string is None:
            return None
        return string
    
    def _remove_string(self, string):

        for point in string.stones:
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    neighbor_string.add_liberty(point)
            self._grid[point] = None

# Rules for placing and capturing stones on a Board
class GameState():
    def __init__(self, board, next_player, previous, move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        self.last_move = move

    def apply_move(self, move):
        """
        Returns the new GameState after applying a move
        """

        if move.is_play:
            # Choose move
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        else:
            # Choose pass
            next_board = self.board

        return GameState(next_board, self.next_player.other, self, move)
    
    @classmethod
    def new_game(cls, board_size):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return GameState(board, Player.black, None, None)
    
    def is_over(self):
        """
        Decide if the game is over

        """
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass
    
    