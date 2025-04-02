export enum MenuCategory {
  MAIN = 'MAIN',
  SIDES = 'SIDES',
  DRINKS = 'DRINKS'
}

export enum DrinkType {
  MILKSHAKE = 'MILKSHAKE',
  SODA = 'SODA'
}

export enum MilkshakeFlavor {
  CHOCOLATE = 'CHOCOLATE',
  VANILLA = 'VANILLA',
  STRAWBERRY = 'STRAWBERRY'
}

export enum SodaType {
  COKE = 'COKE',
  DIET_COKE = 'DIET_COKE'
}

export interface MenuItem {
  id: string;
  name: string;
  description: string;
  category: MenuCategory;
  basePrice: number;
  options: MenuItemOption[];
  available: boolean;
  flavors?: Array<{
    id: string;
    name: string;
    available: boolean;
  }>;
}

export interface MenuItemOption {
  id: string;
  name: string;
  priceModifier: number;
  available: boolean;
}

export interface DrinkItem extends MenuItem {
  drinkType: DrinkType;
  milkshakeFlavor?: MilkshakeFlavor;
  sodaType?: SodaType;
} 