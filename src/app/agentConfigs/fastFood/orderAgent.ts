import { AgentConfig } from "@/app/types";
import { menuItems } from "@/app/data/menu";
import { MenuCategory, MenuItem, DrinkItem } from "@/app/types/menu";
import { OrderCalculator } from "@/app/utils/orderCalculator";

interface OrderItem {
  itemId: string;
  name: string;
  selectedOptionId: string;
  price: number;
}

interface OrderContext {
  items: OrderItem[];
  total: number;
}

// Helper function to find the closest matching item ID
function findClosestItemId(inputId: string): string | null {
  // Direct match
  if (menuItems.some(item => item.id === inputId)) {
    return inputId;
  }

  // Normalize input (remove spaces, convert to lowercase)
  const normalizedInput = inputId.toLowerCase().replace(/\s+/g, '-');

  // Try to find a match
  const match = menuItems.find(item =>
    item.id === normalizedInput ||
    item.id.includes(normalizedInput) ||
    normalizedInput.includes(item.id)
  );

  return match ? match.id : null;
}

// Helper function to find the closest matching option ID
function findClosestOptionId(menuItem: MenuItem | DrinkItem, inputOptionId: string): string | null {
  // Direct match
  if (menuItem.options.some(opt => opt.id === inputOptionId)) {
    return inputOptionId;
  }

  // Normalize input (remove spaces, convert to lowercase)
  const normalizedInput = inputOptionId.toLowerCase().replace(/\s+/g, '-');

  // Try to find a match
  const match = menuItem.options.find(opt =>
    opt.id === normalizedInput ||
    opt.id.includes(normalizedInput) ||
    normalizedInput.includes(opt.id)
  );

  return match ? match.id : null;
}

const orderAgent: AgentConfig = {
  name: "orderAgent",
  publicDescription: "A friendly fast food order taker that helps customers order from our menu.",
  model: "gpt-3.5-turbo",
  instructions: `
# Personality and Tone
## Identity
You are a cheerful and efficient fast food order taker. You're enthusiastic about helping customers get exactly what they want, and you make sure to confirm all order details clearly.

## Task
Your primary goal is to help customers order from our menu. We offer:
- French Fries (Small, Medium, Large)
- Chicken Nuggets (6, 10, or 20 pieces)
- Drinks:
  - Milkshakes (Chocolate, Vanilla, Strawberry) in Small, Medium, Large
  - Sodas (Coke, Diet Coke) in Small, Medium, Large

## Demeanor
Friendly, professional, and attentive. You're quick to understand customer preferences and make sure to get all details right.

## Tone
Warm and welcoming, but efficient. You speak clearly and make sure to confirm all details.

## Level of Enthusiasm
Moderately enthusiastic - you're excited to help but maintain professionalism.

## Level of Formality
Casual but professional - you're friendly but still maintain a service-oriented demeanor.

## Level of Emotion
Supportive and encouraging - you make customers feel comfortable with their choices.

## Filler Words
Minimal use of filler words - you're clear and concise.

## Pacing
Medium pace - clear enough to understand but efficient.

# Steps
1. Greet the customer warmly with "Welcome to McDonald's! How can I help you today?"
2. Ask what they'd like to order
3. For each item:
   - Confirm the item and size
   - For drinks, confirm the specific type (flavor for milkshakes, regular/diet for sodas)
4. Update the order context using the updateOrderContext tool
5. Confirm the total price

# Order Context Format
The order context should be updated in this format:
{
  "items": [
    {
      "itemId": "string",
      "name": "string",
      "selectedOptionId": "string",
      "price": number
    }
  ],
  "total": number
}

# Important Notes
- Always check the current order state before making changes
- If a customer wants to remove an item, update the order context with the remaining items
- If a customer wants to modify an item, update the order context with the modified item
- Keep track of the current order total and ensure it matches the sum of all items
- IMPORTANT: Use the EXACT item IDs from the menu:
  - For Chicken Nuggets: use "chicken-nuggets" (not "chicken-nuggets-6")
  - For French Fries: use "french-fries"
  - For Milkshakes: use "milkshakes"
  - For Sodas: use "sodas"
- For options, use the EXACT option IDs:
  - For sizes: "small", "medium", "large"
  - For nugget quantities: "6-piece", "10-piece", "20-piece"
  - For milkshake flavors: "chocolate", "vanilla", "strawberry"
  - For soda types: "coke", "diet-coke"
- If you encounter an error with an item ID or option ID, try to find the closest match
- Always verify the current order state before making changes
`,
  tools: [
    {
      type: "function",
      name: "getMenuItems",
      description: "Get available menu items by category",
      parameters: {
        type: "object",
        properties: {
          category: {
            type: "string",
            enum: Object.values(MenuCategory)
          }
        },
        required: ["category"]
      }
    },
    {
      type: "function",
      name: "getCurrentOrder",
      description: "Get the current order state",
      parameters: {
        type: "object",
        properties: {},
        required: []
      }
    },
    {
      type: "function",
      name: "updateOrderContext",
      description: "Updates the order context with selected items. Must use exact menu item IDs and prices from the menu.",
      parameters: {
        type: "object",
        properties: {
          orderContext: {
            type: "object",
            properties: {
              items: {
                type: "array",
                items: {
                  type: "object",
                  properties: {
                    itemId: { type: "string" },
                    name: { type: "string" },
                    selectedOptionId: { type: "string" },
                    price: { type: "number" }
                  },
                  required: ["itemId", "name", "selectedOptionId", "price"]
                }
              },
              total: { type: "number" }
            },
            required: ["items", "total"]
          }
        },
        required: ["orderContext"]
      }
    }
  ],
  toolLogic: {
    getMenuItems: async (args) => {
      const { category } = args;
      return menuItems.filter(item => item.category === category && item.available);
    },
    getCurrentOrder: async () => {
      // Get the current order state from the window message
      return new Promise((resolve) => {
        const handleMessage = (event: MessageEvent) => {
          if (event.data.type === 'current_order') {
            window.removeEventListener('message', handleMessage);
            resolve(event.data.order);
          }
        };
        window.addEventListener('message', handleMessage);
        window.postMessage({ type: 'get_current_order' }, '*');
      });
    },
    updateOrderContext: async (args) => {
      const { orderContext } = args as { orderContext: OrderContext };

      // Validate each item against the actual menu
      const validatedItems = orderContext.items.map((orderItem: OrderItem) => {
        // Try to find the correct item ID
        let menuItem = menuItems.find(item => item.id === orderItem.itemId);

        // If not found, try to find the closest match
        if (!menuItem) {
          const closestId = findClosestItemId(orderItem.itemId);
          if (closestId) {
            menuItem = menuItems.find(item => item.id === closestId);
            console.log(`Corrected item ID from "${orderItem.itemId}" to "${closestId}"`);
          }
        }

        if (!menuItem) {
          console.error(`Invalid item ID: ${orderItem.itemId}. Valid IDs are: ${menuItems.map(item => item.id).join(', ')}`);
          throw new Error(`Invalid item ID: ${orderItem.itemId}. Valid IDs are: ${menuItems.map(item => item.id).join(', ')}`);
        }

        // Try to find the correct option ID
        let option = menuItem.options.find(opt => opt.id === orderItem.selectedOptionId);

        // If not found, try to find the closest match
        if (!option) {
          const closestOptionId = findClosestOptionId(menuItem, orderItem.selectedOptionId);
          if (closestOptionId) {
            option = menuItem.options.find(opt => opt.id === closestOptionId);
            console.log(`Corrected option ID from "${orderItem.selectedOptionId}" to "${closestOptionId}" for item "${menuItem.name}"`);
          }
        }

        if (!option) {
          console.error(`Invalid option ID: ${orderItem.selectedOptionId} for item: ${menuItem.name}. Valid options are: ${menuItem.options.map(opt => opt.id).join(', ')}`);
          throw new Error(`Invalid option ID: ${orderItem.selectedOptionId} for item: ${menuItem.name}. Valid options are: ${menuItem.options.map(opt => opt.id).join(', ')}`);
        }

        const correctPrice = menuItem.basePrice + option.priceModifier;
        if (Math.abs(orderItem.price - correctPrice) > 0.01) {
          throw new Error(`Incorrect price for ${menuItem.name} with option ${option.name}. Expected: ${correctPrice.toFixed(2)}, Got: ${orderItem.price.toFixed(2)}`);
        }

        return {
          itemId: menuItem.id,
          name: orderItem.name,
          selectedOptionId: option.id,
          price: correctPrice
        };
      });

      // Calculate correct total
      const correctTotal = validatedItems.reduce((sum: number, item: OrderItem) => sum + item.price, 0);
      if (Math.abs(orderContext.total - correctTotal) > 0.01) {
        throw new Error(`Incorrect total. Expected: ${correctTotal.toFixed(2)}, Got: ${orderContext.total.toFixed(2)}`);
      }

      // Send the validated order context update to the UI
      window.postMessage({
        type: 'order_context',
        context: {
          items: validatedItems,
          total: Number(correctTotal.toFixed(2))
        }
      }, '*');

      return { success: true };
    }
  }
};

export default orderAgent; 