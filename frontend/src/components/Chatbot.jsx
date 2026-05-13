import React, { useState } from 'react';
import { MessageCircle, Send, X } from 'lucide-react';
import { askTelecomAssistant } from '../services/api';
import QuerySuggestions from './QuerySuggestions';

export default function Chatbot({ onResult, onLoading }) {
  const [open, setOpen] = useState(true);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([{ role: 'assistant', text: 'Ask me about churn, revenue, ARPU, risk, products, or network quality.' }]);
  const [loading, setLoading] = useState(false);

  async function send(text = input) {
    if (!text.trim()) return;
    setInput('');
    setLoading(true); onLoading?.(true);
    setMessages(prev => [...prev, { role: 'user', text }]);
    try {
      const result = await askTelecomAssistant(text);
      onResult(result);
      setMessages(prev => [...prev, { role: 'assistant', text: result.answer }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', text: 'Backend is not reachable. Start FastAPI on port 8001.' }]);
    } finally {
      setLoading(false); onLoading?.(false);
    }
  }

  if (!open) return <button className="chat-fab" onClick={() => setOpen(true)}><MessageCircle size={24} /></button>;

  return <aside className="chatbot-panel"><div className="chatbot-header"><strong>Telecom Assistant</strong><button onClick={() => setOpen(false)}><X size={18} /></button></div><QuerySuggestions onSelect={send} /><div className="chatbot-messages">{messages.map((m, i) => <div key={i} className={`msg ${m.role}`}>{m.text}</div>)}{loading && <div className="msg assistant loading-dot">Analyzing telecom data and generating chart...</div>}</div><div className="chatbot-input"><input value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && send()} placeholder="Ask a telecom KPI question..."/><button onClick={() => send()}><Send size={18}/></button></div></aside>;
}
