import { Meal } from "../api/client";

interface MealCardsProps {
  meals: Record<string, Meal>;
}

const SLOT_LABELS: Record<string, string> = {
  breakfast: "Breakfast",
  lunch: "Lunch",
  dinner: "Dinner",
};

export default function MealCards({ meals }: MealCardsProps) {
  const slots = Object.keys(meals);
  if (!slots.length) return null;

  return (
    <section className="card">
      <h2>Meal plan</h2>
      <div className="meal-grid">
        {slots.map((slot) => {
          const meal = meals[slot];
          return (
            <article key={slot} className="meal-card">
              <h3>{SLOT_LABELS[slot] ?? slot}</h3>
              <p className="meal-name">{meal.name}</p>
              <p>{meal.description}</p>
              <p className="meta">{meal.prep_time_min} min prep</p>
              <ul>
                {meal.ingredients.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </article>
          );
        })}
      </div>
    </section>
  );
}
