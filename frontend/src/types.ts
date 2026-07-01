export interface RecommendRequest {
  media_type: "movie" | "tv" | "any";
  genre?: string;
  mood?: string;
  watching_with?: string;
  similar_title?: string;
  free_text?: string;
}

export interface Recommendation {
  title: string;
  media_type: string;
  reason: string;
  genre: string;
  runtime?: string;
  age_rating?: string;
  rating?: number;
  where_to_watch: string[];
  poster_url?: string;
}

export interface RecommendResponse {
  recommendations: Recommendation[];
}