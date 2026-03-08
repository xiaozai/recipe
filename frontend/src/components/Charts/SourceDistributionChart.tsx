import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'
import { useSettingsStore } from '../../stores/settingsStore'

interface SourceDistributionChartProps {
  sourceCounts: Record<string, number>
}

const COLORS = {
  github: '#2dba4e',
  hackernews: '#ff6600',
  reddit: '#ff4500',
  web: '#4285f4',
}

const SOURCE_LABELS: Record<string, { en: string; zh: string }> = {
  github: { en: 'GitHub', zh: 'GitHub' },
  hackernews: { en: 'Hacker News', zh: 'Hacker News' },
  reddit: { en: 'Reddit', zh: 'Reddit' },
  web: { en: 'Web', zh: 'Web' },
}

export default function SourceDistributionChart({ sourceCounts }: SourceDistributionChartProps) {
  const { t, language } = useSettingsStore()

  const data = Object.entries(sourceCounts)
    .filter(([_, count]) => count > 0)
    .map(([source, count]) => ({
      name: SOURCE_LABELS[source]?.[language] || source,
      value: count,
      source,
    }))

  if (data.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No data available
      </div>
    )
  }

  return (
    <div className="h-64">
      <h4 className="text-lg font-semibold text-gray-900 mb-4">{t.charts.sourceDistribution}</h4>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={50}
            outerRadius={80}
            paddingAngle={5}
            dataKey="value"
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
          >
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS[entry.source as keyof typeof COLORS] || '#8884d8'}
              />
            ))}
          </Pie>
          <Tooltip
            formatter={(value: number) => [`${value} ${t.analysis.items}`, '']}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}