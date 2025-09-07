a# Agent Prompt: Build Student Career‑Path Interest Selection → RAG Handoff (Structure Only)

## Objective

Create a responsive web app skeleton that asks students to select interest bubbles (Reddit‑style), guiding them into possible **career paths** (industry, field, title). Persist their selections and route them to a new tab containing a placeholder LLM RAG interaction page. **Do not integrate any real LLM or RAG backends yet**—just the UI/UX flow and mock endpoints.

## Deliverables

1. **Codebase** with an easy front‑end stack for beginners (React + Vite + TypeScript recommended for simplicity; Next.js optional).
2. **Two pages:**
   - `/` (Onboarding): career interest bubble selection grid with search/filter, selectable chips, submit CTA.
   - `/chat` (RAG Placeholder): simple chat UI scaffold (input box, message list, mock streaming), reads selected interests from persisted storage or URL.
3. **Persistence:** store selections to `localStorage` and POST to a mock API route `/api/selections` (no external DB required; can log to console or use in‑memory store).
4. **Navigation:** on submit from `/`, open `/chat` in a **new tab** (or same tab, both acceptable) and pass selections via `?topics=` query string **and** rely on localStorage as fallback.
5. **README** with install/run instructions and short architecture overview.

## Tech Stack (defaults)

- **Framework:** React + Vite + TypeScript (simpler for new devs)
- **Styling:** Tailwind CSS (easy utility styling)
- **UI Components:** shadcn/ui optional for chips/buttons
- **Icons:** lucide-react
- **State:** local component state + `localStorage`
- **API:** lightweight mock handler (Express or Vite dev server middleware)

## User Flow

1. **Landing **``
   - Header: placeholder name/logo.
   - Search input + category filter dropdown.
   - Responsive grid of career interest bubbles (chips) with: label, optional icon, and selectable state.
   - Rules: **min 1, max 3 selections**, but users can skip entirely.
   - On Submit: persist to localStorage, POST to `/api/selections`, then open `/chat?topics=...`.
2. **RAG Placeholder **``
   - Header shows selected topics as read‑only chips.
   - Chat area: message list + input + “Send” button; messages append locally (no backend).
   - Optional: mock “typing” indicator.

## Data Structures

```ts
export type Topic = {
  id: string;        // slug‑like unique id
  label: string;     // display name
  category?: string; // optional grouping (e.g., Industry, Field, Title)
  icon?: string;     // lucide icon name
};

export type SelectionPayload = {
  selectedTopicIds: string[]; // 1–3 items
  selectedAt: string;         // ISO timestamp
};
```

### Sample Topics (seed)

```ts
export const SEED_TOPICS: Topic[] = [
  { id: 'tech', label: 'Technology (Industry)', icon: 'Cpu' },
  { id: 'healthcare', label: 'Healthcare (Industry)', icon: 'HeartPulse' },
  { id: 'finance', label: 'Finance (Industry)', icon: 'LineChart' },
  { id: 'design', label: 'Design (Field)', icon: 'Palette' },
  { id: 'engineering', label: 'Engineering (Field)', icon: 'Wrench' },
  { id: 'data', label: 'Data Science (Field)', icon: 'Database' },
  { id: 'software_eng', label: 'Software Engineer (Title)', icon: 'Code2' },
  { id: 'project_manager', label: 'Project Manager (Title)', icon: 'ClipboardList' },
  { id: 'researcher', label: 'Researcher (Title)', icon: 'FlaskConical' }
];
```

## Implementation Notes

- **Accessibility:** chips as buttons with `aria-pressed`; focus styles.
- **Responsive layout:** 2–6 columns depending on breakpoints.
- **Persistence:**
  - `localStorage.setItem('selectedTopics', JSON.stringify(string[]))`
  - query param `topics=...` as redundancy.
- **Mock API:** POST `/api/selections` logs payload; always return success.
- **Styling cues:** Reddit‑like chip/tag cloud; rounded, hover effects.

## Folder Structure (React + Vite)

```
src/
  pages/
    Onboarding.tsx
    Chat.tsx
  components/
    Bubble.tsx
    BubbleGrid.tsx
    TopicSearch.tsx
  lib/
    topics.ts
    storage.ts
    types.ts
  api/
    selections.ts (mock handler)
```

## Acceptance Criteria

-

## README Content (outline)

- Install: `npm i`
- Run: `npm run dev`
- Configure: edit `lib/topics.ts` for career interests; update min/max rules.
- Notes: No real LLM; mock only; plug future endpoints later.

## Out of Scope (for now)

- Real RAG/LLM calls, DB persistence, auth, deployment config, tests.

## Instructions to Execute

1. Scaffold React + Vite + TypeScript project with Tailwind.
2. Implement `/` page with bubble selection (min=1, max=3, skip allowed).
3. Add `storage.ts` helpers.
4. Implement `/api/selections` mock handler.
5. Implement `/chat` placeholder page with selected chips + simple chat.
6. Deliver code + README.

