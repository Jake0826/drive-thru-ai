from enum import Enum
from .base_item import BaseItem, Size


class DrinkType(Enum):
    FOUNTAIN = "fountain"
    MILKSHAKE = "milkshake"


class FountainFlavor(Enum):
    COKE = "Coke"
    DIET_COKE = "Diet Coke"


class MilkshakeFlavor(Enum):
    STRAWBERRY = "Strawberry"
    VANILLA = "Vanilla"
    CHOCOLATE = "Chocolate"


class Drink(BaseItem):
    FOUNTAIN_PRICES = {
        Size.SMALL: 1.99,
        Size.MEDIUM: 2.49,
        Size.LARGE: 2.99
    }

    MILKSHAKE_PRICES = {
        Size.SMALL: 3.99,
        Size.MEDIUM: 4.49,
        Size.LARGE: 4.99
    }

    def __init__(self, drink_type: DrinkType, flavor: FountainFlavor | MilkshakeFlavor, size: Size):
        self.drink_type = drink_type
        self.flavor = flavor
        self.size = size

        if drink_type == DrinkType.FOUNTAIN:
            price = self.FOUNTAIN_PRICES[size]
            name = f"{size.value.capitalize()} {flavor.value}"
        else:  # Milkshake
            price = self.MILKSHAKE_PRICES[size]
            name = f"{size.value.capitalize()} {flavor.value} Milkshake"

        super().__init__(name, price)

    def get_description(self) -> str:
        return self.name

    def get_image(self) -> str:
        if self.drink_type == DrinkType.FOUNTAIN:
            return "https://via.placeholder.com/150?text=Fountain+Drink"
        else:
            return "https://via.placeholder.com/150?text=Milkshake"
