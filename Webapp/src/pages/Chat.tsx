import React, { useEffect, useState, useRef } from 'react';
import { getSelectedTopics } from '../lib/storage';
import { SEED_TOPICS } from '../lib/topics';

function getTopicsFromQuery() {
  const params = new URLSearchParams(window.location.search);
  const ids = params.get('topics')?.split(',').filter(Boolean) || [];
  return ids.length ? ids : getSelectedTopics();
}

export default function Chat() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<{ role: string; text: string }[]>([]);
  const [topics, setTopics] = useState<string[]>([]);
  const [typing, setTyping] = useState(false);
  const listRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setTopics(getTopicsFromQuery());
  }, []);

  useEffect(() => {
    listRef.current?.scrollTo(0, listRef.current.scrollHeight);
  }, [messages]);

  function send() {
    if (!input.trim()) return;
    setMessages(msgs => [...msgs, { role: 'user', text: input }]);
    setInput('');
    setTyping(true);
    setTimeout(() => {
      setMessages(msgs => [...msgs, { role: 'ai', text: 'This is a mock response.' }]);
      setTyping(false);
    }, 800);
  }

  return (
    <div className="min-h-screen flex flex-col items-center p-4">
      <header className="mb-4 text-xl font-bold">Career Chat</header>
      <div className="flex gap-2 mb-4 flex-wrap">
        {topics.map(id => {
          const t = SEED_TOPICS.find(t => t.id === id);
          return t ? (
            <span key={id} className="px-3 py-1 rounded-full bg-blue-100 text-blue-800 text-sm">{t.label}</span>
          ) : null;
        })}
      </div>
      <div ref={listRef} className="flex-1 w-full max-w-xl border rounded p-4 mb-4 overflow-y-auto bg-white" style={{ minHeight: 200, maxHeight: 300 }}>
        {messages.map((m, i) => (
          <div key={i} className={`mb-2 ${m.role === 'user' ? 'text-right' : 'text-left'}`}>
            <span className={m.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'} style={{ borderRadius: 12, padding: '6px 12px', display: 'inline-block' }}>{m.text}</span>
          </div>
        ))}
        {typing && <div className="text-gray-400">AI is typing...</div>}
      </div>
      <form className="flex w-full max-w-xl gap-2" onSubmit={e => { e.preventDefault(); send(); }}>
        <input
          className="flex-1 px-3 py-2 border rounded"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button className="px-4 py-2 rounded bg-blue-600 text-white" type="submit">Send</button>
      </form>
    </div>
  );
}
