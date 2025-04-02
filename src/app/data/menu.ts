import { MenuItem, DrinkItem, MenuCategory, DrinkType, MilkshakeFlavor, SodaType } from '@/app/types/menu';

export const menuItems: (MenuItem | DrinkItem)[] = [
  {
    id: 'chicken-nuggets',
    name: 'Chicken Nuggets',
    description: 'Crispy, golden chicken nuggets served with your choice of dipping sauce.',
    category: MenuCategory.MAIN,
    basePrice: 3.99,
    available: true,
    options: [
      { id: '6-piece', name: '6 Piece', priceModifier: 0, available: true },
      { id: '10-piece', name: '10 Piece', priceModifier: 2.00, available: true },
      { id: '20-piece', name: '20 Piece', priceModifier: 4.00, available: true }
    ]
  },
  {
    id: 'french-fries',
    name: 'French Fries',
    description: 'Crispy, golden fries seasoned with our special blend of spices.',
    category: MenuCategory.SIDES,
    basePrice: 2.99,
    available: true,
    options: [
      { id: 'small', name: 'Small', priceModifier: 0, available: true },
      { id: 'medium', name: 'Medium', priceModifier: 1.00, available: true },
      { id: 'large', name: 'Large', priceModifier: 2.00, available: true }
    ]
  },
  {
    id: 'milkshakes',
    name: 'Milkshakes',
    description: 'Creamy, thick milkshakes made with real ice cream.',
    category: MenuCategory.DRINKS,
    basePrice: 4.99,
    available: true,
    drinkType: DrinkType.MILKSHAKE,
    options: [
      { id: 'small', name: 'Small', priceModifier: 0, available: true },
      { id: 'medium', name: 'Medium', priceModifier: 1.00, available: true },
      { id: 'large', name: 'Large', priceModifier: 2.00, available: true }
    ],
    flavors: [
      { id: 'chocolate', name: 'Chocolate', available: true },
      { id: 'vanilla', name: 'Vanilla', available: true },
      { id: 'strawberry', name: 'Strawberry', available: true }
    ]
  },
  {
    id: 'sodas',
    name: 'Sodas',
    description: 'Ice-cold Coca-Cola beverages.',
    category: MenuCategory.DRINKS,
    basePrice: 1.99,
    available: true,
    drinkType: DrinkType.SODA,
    options: [
      { id: 'small', name: 'Small', priceModifier: 0, available: true },
      { id: 'medium', name: 'Medium', priceModifier: 0.50, available: true },
      { id: 'large', name: 'Large', priceModifier: 1.00, available: true }
    ],
    flavors: [
      { id: 'coke', name: 'Coca-Cola', available: true },
      { id: 'diet-coke', name: 'Diet Coke', available: true }
    ]
  }
]; 