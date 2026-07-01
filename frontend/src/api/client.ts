import type { RecommendRequest, RecommendResponse } from "../types";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function getRecommendations(
  req: RecommendRequest
): Promise<RecommendResponse> {
  const res = await fetch(`${API_URL}/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });

  if (!res.ok) {
    throw new Error("Failed to fetch recommendations");
  }

  return res.json();
}