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
1. Greet the customer warmly
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
        const menuItem = menuItems.find(item => item.id === orderItem.itemId);
        if (!menuItem) {
          throw new Error(`Invalid item ID: ${orderItem.itemId}`);
        }

        const option = menuItem.options.find(opt => opt.id === orderItem.selectedOptionId);
        if (!option) {
          throw new Error(`Invalid option ID: ${orderItem.selectedOptionId} for item: ${menuItem.name}`);
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