import React, { useState, useEffect } from 'react';
import { MenuItem, DrinkItem, MenuCategory } from '@/app/types/menu';
import { menuItems } from '@/app/data/menu';
import { OrderCalculator } from '@/app/utils/orderCalculator';
import { OrderItem, OrderState, Order } from '@/app/types/order';

interface MenuProps {
  order: Order;
  onOrderUpdate: (order: Order) => void;
}

const Menu: React.FC<MenuProps> = ({ order, onOrderUpdate }) => {
  const [isOpen, setIsOpen] = useState(true);
  const [selectedFlavors, setSelectedFlavors] = useState<Record<string, string | null>>({});

  // Update total whenever order items change
  useEffect(() => {
    const newTotal = Number(order.items.reduce((sum, item) => sum + item.price, 0).toFixed(2));
    if (Math.abs(newTotal - order.total) > 0.01) {
      const newOrder = new Order();
      order.items.forEach(item => {
        const menuItem = menuItems.find(mi => mi.id === item.itemId);
        if (menuItem) {
          newOrder.addItem(menuItem, item.selectedOptionId);
        }
      });
      onOrderUpdate(newOrder);
    }
  }, [order, onOrderUpdate]);

  const getMenuItem = (itemId: string): MenuItem | DrinkItem | undefined => {
    return menuItems.find(item => item.id === itemId);
  };

  const handleAddItem = (item: MenuItem | DrinkItem, optionId: string, flavorId?: string) => {
    const newOrder = new Order();
    order.items.forEach(existingItem => {
      const menuItem = menuItems.find(mi => mi.id === existingItem.itemId);
      if (menuItem) {
        newOrder.addItem(menuItem, existingItem.selectedOptionId);
      }
    });

    const option = item.options.find(opt => opt.id === optionId);
    if (!option) return;

    const price = item.basePrice + option.priceModifier;
    const name = flavorId ? `${item.name} - ${item.flavors?.find(f => f.id === flavorId)?.name}` : item.name;

    newOrder.addItem(item, optionId);
    onOrderUpdate(newOrder);
    setSelectedFlavors(prev => ({ ...prev, [item.id]: null }));
  };

  const handleFlavorSelect = (itemId: string, flavorId: string) => {
    setSelectedFlavors(prev => ({ ...prev, [itemId]: flavorId }));
  };

  const handleRemoveItem = (itemId: string, index: number) => {
    const newOrder = new Order();
    order.items.forEach((existingItem, i) => {
      if (i !== index) {
        const menuItem = menuItems.find(mi => mi.id === existingItem.itemId);
        if (menuItem) {
          newOrder.addItem(menuItem, existingItem.selectedOptionId);
        }
      }
    });
    onOrderUpdate(newOrder);
  };

  return (
    <div className={`bg-white shadow-lg transition-all duration-300 ${isOpen ? 'w-96' : 'w-12'}`}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-full bg-white p-2 rounded-l-lg shadow-md"
      >
        {isOpen ? '→' : '←'}
      </button>

      <div className="h-full flex flex-col">
        {/* Menu Section */}
        <div className="flex-1 overflow-y-auto p-4">
          <h2 className="text-xl font-semibold mb-4">Menu</h2>
          {Object.values(MenuCategory).map(category => (
            <div key={category} className="mb-6">
              <h3 className="text-lg font-medium mb-2">{category}</h3>
              <div className="space-y-2">
                {menuItems
                  .filter(item => item.category === category && item.available)
                  .map(item => (
                    <div key={item.id} className="border rounded-lg p-3">
                      <h4 className="font-medium">{item.name}</h4>
                      <p className="text-sm text-gray-600 mb-2">{item.description}</p>
                      {item.flavors && (
                        <div className="mb-2 flex flex-wrap gap-2">
                          {item.flavors.map(flavor => (
                            <button
                              key={flavor.id}
                              onClick={() => handleFlavorSelect(item.id, flavor.id)}
                              className={`px-2 py-1 text-sm rounded ${selectedFlavors[item.id] === flavor.id
                                ? 'bg-blue-100 text-blue-800'
                                : 'bg-gray-100 hover:bg-gray-200'
                                }`}
                            >
                              {flavor.name}
                            </button>
                          ))}
                        </div>
                      )}
                      <div className="space-y-1">
                        {item.options.map(option => (
                          <div
                            key={option.id}
                            className="w-full text-left px-2 py-1 text-sm text-gray-500"
                          >
                            {option.name} - {OrderCalculator.formatPrice(item.basePrice + option.priceModifier)}
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          ))}
        </div>

        {/* Order Section */}
        <div className="border-t p-4">
          <h2 className="text-xl font-semibold mb-4">Current Order</h2>
          {order.items.length === 0 ? (
            <p className="text-gray-500">No items in order</p>
          ) : (
            <>
              <div className="space-y-2">
                {order.items.map((item, index) => {
                  const menuItem = getMenuItem(item.itemId);
                  if (!menuItem) return null;

                  return (
                    <div key={`${item.itemId}-${index}`} className="flex justify-between items-center">
                      <div>
                        <span className="font-medium">{item.name}</span>
                        <span className="text-gray-600 ml-2">
                          ({OrderCalculator.getItemDescription(menuItem, item.selectedOptionId)})
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="font-medium">{OrderCalculator.formatPrice(item.price)}</span>
                        {/* <button
                          onClick={() => handleRemoveItem(item.itemId, index)}
                          className="text-red-500 hover:text-red-700"
                        >
                          ×
                        </button> */}
                      </div>
                    </div>
                  );
                })}
              </div>
              <div className="mt-4 pt-4 border-t">
                <div className="flex justify-between items-center">
                  <span className="font-semibold">Total</span>
                  <span className="font-semibold">{OrderCalculator.formatPrice(order.total)}</span>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Menu; 