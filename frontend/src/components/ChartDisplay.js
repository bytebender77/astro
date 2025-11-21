import React, { useState } from 'react';
import './ChartDisplay.css';

const ChartDisplay = ({ chartData }) => {
  const [activeTab, setActiveTab] = useState('overview');

  if (!chartData) return null;

  const renderOverview = () => (
    <div className="chart-section">
      <h3>Chart Overview</h3>
      
      <div className="info-card">
        <h4>Ascendant (Lagna)</h4>
        <p className="highlight">{chartData.ascendant.sign}</p>
        <p className="detail">{chartData.ascendant.degree}°</p>
      </div>

      <div className="info-card">
        <h4>Moon Sign</h4>
        <p className="highlight">{chartData.planets.Moon.sign}</p>
        <p className="detail">Nakshatra: {chartData.moon_nakshatra.name}</p>
        <p className="detail">Pada: {chartData.moon_nakshatra.pada}</p>
      </div>

      <div className="info-card">
        <h4>Sun Sign</h4>
        <p className="highlight">{chartData.planets.Sun.sign}</p>
        <p className="detail">{chartData.planets.Sun.degree}°</p>
      </div>
    </div>
  );

  const renderPlanets = () => (
    <div className="chart-section">
      <h3>Planetary Positions</h3>
      <div className="planets-list">
        {Object.entries(chartData.planets).map(([planet, data]) => (
          <div key={planet} className="planet-card">
            <h4>{planet}</h4>
            <p><strong>Sign:</strong> {data.sign}</p>
            <p><strong>Degree:</strong> {data.degree}°</p>
            <p><strong>Nakshatra:</strong> {data.nakshatra}</p>
            {chartData.strengths[planet] && (
              <p className={`strength ${chartData.strengths[planet].status.toLowerCase()}`}>
                <strong>Strength:</strong> {chartData.strengths[planet].status}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );

  const renderHouses = () => (
    <div className="chart-section">
      <h3>House System</h3>
      <div className="houses-list">
        {chartData.houses.map((house) => (
          <div key={house.house} className="house-card">
            <h4>{house.house}th House</h4>
            <p><strong>Sign:</strong> {house.sign}</p>
            <p className="house-desc">{house.description}</p>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="chart-display">
      <div className="chart-tabs">
        <button 
          className={activeTab === 'overview' ? 'active' : ''}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button 
          className={activeTab === 'planets' ? 'active' : ''}
          onClick={() => setActiveTab('planets')}
        >
          Planets
        </button>
        <button 
          className={activeTab === 'houses' ? 'active' : ''}
          onClick={() => setActiveTab('houses')}
        >
          Houses
        </button>
      </div>

      <div className="chart-content">
        {activeTab === 'overview' && renderOverview()}
        {activeTab === 'planets' && renderPlanets()}
        {activeTab === 'houses' && renderHouses()}
      </div>
    </div>
  );
};

export default ChartDisplay;