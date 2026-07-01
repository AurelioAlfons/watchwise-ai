import { useState } from "react";
import PreferenceForm from "./components/PreferenceForm";
import ResultsGrid from "./components/ResultsGrid";
import { getRecommendations } from "./api/client";
import type { Recommendation, RecommendRequest } from "./types";

export default function App() {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(data: RecommendRequest) {
    setLoading(true);
    setError("");
    setRecommendations([]);

    try {
      const response = await getRecommendations(data);
      setRecommendations(response.recommendations);
    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-ink font-sans">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 py-10 sm:py-16">
        <div className="text-center mb-10">
          <h1 className="font-display text-3xl sm:text-5xl font-extrabold text-white tracking-tight">
            WatchWise <span className="text-gold">AI</span>
          </h1>
          <p className="text-muted mt-3 text-sm sm:text-base max-w-md mx-auto">
            Tell us your mood — we'll find something worth watching.
          </p>
        </div>

        <PreferenceForm onSubmit={handleSubmit} loading={loading} />

        {loading && (
          <p className="mt-8 text-center text-muted animate-pulse">
            Finding your picks...
          </p>
        )}

        {error && (
          <p className="mt-8 text-center text-red-400">{error}</p>
        )}

        <ResultsGrid recs={recommendations} />
      </div>
    </main>
  );
}