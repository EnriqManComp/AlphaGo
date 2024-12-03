import importlib

"""
One color is represented as 1, the other as -1,
and empty points as 0. So instead of using 1 for black,
and -1 for white, you will use 1 for whoever has the next turn,
and -1 for the opponent.



"""

class Encoder:
    def name(self):
        """
        Lets you support logging or saving the name of the encoder your model is using
        """
        raise NotImplementedError()
    
    def encode(self, game_state):
        """
        Encodes Go Board into numeric data
        """
        raise NotImplementedError()
    
    def encode_point(self, point):
        """
        Encodes a Go Board point into an integer index
        """
        raise NotImplementedError()
    
    def decode_point(self, index):
        raise NotImplementedError()
    
    def num_points(self):
        """
        Number of points on the board (width times height)
        """
        raise NotImplementedError()
    
    def shape(self):
        """
        Shape of the encoded board structure
        """
        raise NotImplementedError()
    
def get_encoder_by_name(name, board_size):
    """
    Creates encoder instances by referencing their name
    """
    if isinstance(board_size, int):
        # If board_size is one integer, you create a square board from it
        board_size = (board_size, board_size)
    module = importlib.import_module("go.encoders." + name)
    # Each encoder implementation will have to provide a "create"
    # function that provides an instance.
    constructor = getattr(module, "create")
    return constructor(board_size)

