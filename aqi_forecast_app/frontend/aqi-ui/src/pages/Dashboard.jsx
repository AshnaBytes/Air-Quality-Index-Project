import { useEffect, useState } from "react";
import { fetchAQIForecast } from "../api/aqiService";

import TodayCard from "../components/TodayCard";
import ForecastCard from "../components/ForecastCard";
import AQIChart from "../components/AQIChart";
import WeatherDetailCard from "../components/WeatherDetailCard";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAQIForecast()
      .then(setData)
      .catch((err) => {
        console.error(err);
        setError("Failed to load AQI data");
      });
  }, []);

  if (error) return <div className="loading">{error}</div>;
  if (!data) return <div className="loading">Loading AQI data… 🌫️</div>;

  const { today, forecast } = data;

  return (
  <div className="dashboard">

    {/* MAIN HEADER */}
    <h1 className="title">
      Air Quality Intelligence Dashboard
    </h1>

    <p className="subtitle">
      Real-Time AQI Monitoring & AI-Powered 3-Day Forecasting
    </p>


    <div className="grid-layout">

    

      {/* LEFT PANEL */}
      <div className="left-panel">

        {/* TODAY WRAPPER GLASS BOX */}
        <div className="glass-card today-wrapper">

        {/* LOCATION TOP LEFT */}
        <div className="location-inline">📍 Karachi, Pakistan </div>

        <h2 className="today-section-heading"> Today’s Air Quality Overview </h2>

        <TodayCard
          aqi={today?.aqi}
          date={today?.date}
        />

      </div>

        {/* TODAY HIGHLIGHTS */}
        <div className="glass-card highlights-box">
          <h3 className="section-heading">
            Environmental Conditions
          </h3>

          <div className="details-grid">
            <WeatherDetailCard
              title="Humidity"
              value={today?.humidity}
              unit="%"
              icon="💧"
            />
            <WeatherDetailCard
              title="Rain"
              value={today?.rain}
              unit="mm"
              icon="🌧"
            />
            <WeatherDetailCard
              title="Pressure"
              value={today?.pressure}
              unit="hPa"
              icon="🌡️"
            />
            <WeatherDetailCard
              title="Wind"
              value={today?.wind_speed}
              unit="km/h"
              icon="🌬️"
            />
          </div>
        </div>

      </div>

      {/* RIGHT PANEL */}
      <div className="right-panel">

        {/* FORECAST */}
        <div className="glass-card forecast-section">
          <h3 className="section-heading">
            3-Day Air Quality Outlook
          </h3>

          <div className="forecast-row">
            {forecast.map((day, index) => (
              <ForecastCard key={index} day={day} />
            ))}
          </div>
        </div>

        {/* TREND CHART */}
        <AQIChart
          today={today}
          forecast={forecast}
          title="AQI Trend Analysis"
        />

      </div>
    </div>
  </div>
);
}
