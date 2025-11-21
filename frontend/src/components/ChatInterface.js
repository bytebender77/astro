import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { FiSend, FiUser, FiCpu } from 'react-icons/fi';
import { toast } from 'react-toastify';
import './ChatInterface.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const SUGGESTED_QUESTIONS = {
  career: [
    "What does my chart say about my career prospects?",
    "When is a good time for a job change?",
    "What career path suits me best according to my chart?"
  ],
  marriage: [
    "What does my 7th house indicate about marriage?",
    "When is a favorable time for marriage?",
    "How can I improve my relationships?"
  ],
  finance: [
    "What are my financial prospects?",
    "When should I invest or start a business?",
    "What remedies can improve my wealth?"
  ],
  general: [
    "Give me an overview of my birth chart",
    "What are my strengths according to my planets?",
    "What life lessons should I focus on?"
  ]
};

const ChatInterface = ({ sessionId, chartData }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedContext, setSelectedContext] = useState('general');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Send initial greeting
    const greeting = {
      role: 'assistant',
      content: `Namaste! 🙏 I've analyzed your birth chart. Your ascendant is ${chartData.ascendant.sign}, and your Moon is in ${chartData.planets.Moon.sign} in the ${chartData.moon_nakshatra.name} Nakshatra. I'm here to provide guidance on your life path. What would you like to explore today?`,
      timestamp: new Date()
    };
    setMessages([greeting]);
  }, [chartData]);

  const sendMessage = async (messageText = null) => {
    const text = messageText || inputMessage.trim();
    if (!text) return;

    const userMessage = {
      role: 'user',
      content: text,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/chat`, {
        session_id: sessionId,
        message: text,
        context: selectedContext
      });

      const aiMessage = {
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error:', error);
      toast.error('Failed to get response. Please try again.');
      
      const errorMessage = {
        role: 'assistant',
        content: 'I apologize, but I encountered an error. Please try asking your question again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>AI Jyotish Consultation</h2>
        <div className="context-selector">
          <label>Focus Area:</label>
          <select 
            value={selectedContext} 
            onChange={(e) => setSelectedContext(e.target.value)}
          >
            <option value="general">General Guidance</option>
            <option value="career">Career & Profession</option>
            <option value="marriage">Marriage & Relationships</option>
            <option value="finance">Finance & Wealth</option>
            <option value="health">Health & Wellbeing</option>
            <option value="education">Education & Learning</option>
            <option value="spiritual">Spiritual Growth</option>
          </select>
        </div>
      </div>

      <div className="suggested-questions">
        <p>Quick questions:</p>
        <div className="question-chips">
          {SUGGESTED_QUESTIONS[selectedContext].map((question, idx) => (
            <button
              key={idx}
              className="question-chip"
              onClick={() => sendMessage(question)}
              disabled={loading}
            >
              {question}
            </button>
          ))}
        </div>
      </div>

      <div className="messages-container">
        {messages.map((message, idx) => (
          <div key={idx} className={`message ${message.role}`}>
            <div className="message-icon">
              {message.role === 'user' ? <FiUser /> : <FiCpu />}
            </div>
            <div className="message-content">
              <div className="message-text">{message.content}</div>
              <div className="message-time">
                {message.timestamp.toLocaleTimeString()}
              </div>
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="message assistant">
            <div className="message-icon"><FiCpu /></div>
            <div className="message-content">
              <div className="typing-indicator">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <textarea
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask about your chart, life guidance, or specific concerns..."
          rows="2"
          disabled={loading}
        />
        <button 
          onClick={() => sendMessage()} 
          disabled={loading || !inputMessage.trim()}
          className="send-btn"
        >
          <FiSend />
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;