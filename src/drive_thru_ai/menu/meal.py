from typing import Union
from .base_item import BaseItem, Size
from .burger import Burger
from .nuggets import Nuggets
from .drinks import Drink
from .fries import Fries


class Meal(BaseItem):
    def __init__(self,
                 main_item: Union[Burger, Nuggets],
                 drink: Drink,
                 fries: Fries):
        if drink.size not in [Size.MEDIUM, Size.LARGE]:
            raise ValueError("Meal drinks must be medium or large")
        if fries.size not in [Size.MEDIUM, Size.LARGE]:
            raise ValueError("Meal fries must be medium or large")

        total_price = main_item.get_price() + drink.get_price() + \
            fries.get_price() - 1.0
        super().__init__(f"{main_item.name} Meal", total_price)

        self.main_item = main_item
        self.drink = drink
        self.fries = fries

    def get_description(self) -> str:
        return (f"{self.main_item.get_description()} Meal with "
                f"{self.drink.get_description()} and "
                f"{self.fries.get_description()}")

    def get_image(self) -> str:
        return "https://via.placeholder.com/150?text=Complete+Meal"
