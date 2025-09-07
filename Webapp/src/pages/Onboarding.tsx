import React, { useState } from 'react';
import { SEED_TOPICS } from '../lib/topics';
import { saveSelectedTopics } from '../lib/storage';
import { postSelection } from '../api/selections';

const MIN = 1;
const MAX = 3;

export default function Onboarding() {
  const [selected, setSelected] = useState<string[]>([]);
  const [search, setSearch] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const filtered = SEED_TOPICS.filter(t =>
    t.label.toLowerCase().includes(search.toLowerCase())
  );

  function toggle(id: string) {
    setSelected(sel =>
      sel.includes(id)
        ? sel.filter(s => s !== id)
        : sel.length < MAX
        ? [...sel, id]
        : sel
    );
  }

  async function handleSubmit() {
    setSubmitting(true);
    saveSelectedTopics(selected);
    await postSelection({ selectedTopicIds: selected, selectedAt: new Date().toISOString() });
    const params = new URLSearchParams({ topics: selected.join(',') });
    window.open(`/chat?${params.toString()}`, '_blank');
    setSubmitting(false);
  }

  return (
    <div className="min-h-screen flex flex-col items-center p-4">
      <header className="mb-6 text-2xl font-bold">Career Path Finder</header>
      <input
        className="mb-4 px-3 py-2 border rounded w-full max-w-md"
        placeholder="Search interests..."
        value={search}
        onChange={e => setSearch(e.target.value)}
      />
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3 w-full max-w-2xl mb-6">
        {filtered.map(topic => (
          <button
            key={topic.id}
            className={`rounded-full px-4 py-2 border flex items-center gap-2 transition
              ${selected.includes(topic.id) ? 'bg-blue-500 text-white' : 'bg-white hover:bg-blue-100'}
            `}
            aria-pressed={selected.includes(topic.id)}
            onClick={() => toggle(topic.id)}
            disabled={submitting}
          >
            {/* Icon placeholder */}
            <span>{topic.icon ? topic.icon : '•'}</span>
            {topic.label}
          </button>
        ))}
      </div>
      <div className="flex gap-2">
        <button
          className="px-6 py-2 rounded bg-blue-600 text-white disabled:opacity-50"
          onClick={handleSubmit}
          disabled={submitting || (selected.length < MIN && selected.length !== 0)}
        >
          {submitting ? 'Submitting...' : 'Submit'}
        </button>
        <button
          className="px-6 py-2 rounded bg-gray-300 text-gray-700"
          onClick={() => handleSubmit()}
          disabled={submitting}
        >
          Skip
        </button>
      </div>
      <div className="mt-2 text-sm text-gray-500">
        Select {MIN}–{MAX} interests (or skip)
      </div>
    </div>
  );
}
