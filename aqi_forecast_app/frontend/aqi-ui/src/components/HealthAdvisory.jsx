import React from "react";

const getAdvisory = (aqi) => {
  if (!aqi) return {};

  if (aqi <= 50) {
    return {
      level: "Good",
      message: "Air quality is excellent. Enjoy your day outdoors!",
      color: "#22c55e"
    };
  }

  if (aqi <= 100) {
    return {
      level: "Moderate",
      message: "Air quality is acceptable. Sensitive individuals should take precautions.",
      color: "#eab308"
    };
  }

  if (aqi <= 150) {
    return {
      level: "Unhealthy for Sensitive Groups",
      message: "Sensitive groups should reduce prolonged outdoor exertion.",
      color: "#d56f26"
    };
  }

  if (aqi <= 200) {
    return {
      level: "Unhealthy",
      message: "Limit outdoor activities. Consider wearing a mask.",
      color: "#d13131"
    };
  }

  return {
    level: "Very Unhealthy",
    message: "Avoid going outside. Stay indoors and use air purification if possible.",
    color: "#7c3aed"
  };
};

const HealthAdvisory = ({ aqi }) => {
  const advisory = getAdvisory(aqi);

  return (
    <div className="advisory-content">
      <h3 className="section-heading">⚠ Health Advisory For Today</h3>

      <div
        className="advisory-box"
        style={{ borderLeft: `5px solid ${advisory.color}` }}
      >
        <p className="advisory-level" style={{ color: advisory.color }}>
          {advisory.level}
        </p>

        <p className="advisory-message">
          {advisory.message}
        </p>
      </div>
    </div>
  );
};

export default HealthAdvisory;
