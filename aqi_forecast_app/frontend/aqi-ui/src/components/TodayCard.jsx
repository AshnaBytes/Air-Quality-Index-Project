import React from "react";

export default function TodayCard({ aqi, date }) {
  return (
    <div className="card big">
      <h2>Karachi</h2>
      <h1>{aqi.toFixed(1)}</h1>
      <p>AQI • {date}</p>
      <span>🌫️</span>
    </div>
  );
}
