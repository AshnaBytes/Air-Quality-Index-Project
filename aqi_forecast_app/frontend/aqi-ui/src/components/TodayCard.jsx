function getAQICategory(aqi) {
  if (aqi == null) return "Loading";
  if (aqi > 200) return "Hazardous";
  if (aqi > 150) return "Unhealthy";
  if (aqi > 100) return "Unhealthy for Sensitive Groups";
  if (aqi > 50) return "Moderate";
  return "Good";
}

export default function TodayCard({ aqi, date }) {
  const safeAQI =
    typeof aqi === "number" && !isNaN(aqi)
      ? aqi
      : null;

  const category = getAQICategory(safeAQI);

  return (
    <div className="today-card glass-card">

      <div className="today-label">
        Current AQI
      </div>

      <div className="today-aqi">
        {safeAQI !== null ? safeAQI.toFixed(1) : "--"}
      </div>

      <p className="aqi-category">
        {safeAQI !== null ? category : "Fetching data..."}
      </p>

      <p className="today-date">
        {date || "--"}
      </p>
    </div>
  );
}
