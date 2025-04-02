import { MenuItem, DrinkItem } from '@/app/types/menu';
import { menuItems } from '@/app/data/menu';

export class OrderCalculator {
  static calculateItemPrice(item: MenuItem | DrinkItem, selectedOptionId: string): number {
    const option = item.options.find(opt => opt.id === selectedOptionId);
    if (!option) return item.basePrice;
    return item.basePrice + option.priceModifier;
  }

  static calculateOrderTotal(items: Array<{ item: MenuItem | DrinkItem; selectedOptionId: string; }>): number {
    return items.reduce((total, { item, selectedOptionId }) => {
      return total + this.calculateItemPrice(item, selectedOptionId);
    }, 0);
  }

  static formatPrice(price: number | undefined | null): string {
    if (price === undefined || price === null) return '$0.00';
    return `$${Number(price).toFixed(2)}`;
  }

  static getItemDescription(item: MenuItem | DrinkItem, selectedOptionId: string): string {
    const option = item.options.find(opt => opt.id === selectedOptionId);
    if (!option) return '';

    if ('drinkType' in item) {
      if (item.drinkType === 'MILKSHAKE' && item.milkshakeFlavor) {
        return `${item.milkshakeFlavor} ${option.name}`;
      } else if (item.drinkType === 'SODA' && item.sodaType) {
        return `${item.sodaType} ${option.name}`;
      }
    }

    return option.name;
  }
} 