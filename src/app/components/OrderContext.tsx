import React from 'react';
import { MenuItem, DrinkItem } from '@/app/types/menu';
import { OrderCalculator } from '@/app/utils/orderCalculator';
import { menuItems } from '@/app/data/menu';

interface OrderItem {
  itemId: string;
  name: string;
  selectedOptionId: string;
  price: number;
}

interface OrderContextProps {
  items: OrderItem[];
  total: number;
}

const OrderContext: React.FC<OrderContextProps> = ({ items, total }) => {
  const getMenuItem = (itemId: string): MenuItem | DrinkItem | undefined => {
    return menuItems.find(item => item.id === itemId);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-4">
      <h2 className="text-xl font-semibold mb-4">Current Order</h2>
      {items.length === 0 ? (
        <p className="text-gray-500">No items in order yet</p>
      ) : (
        <>
          <div className="space-y-2">
            {items.map((item, index) => {
              const menuItem = getMenuItem(item.itemId);
              if (!menuItem) return null;

              return (
                <div key={index} className="flex justify-between items-center">
                  <div>
                    <span className="font-medium">{item.name}</span>
                    <span className="text-gray-600 ml-2">
                      ({OrderCalculator.getItemDescription(menuItem, item.selectedOptionId)})
                    </span>
                  </div>
                  <span className="font-medium">{OrderCalculator.formatPrice(item.price)}</span>
                </div>
              );
            })}
          </div>
          <div className="mt-4 pt-4 border-t">
            <div className="flex justify-between items-center">
              <span className="font-semibold">Total</span>
              <span className="font-semibold">{OrderCalculator.formatPrice(total)}</span>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default OrderContext; 