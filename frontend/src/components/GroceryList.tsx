import { GroceryItem } from "../api/client";

interface GroceryListProps {
  items: GroceryItem[];
  currency: string;
}

export default function GroceryList({ items, currency }: GroceryListProps) {
  if (!items.length) return null;

  return (
    <section className="card">
      <h2>Grocery list</h2>
      <ul className="grocery-list">
        {items.map((item) => (
          <li key={`${item.item}-${item.quantity}`}>
            <span>{item.item}</span>
            <span className="qty">{item.quantity}</span>
            <span className="cost">
              {item.estimated_cost.toFixed(2)} {currency}
            </span>
          </li>
        ))}
      </ul>
    </section>
  );
}
