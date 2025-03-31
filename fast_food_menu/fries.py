from .base_item import BaseItem, Size


class Fries(BaseItem):
    PRICES = {
        Size.SMALL: 1.99,
        Size.MEDIUM: 2.49,
        Size.LARGE: 2.99
    }

    def __init__(self, size: Size):
        super().__init__(f"{size.value.capitalize()} Fries", self.PRICES[size])
        self.size = size

    def get_description(self) -> str:
        return f"{self.size.value.capitalize()} Fries"

    def get_image(self) -> str:
        return "https://via.placeholder.com/150?text=French+Fries"
