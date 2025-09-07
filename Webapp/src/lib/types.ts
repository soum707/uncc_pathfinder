export interface Topic {
  id: string;        // slug‑like unique id
  label: string;     // display name
  category?: string; // optional grouping (e.g., Industry, Field, Title)
  icon?: string;     // lucide icon name
}

export interface SelectionPayload {
  selectedTopicIds: string[]; // 1–3 items
  selectedAt: string;         // ISO timestamp
}
