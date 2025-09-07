// Helpers for localStorage persistence

const STORAGE_KEY = 'selectedTopics';

export function saveSelectedTopics(topicIds: string[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(topicIds));
}

export function getSelectedTopics(): string[] {
  const data = localStorage.getItem(STORAGE_KEY);
  if (!data) return [];
  try {
    return JSON.parse(data);
  } catch {
    return [];
  }
}

export function clearSelectedTopics() {
  localStorage.removeItem(STORAGE_KEY);
}
