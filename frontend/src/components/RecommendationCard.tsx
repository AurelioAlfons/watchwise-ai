import type { Recommendation } from "../types";
import { Star, Clock, Tv } from "lucide-react";

export default function RecommendationCard({ rec }: { rec: Recommendation }) {
  return (
    <div className="bg-surface border border-border rounded-2xl p-4 flex gap-4 hover:border-gold/40 transition-colors">
      {rec.poster_url && (
        <img
          src={rec.poster_url}
          alt={rec.title}
          className="w-20 sm:w-24 h-28 sm:h-36 object-cover rounded-xl shrink-0"
        />
      )}
      <div className="flex-1 min-w-0">
        <h3 className="text-base sm:text-lg font-semibold text-white truncate">
          {rec.title}
        </h3>
        <div className="flex flex-wrap items-center gap-x-3 gap-y-1 mt-1 text-xs text-muted">
          <span>{rec.genre}</span>
          {rec.runtime && (
            <span className="flex items-center gap-1">
              <Clock size={12} /> {rec.runtime}
            </span>
          )}
          {rec.age_rating && (
            <span className="px-1.5 py-0.5 bg-surfaceSoft border border-border rounded text-[10px]">
              {rec.age_rating}
            </span>
          )}
          {rec.rating && (
            <span className="flex items-center gap-1 text-gold">
              <Star size={12} fill="currentColor" /> {rec.rating.toFixed(1)}
            </span>
          )}
        </div>
        <p className="text-sm text-slate-300 mt-2 leading-snug">{rec.reason}</p>
        {rec.where_to_watch.length > 0 && (
          <p className="flex items-center gap-1 text-xs text-muted mt-3">
            <Tv size={12} /> {rec.where_to_watch.join(", ")}
          </p>
        )}
      </div>
    </div>
  );
}