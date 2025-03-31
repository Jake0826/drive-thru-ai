from enum import Enum
from .base_item import BaseItem


class IngredientAmount(Enum):
    NONE = "none"
    LIGHT = "light"
    NORMAL = "normal"
    DOUBLE = "double"


class Burger(BaseItem):
    def __init__(self, base_price: float):
        self.ingredients = {
            "patty": IngredientAmount.NORMAL,
            "cheese": IngredientAmount.NORMAL,
            "lettuce": IngredientAmount.NORMAL,
            "tomato": IngredientAmount.NORMAL,
            "onion": IngredientAmount.NORMAL,
            "pickles": IngredientAmount.NORMAL,
            "sauce": IngredientAmount.NORMAL
        }
        # Generate initial name based on default ingredients
        self.name = self._generate_name()
        super().__init__(self.name, base_price)

    def set_ingredient(self, ingredient: str, amount: IngredientAmount):
        if ingredient in self.ingredients:
            self.ingredients[ingredient] = amount
            # Adjust price based on ingredient amount
            if amount == IngredientAmount.DOUBLE:
                self.price += 1.0
            # elif amount == IngredientAmount.NONE:
                # self.price -= 0.5
            # Update name after ingredient change
            self.name = self._generate_name()

    def _generate_name(self) -> str:
        # Start with patty description
        patty_desc = self.ingredients["patty"].value
        name_parts = [f"{patty_desc} patty"]

        # Add other ingredients that are not normal
        for ingredient, amount in self.ingredients.items():
            if ingredient != "patty" and amount != IngredientAmount.NORMAL:
                if amount == IngredientAmount.NONE:
                    name_parts.append(f"no {ingredient}")
                else:
                    name_parts.append(f"{amount.value} {ingredient}")

        return " ".join(name_parts).title()

    def get_description(self) -> str:
        desc = f"Burger with: "
        ingredients_desc = []
        for ingredient, amount in self.ingredients.items():
            if amount != IngredientAmount.NONE:
                ingredients_desc.append(f"{amount.value} {ingredient}")
        return desc + ", ".join(ingredients_desc)

    def get_image(self) -> str:
        return "https://via.placeholder.com/150?text=Burger"

