import { useState } from "react";
import { createPlan, ParsedIntent, PlanRequest, PlanResponse } from "./api/client";
import BudgetBadge from "./components/BudgetBadge";
import ClarificationPrompt from "./components/ClarificationPrompt";
import GroceryList from "./components/GroceryList";
import IntentForm from "./components/IntentForm";
import MealCards from "./components/MealCards";
import ParsedIntentChips from "./components/ParsedIntentChips";
import Substitutions from "./components/Substitutions";

type Phase = "form" | "clarify" | "results";

export default function App() {
  const [phase, setPhase] = useState<Phase>("form");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [response, setResponse] = useState<PlanResponse | null>(null);
  const [lastRequest, setLastRequest] = useState<PlanRequest | null>(null);
  const [partialIntent, setPartialIntent] = useState<ParsedIntent | null>(null);
  const [clarificationQuestion, setClarificationQuestion] = useState("");

  async function submitPlan(request: PlanRequest) {
    setLoading(true);
    setError("");
    try {
      const data = await createPlan(request);
      setResponse(data);
      setLastRequest(request);
      if (data.status === "needs_clarification" && data.clarification) {
        setPartialIntent(data.clarification.partial_intent);
        setClarificationQuestion(data.clarification.question);
        setPhase("clarify");
      } else {
        setPhase("results");
      }
    } catch {
      setError("Something went wrong. Check your API key and try again.");
    } finally {
      setLoading(false);
    }
  }

  function handleGenerate(userIntent: string, budget: number) {
    submitPlan({ user_intent: userIntent, budget, currency: "USD" });
  }

  function handleClarifyAnswer(answer: string) {
    if (!lastRequest || !partialIntent) return;
    submitPlan({
      user_intent: lastRequest.user_intent,
      budget: lastRequest.budget,
      currency: lastRequest.currency,
      partial_intent: partialIntent,
      clarification_answer: answer,
    });
  }

  function handleReset() {
    setPhase("form");
    setResponse(null);
    setPartialIntent(null);
    setClarificationQuestion("");
    setLastRequest(null);
    setError("");
  }

  return (
    <div className="page">
      <header className="hero">
        <h1>Your Cooking To-Do List</h1>
        <p>AI meal planning for your day — breakfast, lunch, dinner, groceries, and budget.</p>
      </header>

      {phase === "form" && (
        <IntentForm onSubmit={handleGenerate} loading={loading} />
      )}

      {phase === "clarify" && (
        <ClarificationPrompt
          question={clarificationQuestion}
          onSubmit={handleClarifyAnswer}
          loading={loading}
          onBack={handleReset}
        />
      )}

      {error && (
        <p className="error" role="alert">
          {error}
        </p>
      )}

      {phase === "results" && response?.plan && (
        <section className="results" aria-live="polite">
          <ParsedIntentChips intent={response.plan.parsed_intent} />
          <MealCards meals={response.plan.meals} />
          <GroceryList items={response.plan.grocery_list} currency={lastRequest?.currency ?? "USD"} />
          <Substitutions items={response.plan.substitutions} />
          <BudgetBadge budget={response.plan.budget} retries={response.plan.retries} />
          <button type="button" className="secondary" onClick={handleReset}>
            Plan another day
          </button>
        </section>
      )}
    </div>
  );
}
