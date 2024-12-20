import numpy as np

from go.encoders.base import Encoder
from go.goboard import Point

class OnePlaneEncoder(Encoder):
    def __init__(self, board_size):
        self.board_width, self.board_height = board_size
        self.num_planes = 1

    def name(self):
        # You can reference this encoder using its name "oneplane"
        return 'oneplane'
    
    def encode(self, game_state):
        """
        Fill a matrix with 1 if the point contains one of the current player's stones,
        and -1 if the point contains the opponent's stones. Otherwise, 0 if the point is empty.

        """
        board_matrix = np.zeros(self.shape())
        next_player = game_state.next_player
        for r in range(self.board_height):
            for c in range(self.board_width):
                p = Point(row=r+1, col=c+1)
                go_string = game_state.board.get_go_string(p)
                if go_string is None:
                    continue
                if go_string.color == next_player:
                    board_matrix[0,r,c] = 1
                else:
                    board_matrix[0,r,c] = -1
        return board_matrix
    
    def encode_point(self, point):
        """
        Turns a board point into an integer index
        """
        return self.board_width * (point.row - 1) + (point.col - 1)
    
    def decode_point(self, index):
        """
        Turns an integer index into a board point
        """
        row = index // self.board_width
        col = index % self.board_width
        return Point(row=row+1, col=col+1)
    
    def num_points(self):
        return self.board_width * self.board_height
    
    def shape(self):
        return self.num_planes, self.board_height, self.board_width
