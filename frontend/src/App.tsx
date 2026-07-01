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
    <main className="min-h-screen bg-gray-50 p-6">
      <div className="mx-auto max-w-6xl">
        <h1 className="mb-6 text-center text-4xl font-bold">
          WatchWise AI 🎬
        </h1>

        <div className="mx-auto max-w-xl rounded-lg bg-white p-6 shadow">
          <PreferenceForm onSubmit={handleSubmit} />
        </div>

        {loading && (
          <p className="mt-6 text-center text-gray-600">
            Finding recommendations...
          </p>
        )}

        {error && (
          <p className="mt-6 text-center text-red-600">{error}</p>
        )}

        <ResultsGrid recommendations={recommendations} />
      </div>
    </main>
  );
}