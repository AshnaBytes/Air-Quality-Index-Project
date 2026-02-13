export default function ForecastCard({ label, value }) {
  return (
    <div className="forecast-card">
      <h3>{label}</h3>
      <div className="forecast-value">{value.toFixed(1)}</div>
      <span>AQI</span>
    </div>
  );
}
