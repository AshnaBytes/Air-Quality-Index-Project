import { LineChart, Line, XAxis, YAxis, Tooltip } from "recharts"

const mock = [
  { day: "Mon", aqi: 90 },
  { day: "Tue", aqi: 88 },
  { day: "Wed", aqi: 86 },
  { day: "Thu", aqi: 84 },
  { day: "Fri", aqi: 82 },
]

export default function AQIChart() {
  return (
    <div className="bg-card p-6 rounded-xl">
      <h3 className="mb-4">AQI Trend</h3>
      <LineChart width={700} height={250} data={mock}>
        <XAxis dataKey="day" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="aqi" stroke="#facc15" />
      </LineChart>
    </div>
  )
}
