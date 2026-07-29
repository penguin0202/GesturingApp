class Position:
    def __init__(self, x: float = 0, y: float = 0):
        self.x: float = x
        self.y: float = y
    def __add__(self, other: "Position"):
        return Position(x=self.x + other.x, y=self.y + other.y)
    def __sub__(self, other: "Position"):
        return Position(x=self.x - other.x, y=self.y - other.y)