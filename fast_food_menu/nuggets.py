from .base_item import BaseItem


class Nuggets(BaseItem):
    PIECE_COUNTS = [6, 10, 20]
    PRICES = {
        6: 3.99,
        10: 5.99,
        20: 9.99
    }

    def __init__(self, piece_count: int):
        if piece_count not in self.PIECE_COUNTS:
            raise ValueError(
                f"Invalid piece count. Must be one of {self.PIECE_COUNTS}")
        super().__init__(
            f"{piece_count} Piece Chicken Nuggets", self.PRICES[piece_count])
        self.piece_count = piece_count

    def get_description(self) -> str:
        return f"{self.piece_count} Piece Chicken Nuggets"

    def get_image(self) -> str:
        return "https://via.placeholder.com/150?text=Chicken+Nuggets"
