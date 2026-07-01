import type { Recommendation } from "../types";
import RecommendationCard from "./RecommendationCard";

interface Props {
  recommendations: Recommendation[];
}

export default function ResultsGrid({ recommendations }: Props) {
  if (recommendations.length === 0) return null;

  return (
    <div className="mt-6 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {recommendations.map((rec) => (
        <RecommendationCard key={rec.title} recommendation={rec} />
      ))}
    </div>
  );
}