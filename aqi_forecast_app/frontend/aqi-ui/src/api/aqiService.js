const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function fetchAQIForecast() {
  const res = await fetch(`${BASE_URL}/predict`);
  
  if (!res.ok) {
    throw new Error("Failed to fetch AQI data");
  }

  return res.json();
}
