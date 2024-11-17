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