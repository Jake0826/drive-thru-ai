import { MenuItem, DrinkItem } from './menu';
import { OrderCalculator } from '../utils/orderCalculator';

export interface OrderItem {
  itemId: string;
  name: string;
  selectedOptionId: string;
  price: number;
}

export interface OrderState {
  items: OrderItem[];
  total: number;
}

export class Order {
  public items: OrderItem[] = [];
  public total: number = 0;

  constructor() {
    this.items = [];
  }

  public addItem(item: MenuItem | DrinkItem, selectedOptionId: string): void {
    const price = OrderCalculator.calculateItemPrice(item, selectedOptionId);
    this.items.push({
      itemId: item.id,
      name: item.name,
      selectedOptionId,
      price
    });
    this.updateTotal();
  }

  public removeItem(index: number): void {
    this.items.splice(index, 1);
    this.updateTotal();
  }

  public getItems(): OrderItem[] {
    return this.items;
  }

  public getTotal(): number {
    return this.total;
  }

  public clear(): void {
    this.items = [];
    this.total = 0;
  }

  private updateTotal(): void {
    this.total = Number(this.items.reduce((sum, item) => sum + item.price, 0).toFixed(2));
  }

  public toJSON(): OrderState {
    return {
      items: this.items,
      total: this.total
    };
  }
} 