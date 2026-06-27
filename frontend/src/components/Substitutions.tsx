import { Substitution } from "../api/client";

interface SubstitutionsProps {
  items: Substitution[];
}

export default function Substitutions({ items }: SubstitutionsProps) {
  if (!items.length) return null;

  return (
    <section className="card">
      <h2>Substitutions</h2>
      <ul className="subs-list">
        {items.map((sub) => (
          <li key={`${sub.original}-${sub.alternative}`}>
            <strong>{sub.original}</strong> → {sub.alternative}
            <span className="reason">{sub.reason}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
