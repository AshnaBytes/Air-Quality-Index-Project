import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

export default function AQIChart({ today, forecast }) {
  const chartData = [
    { date: "Today", aqi: today.aqi },
    ...forecast.map((f, i) => ({
      date: `Day ${i + 1}`,
      aqi: f.aqi,
    })),
  ];

  return (
    <div className="chart-card glass-card">
      <h3 className="section-heading">AQI Trend</h3>

      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={chartData}>
          <CartesianGrid stroke="rgba(255,255,255,0.1)" />

          <XAxis dataKey="date" stroke="rgba(255,255,255,0.6)" />
          <YAxis stroke="rgba(255,255,255,0.6)" />

          <Tooltip
            contentStyle={{
              backgroundColor: "#1e293b",
              borderRadius: "12px",
              border: "none",
            }}
          />

          <Line
            type="monotone"
            dataKey="aqi"
            stroke="#8b5cf6"
            strokeWidth={3}
            dot={{ r: 6 }}
            activeDot={{ r: 8 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
