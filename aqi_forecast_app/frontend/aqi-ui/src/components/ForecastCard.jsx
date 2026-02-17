import { getWeatherIcon } from "../utils/getWeatherIcon";

function getAQICategory(aqi) {
  if (aqi > 200) return "Hazardous";
  if (aqi > 150) return "Unhealthy";
  if (aqi > 100) return "Sensitive";
  if (aqi > 50) return "Moderate";
  return "Good";
}

export default function ForecastCard({ day }) {
  const icon = getWeatherIcon(day.aqi, day.rain);
  const category = getAQICategory(day.aqi);

  return (
    <div className="forecast-card glass-card">
      <p className="forecast-date">
        {new Date(day.date).toLocaleDateString("en-US", {
          weekday: "short",
        })}
      </p>

      <div className="forecast-icon">{icon}</div>

      <div className="forecast-value">{day.aqi.toFixed(1)}</div>

      <p className="forecast-category">{category}</p>
    </div>
  );
}
