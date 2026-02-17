function getAQICategory(aqi) {
  if (aqi > 200) return "Hazardous";
  if (aqi > 150) return "Unhealthy";
  if (aqi > 100) return "Unhealthy for Sensitive Groups";
  if (aqi > 50) return "Moderate";
  return "Good";
}

export default function TodayCard({ aqi, date }) {
  const category = getAQICategory(aqi);

  return (
    <div className="today-card glass-card">
      <h2 className="city-name">Karachi</h2>

      <div className="today-aqi">{aqi.toFixed(1)}</div>

      <p className="aqi-category">{category}</p>

      <p className="today-date">AQI • {date}</p>
    </div>
  );
}
