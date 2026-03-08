import { useSettingsStore } from '../../stores/settingsStore'

interface KeywordCloudProps {
  keywords: string[]
  weights?: number[]
}

export default function KeywordCloud({ keywords, weights }: KeywordCloudProps) {
  const { t } = useSettingsStore()

  // Calculate sizes based on weights or position
  const getKeywordSize = (index: number, weight?: number) => {
    if (weight !== undefined) {
      if (weight >= 0.8) return 'text-2xl'
      if (weight >= 0.6) return 'text-xl'
      if (weight >= 0.4) return 'text-lg'
      return 'text-base'
    }
    // Default: larger for earlier keywords
    if (index < 3) return 'text-2xl'
    if (index < 6) return 'text-xl'
    if (index < 10) return 'text-lg'
    return 'text-base'
  }

  const getKeywordColor = (index: number, weight?: number) => {
    const effectiveWeight = weight ?? (1 - index * 0.05)
    if (effectiveWeight >= 0.8) return 'text-primary-700 bg-primary-100'
    if (effectiveWeight >= 0.6) return 'text-primary-600 bg-primary-50'
    if (effectiveWeight >= 0.4) return 'text-blue-600 bg-blue-50'
    return 'text-gray-600 bg-gray-100'
  }

  // Shuffle keywords for visual variety
  const shuffledKeywords = keywords
    .map((keyword, index) => ({
      keyword,
      weight: weights?.[index],
      originalIndex: index,
    }))
    .sort(() => Math.random() - 0.5)

  if (!keywords || keywords.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No keywords available
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <h4 className="text-lg font-semibold text-gray-900">{t.charts.keywordCloud}</h4>
      <div className="flex flex-wrap gap-2 items-center justify-center p-4 bg-gray-50 rounded-lg min-h-32">
        {shuffledKeywords.map((item, index) => (
          <span
            key={`${item.keyword}-${index}`}
            className={`px-3 py-1 rounded-full font-medium transition-all hover:scale-105 cursor-default ${getKeywordSize(
              item.originalIndex,
              item.weight
            )} ${getKeywordColor(item.originalIndex, item.weight)}`}
          >
            {item.keyword}
          </span>
        ))}
      </div>
    </div>
  )
}