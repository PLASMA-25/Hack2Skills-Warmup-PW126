import { BudgetResult } from "../api/client";

interface BudgetBadgeProps {
  budget: BudgetResult;
  retries: number;
}

export default function BudgetBadge({ budget, retries }: BudgetBadgeProps) {
  return (
    <section className={`card budget-card ${budget.within_budget ? "ok" : "over"}`}>
      <h2>Budget</h2>
      <p className="budget-total">
        Estimated: {budget.estimated_total.toFixed(2)} / {budget.limit.toFixed(2)}
      </p>
      <p className={`badge ${budget.within_budget ? "ok" : "over"}`}>
        {budget.within_budget ? "Within budget" : "Over budget"}
      </p>
      <p>{budget.notes}</p>
      {retries > 0 && <p className="meta">Replanned {retries} time(s) to fit budget.</p>}
    </section>
  );
}
