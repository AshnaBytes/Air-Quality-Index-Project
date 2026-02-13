export async function fetchAQIForecast() {
  const res = await fetch("http://127.0.0.1:8000/predict");
  if (!res.ok) throw new Error("Failed to fetch AQI data");
  return res.json();
}
