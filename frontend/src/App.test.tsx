import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import App from "./App";

describe("App", () => {
  it("renders cooking app heading and form", () => {
    render(<App />);
    expect(screen.getByRole("heading", { name: /cooking to-do list/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/what do you want to cook/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /generate my cooking plan/i })).toBeInTheDocument();
  });
});
