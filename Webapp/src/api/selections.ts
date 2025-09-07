// Mock API handler for POST /api/selections

import type { SelectionPayload } from '../lib/types';

export async function postSelection(payload: SelectionPayload) {
  // Simulate network delay
  await new Promise((res) => setTimeout(res, 300));
  // Log to console (mock persistence)
  console.log('Received selection payload:', payload);
  return { success: true };
}
