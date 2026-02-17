export default function WeatherDetailCard({ title, value, unit, icon }) {
  return (
    <div className="detail-card">
      <div className="detail-icon">{icon}</div>
      <h4>{title}</h4>
      <p className="detail-value">
        {value !== undefined && value !== null ? `${value} ${unit}` : "--"}
      </p>
    </div>
  );
}
