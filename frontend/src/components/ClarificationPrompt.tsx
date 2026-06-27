import { FormEvent, useState } from "react";

interface ClarificationPromptProps {
  question: string;
  onSubmit: (answer: string) => void;
  loading: boolean;
  onBack: () => void;
}

export default function ClarificationPrompt({
  question,
  onSubmit,
  loading,
  onBack,
}: ClarificationPromptProps) {
  const [answer, setAnswer] = useState("");

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!answer.trim()) return;
    onSubmit(answer.trim());
  }

  return (
    <form className="card clarify-card" onSubmit={handleSubmit}>
      <p className="clarify-label">We need a bit more info</p>
      <p className="clarify-question" id="clarify-question">
        {question}
      </p>
      <label htmlFor="clarify-answer" className="visually-hidden">
        Your answer
      </label>
      <input
        id="clarify-answer"
        type="text"
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
        aria-labelledby="clarify-question"
        required
      />
      <div className="button-row">
        <button type="button" className="secondary" onClick={onBack} disabled={loading}>
          Start over
        </button>
        <button type="submit" aria-busy={loading} disabled={loading}>
          {loading ? "Updating…" : "Continue"}
        </button>
      </div>
    </form>
  );
}
