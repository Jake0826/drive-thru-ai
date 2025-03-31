from abc import ABC, abstractmethod
from enum import Enum


class Size(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class BaseItem(ABC):
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    @abstractmethod
    def get_description(self) -> str:
        pass

    def get_price(self) -> float:
        return self.price

    def get_name(self) -> str:
        return self.name

    def get_image(self) -> str:
        # Placeholder image URL for all items
        return "https://via.placeholder.com/150?text=Fast+Food+Item"
