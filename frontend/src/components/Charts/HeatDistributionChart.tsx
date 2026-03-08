import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { useSettingsStore } from '../../stores/settingsStore'

interface HeatDistributionChartProps {
  useCases: Array<{
    name: string
    description?: string
    heat_level: 'high' | 'medium' | 'low'
  }>
}

const HEAT_COLORS = {
  high: '#ef4444',
  medium: '#f59e0b',
  low: '#6b7280',
}

const HEAT_VALUES = {
  high: 3,
  medium: 2,
  low: 1,
}

export default function HeatDistributionChart({ useCases }: HeatDistributionChartProps) {
  const { t } = useSettingsStore()

  const data = useCases.map((uc) => ({
    name: uc.name.length > 20 ? uc.name.slice(0, 20) + '...' : uc.name,
    fullName: uc.name,
    heat: HEAT_VALUES[uc.heat_level] || 1,
    heatLevel: uc.heat_level,
    fill: HEAT_COLORS[uc.heat_level] || HEAT_COLORS.low,
  }))

  if (!useCases || useCases.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No use cases available
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <h4 className="text-lg font-semibold text-gray-900">{t.charts.heatDistribution}</h4>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            layout="vertical"
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              type="number"
              domain={[0, 3]}
              ticks={[1, 2, 3]}
              tickFormatter={(value) => {
                if (value === 3) return t.analysis.heat === '热度' ? '高' : 'High'
                if (value === 2) return t.analysis.heat === '热度' ? '中' : 'Medium'
                if (value === 1) return t.analysis.heat === '热度' ? '低' : 'Low'
                return ''
              }}
            />
            <YAxis
              type="category"
              dataKey="name"
              width={100}
              tick={{ fontSize: 12 }}
            />
            <Tooltip
              formatter={(_value: number, _name: string, props: any) => [
                props.payload.heatLevel,
                t.analysis.heat,
              ]}
              labelFormatter={(label) => data.find(d => d.name === label)?.fullName || label}
            />
            <Bar dataKey="heat" radius={[0, 4, 4, 0]}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.fill} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}