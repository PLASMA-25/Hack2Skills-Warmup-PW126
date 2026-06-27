import { ParsedIntent } from "../api/client";

interface ParsedIntentChipsProps {
  intent: ParsedIntent;
}

export default function ParsedIntentChips({ intent }: ParsedIntentChipsProps) {
  const chips: string[] = [];
  if (intent.meal_slots?.length) chips.push(intent.meal_slots.join(", "));
  if (intent.cuisine_theme) chips.push(intent.cuisine_theme);
  if (intent.diet) chips.push(intent.diet);
  if (intent.servings) chips.push(`${intent.servings} servings`);
  intent.constraints?.forEach((c) => chips.push(c));
  if (intent.day_context) chips.push(intent.day_context);

  return (
    <section className="card">
      <h2>What we understood</h2>
      <ul className="chips" aria-label="Parsed intent">
        {chips.map((chip) => (
          <li key={chip}>{chip}</li>
        ))}
      </ul>
    </section>
  );
}
