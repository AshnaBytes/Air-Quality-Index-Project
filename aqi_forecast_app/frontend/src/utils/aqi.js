export function aqiInfo(aqi) {
  if (aqi <= 50) return { label: "Good", color: "bg-green-500", icon: "🌤️" }
  if (aqi <= 100) return { label: "Moderate", color: "bg-yellow-400", icon: "🌥️" }
  if (aqi <= 150) return { label: "Unhealthy", color: "bg-orange-500", icon: "🌫️" }
  return { label: "Hazardous", color: "bg-red-600", icon: "☠️" }
}
