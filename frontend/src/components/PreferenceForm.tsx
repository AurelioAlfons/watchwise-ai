import { useState } from "react";
import { Users, User, Heart, Baby, PartyPopper, Sparkles } from "lucide-react";
import Chip from "./Chip";
import type { RecommendRequest } from "../types";

interface Props {
  onSubmit: (req: RecommendRequest) => void;
  loading: boolean;
}

const GENRES = [
  "Action", "Comedy", "Drama", "Horror", "Romance", "Thriller",
  "Mystery", "Fantasy", "Animation", "Adventure", "Crime", "Science Fiction",
];

const MOODS = [
  "Chill", "Cozy", "Funny", "Sad", "Intense",
  "Feel-good", "Dark", "Romantic", "Scary", "Thought-provoking",
];

const WATCHING_WITH = [
  { value: "alone", label: "Alone", icon: User },
  { value: "partner", label: "Partner", icon: Heart },
  { value: "family", label: "Family", icon: Users },
  { value: "kids", label: "Kids", icon: Baby },
  { value: "friends", label: "Friends", icon: PartyPopper },
];

const TYPES = [
  { value: "any", label: "Either" },
  { value: "movie", label: "Movie" },
  { value: "tv", label: "Anime / Show" },
];

export default function PreferenceForm({ onSubmit, loading }: Props) {
  const [form, setForm] = useState<RecommendRequest>({ media_type: "any" });

  const update = (key: keyof RecommendRequest, value: string) =>
    setForm((f) => ({ ...f, [key]: value }));

  const toggle = (key: keyof RecommendRequest, value: string) =>
    setForm((f) => ({ ...f, [key]: f[key] === value ? "" : value }));

  return (
    <form
      onSubmit={(e) => { e.preventDefault(); onSubmit(form); }}
      className="space-y-7 max-w-2xl mx-auto bg-surface border border-border rounded-2xl shadow-xl p-5 sm:p-8"
    >
      {/* Type */}
      <div>
        <label className="block text-sm font-semibold text-white mb-2">
          What are you looking for?
        </label>
        <div className="grid grid-cols-3 gap-2">
          {TYPES.map((t) => (
            <button
              key={t.value}
              type="button"
              onClick={() => update("media_type", t.value)}
              className={`py-2.5 rounded-xl text-sm font-medium border transition-colors
                ${
                  form.media_type === t.value
                    ? "bg-gold text-ink border-gold"
                    : "bg-surfaceSoft text-muted border-border hover:border-gold/50"
                }`}
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>

      {/* Genre */}
      <div>
        <label className="block text-sm font-semibold text-white mb-1">
          Genre
        </label>
        <p className="text-xs text-muted mb-3">Pick one that fits the vibe you're after.</p>
        <div className="flex flex-wrap gap-2">
          {GENRES.map((g) => (
            <Chip
              key={g}
              label={g}
              selected={form.genre === g}
              onClick={() => toggle("genre", g)}
            />
          ))}
        </div>
      </div>

      {/* Mood */}
      <div>
        <label className="block text-sm font-semibold text-white mb-1">
          Mood
        </label>
        <p className="text-xs text-muted mb-3">What kind of headspace are you in right now?</p>
        <div className="flex flex-wrap gap-2">
          {MOODS.map((m) => (
            <Chip
              key={m}
              label={m}
              selected={form.mood === m}
              onClick={() => toggle("mood", m)}
            />
          ))}
        </div>
      </div>

      {/* Watching with */}
      <div>
        <label className="block text-sm font-semibold text-white mb-1">
          Watching with
        </label>
        <p className="text-xs text-muted mb-3">Helps tailor tone and age-appropriateness.</p>
        <div className="grid grid-cols-3 sm:grid-cols-5 gap-2">
          {WATCHING_WITH.map(({ value, label, icon: Icon }) => (
            <button
              key={value}
              type="button"
              onClick={() => toggle("watching_with", value)}
              className={`flex flex-col items-center gap-1.5 py-3 rounded-xl text-xs font-medium border transition-colors
                ${
                  form.watching_with === value
                    ? "bg-gold text-ink border-gold"
                    : "bg-surfaceSoft text-muted border-border hover:border-gold/50"
                }`}
            >
              <Icon size={18} />
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* Similar title */}
      <div>
        <label className="block text-sm font-semibold text-white mb-1">
          Similar to
        </label>
        <p className="text-xs text-muted mb-2">
          A movie or show you loved — we'll find something with a similar vibe.
        </p>
        <input
          className="w-full bg-surfaceSoft border border-border rounded-xl p-3 text-white placeholder-muted/60 focus:outline-none focus:border-gold"
          placeholder="e.g. Parasite, Attack on Titan, Inception"
          onChange={(e) => update("similar_title", e.target.value)}
        />
      </div>

      {/* Free text */}
      <div>
        <label className="block text-sm font-semibold text-white mb-1">
          Anything else?
        </label>
        <p className="text-xs text-muted mb-2">
          Length, subtitles vs dubbed, actors, things to avoid — totally optional.
        </p>
        <textarea
          rows={3}
          className="w-full bg-surfaceSoft border border-border rounded-xl p-3 text-white placeholder-muted/60 focus:outline-none focus:border-gold resize-none"
          placeholder="e.g. something with a twist ending, not too long"
          onChange={(e) => update("free_text", e.target.value)}
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full flex items-center justify-center gap-2 bg-gold text-ink rounded-xl py-3.5 font-semibold hover:brightness-95 active:scale-[0.99] transition disabled:opacity-50 disabled:active:scale-100"
      >
        <Sparkles size={18} />
        {loading ? "Finding picks..." : "Get Recommendations"}
      </button>
    </form>
  );
}