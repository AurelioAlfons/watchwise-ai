import { useState } from "react";
import type { RecommendRequest } from "../types";

interface Props {
  onSubmit: (data: RecommendRequest) => void;
}

export default function PreferenceForm({ onSubmit }: Props) {
  const [form, setForm] = useState<RecommendRequest>({
    media_type: "movie",
    genre: "",
    mood: "",
    watching_with: "",
    similar_title: "",
    free_text: "",
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  return (
    <form
      className="space-y-4"
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit(form);
      }}
    >
      <select
        name="media_type"
        value={form.media_type}
        onChange={handleChange}
        className="w-full rounded border p-2"
      >
        <option value="movie">Movie</option>
        <option value="tv">TV Show</option>
        <option value="any">Any</option>
      </select>

      <input
        name="genre"
        placeholder="Genre"
        value={form.genre}
        onChange={handleChange}
        className="w-full rounded border p-2"
      />

      <input
        name="mood"
        placeholder="Mood"
        value={form.mood}
        onChange={handleChange}
        className="w-full rounded border p-2"
      />

      <input
        name="watching_with"
        placeholder="Watching with"
        value={form.watching_with}
        onChange={handleChange}
        className="w-full rounded border p-2"
      />

      <input
        name="similar_title"
        placeholder="Similar to"
        value={form.similar_title}
        onChange={handleChange}
        className="w-full rounded border p-2"
      />

      <input
        name="free_text"
        placeholder="Extra preferences"
        value={form.free_text}
        onChange={handleChange}
        className="w-full rounded border p-2"
      />

      <button
        type="submit"
        className="rounded bg-blue-600 px-4 py-2 text-white"
      >
        Recommend
      </button>
    </form>
  );
}