import { FormEvent, useState } from "react";

interface IntentFormProps {
  onSubmit: (userIntent: string, budget: number) => void;
  loading: boolean;
}

export default function IntentForm({ onSubmit, loading }: IntentFormProps) {
  const [userIntent, setUserIntent] = useState("");
  const [budget, setBudget] = useState("30");

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const parsedBudget = Number(budget);
    if (!userIntent.trim() || !parsedBudget || parsedBudget <= 0) return;
    onSubmit(userIntent.trim(), parsedBudget);
  }

  return (
    <form className="card form-card" onSubmit={handleSubmit}>
      <label htmlFor="user-intent">What do you want to cook today?</label>
      <textarea
        id="user-intent"
        rows={4}
        value={userIntent}
        onChange={(e) => setUserIntent(e.target.value)}
        placeholder="e.g. Veg North Indian dinner for a busy workday"
        required
      />

      <label htmlFor="budget">Grocery budget (USD)</label>
      <input
        id="budget"
        type="number"
        min="1"
        step="1"
        value={budget}
        onChange={(e) => setBudget(e.target.value)}
        required
      />

      <button type="submit" aria-busy={loading} disabled={loading}>
        {loading ? "Planning your meals…" : "Generate my cooking plan"}
      </button>
    </form>
  );
}
