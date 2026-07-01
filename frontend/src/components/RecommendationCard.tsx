import type { Recommendation } from "../types";

interface Props {
  recommendation: Recommendation;
}

export default function RecommendationCard({ recommendation }: Props) {
  return (
    <div className="rounded-lg border p-4 shadow">
      {recommendation.poster_url && (
        <img
          src={recommendation.poster_url}
          alt={recommendation.title}
          className="mb-3 w-full rounded"
        />
      )}

      <h2 className="text-xl font-bold">{recommendation.title}</h2>

      <p className="text-sm text-gray-500">
        {recommendation.genre}
      </p>

      <p className="mt-2">{recommendation.reason}</p>

      <div className="mt-3 space-y-1 text-sm">
        <p><strong>Runtime:</strong> {recommendation.runtime ?? "N/A"}</p>
        <p><strong>Age:</strong> {recommendation.age_rating ?? "N/A"}</p>
        <p><strong>Rating:</strong> ⭐ {recommendation.rating ?? "N/A"}</p>
        <p>
          <strong>Watch:</strong>{" "}
          {recommendation.where_to_watch.length
            ? recommendation.where_to_watch.join(", ")
            : "Unavailable"}
        </p>
      </div>
    </div>
  );
}