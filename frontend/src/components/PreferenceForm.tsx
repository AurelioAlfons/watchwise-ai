import { useState } from "react";
import type { RecommendRequest } from "../types";

interface Props {
  onSubmit: (req: RecommendRequest) => void;
  loading: boolean;
}

export default function PreferenceForm({ onSubmit, loading }: Props) {
  const [form, setForm] = useState<RecommendRequest>({ media_type: "any" });

  const update = (key: keyof RecommendRequest, value: string) =>
    setForm((f) => ({ ...f, [key]: value }));

  return (
    <form
      onSubmit={(e) => { e.preventDefault(); onSubmit(form); }}
      className="space-y-5 max-w-xl mx-auto bg-white p-6 rounded-2xl shadow"
    >
      {/* Type */}
      <div>
        <select
          className="w-full border rounded-lg p-2"
          onChange={(e) => update("media_type", e.target.value)}
        >
          <option value="any">Movie or Anime/Show</option>
          <option value="movie">Movie</option>
          <option value="tv">Anime / TV Show</option>
        </select>
        <p className="text-xs text-gray-400 mt-1">
          Looking for a movie, a series/anime, or don't mind either?
        </p>
      </div>

      {/* Genre */}
      <div>
        <input
          className="w-full border rounded-lg p-2"
          placeholder="e.g. thriller, fantasy, romance, action"
          onChange={(e) => update("genre", e.target.value)}
        />
        <p className="text-xs text-gray-400 mt-1">
          Genre — pick one that fits, like thriller, comedy, sci-fi, fantasy, horror, romance.
        </p>
      </div>

      {/* Mood */}
      <div>
        <input
          className="w-full border rounded-lg p-2"
          placeholder="e.g. cozy, sad, funny, chill, intense"
          onChange={(e) => update("mood", e.target.value)}
        />
        <p className="text-xs text-gray-400 mt-1">
          What are you in the mood for right now? e.g. sad, funny, chill, intense, feel-good.
        </p>
      </div>

      {/* Watching with */}
      <div>
        <select
          className="w-full border rounded-lg p-2"
          onChange={(e) => update("watching_with", e.target.value)}
        >
          <option value="">Watching with...</option>
          <option value="alone">Alone</option>
          <option value="partner">Partner</option>
          <option value="family">Family</option>
          <option value="kids">Kids</option>
          <option value="friends">Friends</option>
        </select>
        <p className="text-xs text-gray-400 mt-1">
          Who's watching? This helps tailor tone and age-appropriateness — e.g. yourself, with friends, or family movie night.
        </p>
      </div>

      {/* Similar title */}
      <div>
        <input
          className="w-full border rounded-lg p-2"
          placeholder="e.g. Parasite, Attack on Titan, Inception"
          onChange={(e) => update("similar_title", e.target.value)}
        />
        <p className="text-xs text-gray-400 mt-1">
          Similar to something you've already watched and loved? Enter that title and we'll find shows/movies with a similar vibe.
        </p>
      </div>

      {/* Free text */}
      <div>
        <textarea
          className="w-full border rounded-lg p-2"
          placeholder="e.g. something with a twist ending, not too long, subtitles are fine"
          onChange={(e) => update("free_text", e.target.value)}
        />
        <p className="text-xs text-gray-400 mt-1">
          Anything else worth knowing — preferred length, subtitles vs dubbed, specific actors, things to avoid, etc.
        </p>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-indigo-600 text-white rounded-lg p-2 font-medium hover:bg-indigo-700 disabled:opacity-50"
      >
        {loading ? "Finding picks..." : "Get Recommendations"}
      </button>
    </form>
  );
}