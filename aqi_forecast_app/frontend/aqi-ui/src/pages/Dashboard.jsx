import { useEffect, useState } from "react";
import { fetchAQIForecast } from "../api/aqiService";

import TodayCard from "../components/TodayCard";
import ForecastCard from "../components/ForecastCard";
import HazardBanner from "../components/HazardBanner";

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchAQIForecast()
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return <div className="loading">Loading AQI data… 🌫️</div>;
  }

  return (
    <div className="app">
      <h1>🌫️ Karachi Air Quality Forecast</h1>
      <p className="subtitle">Next 3-Day AQI Prediction</p>

      {/* 🚨 Hazard Banner */}
      <HazardBanner aqi={data.today.aqi} />

      {/* 📅 Today */}
      <TodayCard
        aqi={data.today.aqi}
        date={data.today.date}
      />

      {/* 🔮 Forecast */}
      <div className="forecast-row">
        {data.forecast.map((item, idx) => (
          <ForecastCard
            key={idx}
            label={item.date}
            value={item.aqi}
          />
        ))}
      </div>
    </div>
  );
}
