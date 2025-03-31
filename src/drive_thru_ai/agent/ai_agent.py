from drive_thru_ai.menu import *
import json
import os
from typing import Dict, List, Optional
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
        self.current_order = []

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
        
        When creating orders, use the following format:
        - For burgers: Specify patty count, cheese, lettuce, onion, and tomato preferences
        - For drinks: Specify type (fountain/milkshake), size, and flavor
        - For nuggets: Specify piece count
        - For fries: Specify size
        - For meals: Use the predefined meal combinations with appropriate modifications"""

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

        # Generate commands to create orders based on the AI's response
        commands = self._generate_commands(ai_response)
        for command in commands:
            self.execute_command(command)

        return ai_response

    def _generate_commands(self, ai_response: str) -> List[str]:
        """Generate commands to create orders based on the AI's response."""
        commands = []
        # Example logic to generate commands based on the AI response
        if "burger" in ai_response.lower():
            commands.append("create_burger")
        elif "nuggets" in ai_response.lower():
            commands.append("create_nuggets")
        return commands

    def execute_command(self, command: str) -> None:
        """Execute the generated command to create an order."""
        if command == "create_burger":
            # Example: Create a burger with default settings
            burger = Burger(5.99)
            self.current_order.append(burger)
        elif command == "create_nuggets":
            # Example: Create a 6-piece nuggets order
            nuggets = Nuggets(6)
            self.current_order.append(nuggets)

    def _parse_order_details(self, ai_response: str) -> Optional[Dict]:
        """Parse the AI response to extract order details."""
        # Implement logic to parse the AI response and return order details
        # This is a placeholder for the actual implementation
        # Example: If the AI response contains "burger", create a burger order

        if "burger" in ai_response.lower():
            return {"meal": "burger_meal"}
        elif "nuggets" in ai_response.lower():
            return {"meal": "nuggets_meal"}
        return None

    def add_item_to_order(self, order_details: Dict) -> None:
        """Add an item to the current order."""
        order = self.create_order(order_details)
        if order:
            self.current_order.append(order)

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

    def _create_custom_order(self, order_details: Dict) -> Meal:
        """Create a custom order based on individual items."""
        # Implementation for custom orders
        pass

    def get_order_total(self, order: List[Meal]) -> float:
        """Calculate the total price of an order."""
        return sum(item.get_price() for item in order)
