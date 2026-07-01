import type { Recommendation } from "../types";
import RecommendationCard from "./RecommendationCard";

export default function ResultsGrid({ recs }: { recs: Recommendation[] }) {
  if (recs.length === 0) return null;
  return (
    <div className="max-w-4xl mx-auto mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
      {recs.map((r) => (
        <RecommendationCard key={r.title} rec={r} />
      ))}
    </div>
  );
}