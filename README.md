# Drive-thru AI Documentation

An AI agent that takes your orders, also for me to practice building a coding project with Cursor

## Project Structure

- `src/drive_thru_ai/`: Main package directory
  - `menu/`: Menu-related components (items, orders, etc.)
  - `ui/`: User interface components

## Installation

```bash
pip install -e .
```

## Usage

```python
from drive_thru_ai.ui import show_menu, show_drive_thru
from drive_thru_ai.menu import Burger, Drink, Meal

# Create menu items
burger = Burger(5.99)
drink = Drink(DrinkType.FOUNTAIN, FountainFlavor.COKE, Size.MEDIUM)
meal = Meal(burger, drink, Fries(Size.MEDIUM))

# Show the UI
show_menu()
show_drive_thru()
``` 