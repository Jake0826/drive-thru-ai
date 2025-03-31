from typing import List, Dict
from collections import Counter
from .base_item import BaseItem


class Order:
    def __init__(self):
        self.items: List[BaseItem] = []

    def add_item(self, item: BaseItem) -> None:
        self.items.append(item)

    def remove_item(self, index: int) -> None:
        if 0 <= index < len(self.items):
            self.items.pop(index)

    def get_total_price(self) -> float:
        return sum(item.get_price() for item in self.items)

    def get_item_counts(self) -> Dict[str, int]:
        return Counter(item.get_name() for item in self.items)

    def get_order_summary(self) -> str:
        summary = "Order Summary:\n"
        summary += "-" * 40 + "\n"

        # Group items by name and count
        item_counts = self.get_item_counts()
        for item_name, count in item_counts.items():
            # Find the first item of this type to get its price
            first_item = next(
                item for item in self.items if item.get_name() == item_name)
            summary += f"{count}x {item_name}: ${first_item.get_price():.2f} each\n"

        summary += "-" * 40 + "\n"
        summary += f"Total: ${self.get_total_price():.2f}"
        return summary

    def get_items_by_type(self) -> Dict[str, List[BaseItem]]:
        items_by_type = {}
        for item in self.items:
            item_type = item.__class__.__name__
            if item_type not in items_by_type:
                items_by_type[item_type] = []
            items_by_type[item_type].append(item)
        return items_by_type

    def clear_order(self) -> None:
        self.items = []

    def get_number_of_items(self) -> int:
        return len(self.items)
