import React, { useState } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';
import './BirthDetailsForm.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Major Indian cities with coordinates
const INDIAN_CITIES = [
  { name: 'Mumbai', lat: 19.0760, lon: 72.8777, tz: 'Asia/Kolkata' },
  { name: 'Delhi', lat: 28.7041, lon: 77.1025, tz: 'Asia/Kolkata' },
  { name: 'Bangalore', lat: 12.9716, lon: 77.5946, tz: 'Asia/Kolkata' },
  { name: 'Kolkata', lat: 22.5726, lon: 88.3639, tz: 'Asia/Kolkata' },
  { name: 'Chennai', lat: 13.0827, lon: 80.2707, tz: 'Asia/Kolkata' },
  { name: 'Hyderabad', lat: 17.3850, lon: 78.4867, tz: 'Asia/Kolkata' },
  { name: 'Pune', lat: 18.5204, lon: 73.8567, tz: 'Asia/Kolkata' },
  { name: 'Ahmedabad', lat: 23.0225, lon: 72.5714, tz: 'Asia/Kolkata' },
  { name: 'Jaipur', lat: 26.9124, lon: 75.7873, tz: 'Asia/Kolkata' },
  { name: 'Lucknow', lat: 26.8467, lon: 80.9462, tz: 'Asia/Kolkata' },
];

const BirthDetailsForm = ({ onChartCalculated }) => {
  const [formData, setFormData] = useState({
    name: '',
    date: '',
    time: '',
    city: '',
    latitude: '',
    longitude: '',
    timezone: 'Asia/Kolkata'
  });
  const [loading, setLoading] = useState(false);

  const handleCityChange = (e) => {
    const cityName = e.target.value;
    const city = INDIAN_CITIES.find(c => c.name === cityName);
    
    if (city) {
      setFormData({
        ...formData,
        city: cityName,
        latitude: city.lat,
        longitude: city.lon,
        timezone: city.tz
      });
    } else {
      setFormData({ ...formData, city: cityName });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.date || !formData.time || !formData.latitude || !formData.longitude) {
      toast.error('Please fill all required fields');
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/birth-chart`, {
        date: formData.date,
        time: formData.time,
        latitude: parseFloat(formData.latitude),
        longitude: parseFloat(formData.longitude),
        timezone: formData.timezone,
        name: formData.name
      });

      toast.success('Birth chart calculated successfully!');
      onChartCalculated(response.data);
    } catch (error) {
      console.error('Error:', error);
      toast.error('Failed to calculate birth chart. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="birth-details-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label>Name (Optional)</label>
        <input
          type="text"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          placeholder="Your name"
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Birth Date *</label>
          <input
            type="date"
            value={formData.date}
            onChange={(e) => setFormData({ ...formData, date: e.target.value })}
            required
            max={new Date().toISOString().split('T')[0]}
          />
        </div>

        <div className="form-group">
          <label>Birth Time *</label>
          <input
            type="time"
            value={formData.time}
            onChange={(e) => setFormData({ ...formData, time: e.target.value })}
            required
          />
        </div>
      </div>

      <div className="form-group">
        <label>Birth City *</label>
        <select value={formData.city} onChange={handleCityChange} required>
          <option value="">Select a city</option>
          {INDIAN_CITIES.map(city => (
            <option key={city.name} value={city.name}>{city.name}</option>
          ))}
          <option value="other">Other (Enter coordinates manually)</option>
        </select>
      </div>

      {formData.city === 'other' && (
        <div className="form-row">
          <div className="form-group">
            <label>Latitude *</label>
            <input
              type="number"
              step="0.0001"
              value={formData.latitude}
              onChange={(e) => setFormData({ ...formData, latitude: e.target.value })}
              placeholder="e.g., 28.7041"
              required
            />
          </div>

          <div className="form-group">
            <label>Longitude *</label>
            <input
              type="number"
              step="0.0001"
              value={formData.longitude}
              onChange={(e) => setFormData({ ...formData, longitude: e.target.value })}
              placeholder="e.g., 77.1025"
              required
            />
          </div>
        </div>
      )}

      <button type="submit" className="submit-btn" disabled={loading}>
        {loading ? 'Calculating...' : 'Calculate Birth Chart'}
      </button>

      <p className="form-note">
        * All data is processed securely and not stored permanently
      </p>
    </form>
  );
};

export default BirthDetailsForm;