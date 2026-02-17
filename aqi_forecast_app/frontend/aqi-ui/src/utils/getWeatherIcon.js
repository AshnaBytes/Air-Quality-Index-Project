export function getWeatherIcon(aqi, rain) {
  if (rain > 0) return "🌧️";
  if (aqi < 50) return "☀️";
  if (aqi < 100) return "🌤️";
  if (aqi < 150) return "🌥️";
  return "🌫️";
}
