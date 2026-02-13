export default function AQICard({ value, date }) {
  if (value == null) return null;

  const level =
    value > 150 ? "hazard" :
    value > 100 ? "unhealthy" :
    "moderate";

  return (
    <div className={`aqi-card ${level}`}>
      <h2>Today</h2>
      <div className="aqi-value">{value.toFixed(1)}</div>
      <span>{date}</span>
    </div>
  );
}
