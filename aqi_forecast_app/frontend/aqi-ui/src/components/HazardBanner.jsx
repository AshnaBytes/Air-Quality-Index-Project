import React from "react";

function getLevel(aqi) {
  if (aqi > 150) return { text: "HAZARDOUS ⚠️", color: "#7e0023" };
  if (aqi > 100) return { text: "UNHEALTHY 😷", color: "#ff8c00" };
  return { text: "MODERATE 🌤️", color: "#2ecc71" };
}

export default function HazardBanner({ aqi }) {
  const level = getLevel(aqi);

  return (
    <div style={{
      background: level.color,
      padding: "12px",
      borderRadius: "12px",
      textAlign: "center",
      fontWeight: "bold",
      color: "white",
      animation: "pulse 2s infinite"
    }}>
      {level.text}
    </div>
  );
}
