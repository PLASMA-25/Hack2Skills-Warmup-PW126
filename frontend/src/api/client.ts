const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      ...init?.headers,
    },
    ...init,
  });

  if (!response.ok) {
    throw new ApiError(`Request failed: ${response.statusText}`, response.status);
  }

  return response.json() as Promise<T>;
}

export interface HealthResponse {
  status: string;
}

export function fetchHealth(): Promise<HealthResponse> {
  return apiFetch<HealthResponse>("/api/health");
}

export interface ParsedIntent {
  meal_slots: string[] | null;
  servings: number | null;
  cuisine_theme: string | null;
  diet: string | null;
  constraints: string[];
  day_context: string | null;
}

export interface Meal {
  name: string;
  description: string;
  ingredients: string[];
  prep_time_min: number;
}

export interface GroceryItem {
  item: string;
  quantity: string;
  estimated_cost: number;
}

export interface Substitution {
  original: string;
  alternative: string;
  reason: string;
}

export interface BudgetResult {
  estimated_total: number;
  limit: number;
  within_budget: boolean;
  notes: string;
}

export interface ClarificationPrompt {
  question: string;
  missing_fields: string[];
  partial_intent: ParsedIntent;
}

export interface PlanResult {
  parsed_intent: ParsedIntent;
  meals: Record<string, Meal>;
  grocery_list: GroceryItem[];
  substitutions: Substitution[];
  budget: BudgetResult;
  retries: number;
}

export interface PlanResponse {
  status: "needs_clarification" | "complete";
  clarification: ClarificationPrompt | null;
  plan: PlanResult | null;
}

export interface PlanRequest {
  user_intent: string;
  budget: number;
  currency?: string;
  partial_intent?: ParsedIntent | null;
  clarification_answer?: string | null;
}

export function createPlan(request: PlanRequest): Promise<PlanResponse> {
  return apiFetch<PlanResponse>("/api/plan", {
    method: "POST",
    body: JSON.stringify({
      user_intent: request.user_intent,
      budget: request.budget,
      currency: request.currency ?? "USD",
      partial_intent: request.partial_intent ?? null,
      clarification_answer: request.clarification_answer ?? null,
    }),
  });
}
