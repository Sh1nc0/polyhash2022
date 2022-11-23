class Gift:

    def __init__(self, name, score, weight, x, y):
        self.name: str = name
        self.score: int = score
        self.weight: int = weight
        self.x: int = x
        self.y: int = y

    def __str__(self):
        return f"Gift: {self.name} {self.score} {self.weight} {self.x} {self.y}"
