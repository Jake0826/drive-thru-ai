from drive_thru_ai.menu import *
import json
import os
from typing import Dict, List, Optional, Union
from openai import OpenAI
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)


class DriveThruAgent:
    def __init__(self):
        """Initialize the AI agent with OpenAI API key and menu knowledge."""
        # Load the OpenAI API key from the environment variable
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")

        client.api_key = api_key
        self.menu_knowledge = self._load_menu_knowledge()
        self.conversation_history = []
        self.current_order = Order()

    def _load_menu_knowledge(self) -> Dict:
        """Load the menu knowledge base from JSON file."""
        knowledge_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'data',
            'menu_knowledge.json'
        )
        with open(knowledge_path, 'r') as f:
            return json.load(f)

    def _create_system_prompt(self) -> str:
        """Create the system prompt for the AI with menu knowledge."""
        return f"""You are a friendly and efficient drive-thru order taker. 
        You have access to the following menu:
        {json.dumps(self.menu_knowledge, indent=2)}
        
        Your job is to:
        1. Take orders from customers
        2. Ask clarifying questions when needed
        3. Confirm orders before finalizing
        4. Calculate total prices
        5. Be polite and professional
        
        When a customer orders an item, you should:
        1. For burgers: Ask for any customizations (patty, cheese, lettuce, tomato, onion, pickles, sauce)
        2. For drinks: Ask for size and flavor if not specified
        3. For milkshakes: Ask for size and flavor if not specified
        4. For fries: Ask for size if not specified
        5. For nuggets: Ask for piece count if not specified
        
        When creating orders, use the following format:
        - For burgers: Specify customizations (patty, cheese, lettuce, tomato, onion, pickles, sauce)
        - For drinks: Specify type (fountain/milkshake), size, and flavor
        - For nuggets: Specify piece count
        - For fries: Specify size
        
        If a customer's order is missing required details, ask them to specify those details."""

    def process_customer_input(self, customer_input: str) -> str:
        """Process customer input and generate appropriate response."""
        # Add customer input to conversation history
        self.conversation_history.append(
            {"role": "user", "content": customer_input})

        # Create messages for OpenAI API
        messages = [
            {"role": "system", "content": self._create_system_prompt()},
            *self.conversation_history
        ]

        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use the cheapest GPT model
            messages=messages,
            temperature=0.1,
            max_tokens=500
        )

        # Extract and store the response
        ai_response = response.choices[0].message.content
        self.conversation_history.append(
            {"role": "assistant", "content": ai_response})

        # Log the AI response
        logging.info(f"AI Response: {ai_response}")

        # Create an order based on the AI's understanding
        order_details = self._parse_order_details(ai_response)
        if order_details:
            self.add_item_to_order(order_details)

        return ai_response

    def _parse_order_details(self, ai_response: str) -> Optional[Dict]:
        """Parse the AI response to extract order details into a structured format."""
        response_lower = ai_response.lower()
        order_items = []

        # Check for burgers
        if "burger" in response_lower:
            # Extract customizations if present
            customizations = {}
            for ingredient in ["patty", "cheese", "lettuce", "tomato", "onion", "pickles", "sauce"]:
                for amount in ["none", "light", "normal", "double"]:
                    if amount in response_lower and ingredient in response_lower:
                        customizations[ingredient] = amount
                        break

            # If no customizations found, return None to trigger clarifying questions
            if not customizations:
                return None

            order_items.append({
                "type": "item",
                "item_type": "burger",
                "customizations": customizations,
                "quantity": 1
            })

        # Check for nuggets
        if "nuggets" in response_lower:
            count = None
            for count_option in [6, 10, 20]:
                if str(count_option) in response_lower:
                    count = count_option
                    break

            if not count:
                return None

            order_items.append({
                "type": "item",
                "item_type": "nuggets",
                "count": count,
                "quantity": 1
            })

        # Check for drinks
        if "drink" in response_lower or "soda" in response_lower:
            size = None
            flavor = None
            drink_type = "fountain"

            for size_option in ["small", "medium", "large"]:
                if size_option in response_lower:
                    size = size_option
                    break

            for flavor_option in ["coke", "diet_coke"]:
                if flavor_option in response_lower:
                    flavor = flavor_option
                    break

            if not size or not flavor:
                return None

            order_items.append({
                "type": "item",
                "item_type": "drink",
                "drink_type": drink_type,
                "size": size,
                "flavor": flavor,
                "quantity": 1
            })

        # Check for milkshakes
        if "milkshake" in response_lower:
            size = None
            flavor = None

            for size_option in ["small", "medium", "large"]:
                if size_option in response_lower:
                    size = size_option
                    break

            for flavor_option in ["vanilla", "chocolate", "strawberry"]:
                if flavor_option in response_lower:
                    flavor = flavor_option
                    break

            if not size or not flavor:
                return None

            order_items.append({
                "type": "item",
                "item_type": "drink",
                "drink_type": "milkshake",
                "size": size,
                "flavor": flavor,
                "quantity": 1
            })

        # Check for fries
        if "fries" in response_lower:
            size = None
            for size_option in ["small", "medium", "large"]:
                if size_option in response_lower:
                    size = size_option
                    break

            if not size:
                return None

            order_items.append({
                "type": "item",
                "item_type": "fries",
                "size": size,
                "quantity": 1
            })

        # If we found any items, return the structured order
        if order_items:
            return {
                "items": order_items
            }
        return None

    def add_item_to_order(self, order_details: Dict) -> None:
        """Add items to the current order based on the structured order details."""
        if not order_details or "items" not in order_details:
            return

        for item in order_details["items"]:
            custom_item = self._create_custom_order(item)
            if custom_item:
                for _ in range(item["quantity"]):
                    self.current_order.append(custom_item)

    def get_current_order(self) -> List[Meal]:
        """Get the current order."""
        return self.current_order

    def clear_order(self) -> None:
        """Clear the current order."""
        self.current_order = []

    def create_order(self, order_details: Dict) -> Optional[Meal]:
        """Create an order based on the AI's understanding of the customer's request."""
        try:
            if "meal" in order_details:
                return self._create_meal(order_details["meal"])
            else:
                return self._create_custom_order(order_details)
        except Exception as e:
            logging.error(f"Error creating order: {e}")
            return None

    def _create_meal(self, meal_type: str) -> Meal:
        """Create a predefined meal."""
        meal_info = self.menu_knowledge["menu_items"]["meals"][meal_type]

        if meal_type == "burger_meal":
            return Meal(
                main_item=Burger(meal_info["includes"]["main_item"]),
                drink=Drink(
                    DrinkType.FOUNTAIN,
                    FountainFlavor[meal_info["includes"]
                                   ["drink"]["flavor"].upper()],
                    Size[meal_info["includes"]["drink"]["size"].upper()]
                ),
                fries=Fries(Size[meal_info["includes"]
                            ["fries"]["size"].upper()])
            )
        elif meal_type == "nuggets_meal":
            return Meal(
                main_item=Nuggets(meal_info["includes"]["count"]),
                drink=Drink(
                    DrinkType.FOUNTAIN,
                    FountainFlavor[meal_info["includes"]
                                   ["drink"]["flavor"].upper()],
                    Size[meal_info["includes"]["drink"]["size"].upper()]
                ),
                fries=Fries(Size[meal_info["includes"]
                            ["fries"]["size"].upper()])
            )

    def _create_custom_order(self, item_details: Dict) -> Optional[Union[Burger, Drink, Fries, Nuggets]]:
        """Create a custom order based on individual items."""
        try:
            if item_details["item_type"] == "burger":
                burger = Burger(5.99)  # Base price
                for ingredient, amount in item_details["customizations"].items():
                    burger.set_ingredient(
                        ingredient, IngredientAmount[amount.upper()])
                return burger
            elif item_details["item_type"] == "drink":
                if item_details["drink_type"] == "milkshake":
                    return Drink(
                        DrinkType.MILKSHAKE,
                        MilkshakeFlavor[item_details["flavor"].upper()],
                        Size[item_details["size"].upper()]
                    )
                else:  # fountain drink
                    return Drink(
                        DrinkType.FOUNTAIN,
                        FountainFlavor[item_details["flavor"].upper()],
                        Size[item_details["size"].upper()]
                    )
            elif item_details["item_type"] == "fries":
                return Fries(Size[item_details["size"].upper()])
            elif item_details["item_type"] == "nuggets":
                return Nuggets(item_details["count"])
            return None
        except Exception as e:
            logging.error(f"Error creating custom order: {e}")
            return None

    def get_order_total(self, order: List[Meal]) -> float:
        """Calculate the total price of an order."""
        return sum(item.get_price() for item in order)
