import React, { useState } from 'react';
import './App.css';
import BirthDetailsForm from './components/BirthDetailsForm';
import ChatInterface from './components/ChatInterface';
import ChartDisplay from './components/ChartDisplay';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [showChat, setShowChat] = useState(false);

  const handleChartCalculated = (data) => {
    setSessionId(data.session_id);
    setChartData(data.chart_data);
    setShowChat(true);
  };

  const handleReset = () => {
    setSessionId(null);
    setChartData(null);
    setShowChat(false);
  };

  return (
    <div className="App">
      <ToastContainer position="top-right" autoClose={3000} />
      
      <header className="app-header">
        <div className="header-content">
          <h1>🌟 AI Jyotish Guru</h1>
          <p>Vedic Wisdom Meets Artificial Intelligence</p>
        </div>
      </header>

      <main className="app-main">
        {!showChat ? (
          <div className="welcome-section">
            <div className="welcome-card">
              <h2>Welcome to Your Personalized Astrological Journey</h2>
              <p>
                Discover insights about your life, career, relationships, and spiritual path 
                through the ancient wisdom of Vedic Astrology, enhanced by modern AI.
              </p>
              <BirthDetailsForm onChartCalculated={handleChartCalculated} />
            </div>
          </div>
        ) : (
          <div className="dashboard">
            <div className="sidebar">
              <button className="new-session-btn" onClick={handleReset}>
                + New Session
              </button>
              <ChartDisplay chartData={chartData} />
            </div>
            
            <div className="main-content">
              <ChatInterface sessionId={sessionId} chartData={chartData} />
            </div>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>
          Built with 🙏 for AstroHack • Combining Vedic tradition with AI innovation
        </p>
      </footer>
    </div>
  );
}

export default App;