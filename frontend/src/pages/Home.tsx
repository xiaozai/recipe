import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, TrendingUp, Users, Lightbulb, ChevronDown, ChevronUp } from 'lucide-react'
import { useSettingsStore } from '../stores/settingsStore'

// Data sources configuration
const DATA_SOURCES = [
  { id: 'github', label: 'GitHub', description: 'Repositories, issues, discussions' },
  { id: 'hackernews', label: 'Hacker News', description: 'Stories and comments' },
  { id: 'reddit', label: 'Reddit', description: 'Posts and discussions' },
  { id: 'web', label: 'Web', description: 'General web search' },
]

export default function Home() {
  const { t, defaultSources, defaultLimit } = useSettingsStore()
  const [keyword, setKeyword] = useState('')
  const [showFilters, setShowFilters] = useState(false)
  // Initialize from settings store defaults
  const [selectedSources, setSelectedSources] = useState<string[]>(defaultSources)
  const [resultLimit, setResultLimit] = useState(defaultLimit)
  const navigate = useNavigate()

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (keyword.trim()) {
      const params = new URLSearchParams()
      // Always include sources parameter for clarity
      params.set('sources', selectedSources.join(','))
      params.set('limit', String(resultLimit))
      navigate(`/analysis/${encodeURIComponent(keyword.trim())}?${params}`)
    }
  }

  const toggleSource = (sourceId: string) => {
    setSelectedSources(prev =>
      prev.includes(sourceId)
        ? prev.filter(s => s !== sourceId)
        : [...prev, sourceId]
    )
  }

  const features = [
    {
      icon: TrendingUp,
      title: t.home.features.trendAnalysis.title,
      description: t.home.features.trendAnalysis.description,
    },
    {
      icon: Users,
      title: t.home.features.useCaseDiscovery.title,
      description: t.home.features.useCaseDiscovery.description,
    },
    {
      icon: Lightbulb,
      title: t.home.features.opportunityIdentification.title,
      description: t.home.features.opportunityIdentification.description,
    },
  ]

  const popularKeywords = [
    'claude-code',
    'langchain',
    'llm-agents',
    'vector-database',
    'ai-coding',
  ]

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center py-12">
        <h2 className="text-4xl font-bold text-gray-900 mb-4">
          {t.home.title}
        </h2>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          {t.home.subtitle}
        </p>

        {/* Search Form */}
        <form onSubmit={handleSearch} className="max-w-xl mx-auto">
          <div className="flex gap-2">
            <input
              type="text"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              placeholder={t.home.searchPlaceholder}
              className="input flex-1"
            />
            <button type="submit" className="btn-primary flex items-center gap-2">
              <Search className="h-4 w-4" />
              {t.common.analyze}
            </button>
          </div>

          {/* Filter Toggle */}
          <button
            type="button"
            onClick={() => setShowFilters(!showFilters)}
            className="mt-3 flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700 mx-auto"
          >
            {t.analysis.filters}
            {showFilters ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
          </button>

          {/* Filter Options */}
          {showFilters && (
            <div className="mt-4 p-4 bg-gray-50 rounded-lg text-left">
              {/* Data Sources */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t.analysis.dataSources}
                </label>
                <div className="flex flex-wrap gap-2">
                  {DATA_SOURCES.map((source) => (
                    <label
                      key={source.id}
                      className={`flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer transition-colors ${
                        selectedSources.includes(source.id)
                          ? 'bg-primary-100 text-primary-700 border-primary-300'
                          : 'bg-white text-gray-600 border-gray-200'
                      } border`}
                    >
                      <input
                        type="checkbox"
                        checked={selectedSources.includes(source.id)}
                        onChange={() => toggleSource(source.id)}
                        className="sr-only"
                      />
                      <span className="text-sm font-medium">{source.label}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Result Count */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t.analysis.resultCount}: {resultLimit} {t.analysis.items}
                </label>
                <input
                  type="range"
                  min="10"
                  max="100"
                  step="10"
                  value={resultLimit}
                  onChange={(e) => setResultLimit(Number(e.target.value))}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>10</span>
                  <span>50</span>
                  <span>100</span>
                </div>
              </div>
            </div>
          )}
        </form>

        {/* Quick Start Keywords */}
        <div className="mt-6">
          <p className="text-sm text-gray-500 mb-2">{t.home.popularSearches}</p>
          <div className="flex flex-wrap justify-center gap-2">
            {popularKeywords.map((kw) => (
              <button
                key={kw}
                onClick={() => {
                  // Use current filter settings when clicking popular keywords
                  const params = new URLSearchParams()
                  params.set('sources', selectedSources.join(','))
                  params.set('limit', String(resultLimit))
                  navigate(`/analysis/${kw}?${params}`)
                }}
                className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm hover:bg-gray-200 transition-colors"
              >
                {kw}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="grid md:grid-cols-3 gap-6">
        {features.map((feature) => {
          const Icon = feature.icon
          return (
            <div key={feature.title} className="card">
              <div className="h-12 w-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <Icon className="h-6 w-6 text-primary-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          )
        })}
      </section>

      {/* How it works */}
      <section className="card">
        <h3 className="text-2xl font-bold text-gray-900 mb-6">{t.home.howItWorks}</h3>
        <div className="grid md:grid-cols-4 gap-6">
          {[
            { step: 1, title: t.home.steps.enterKeyword, desc: 'Specify the technology you want to analyze' },
            { step: 2, title: t.home.steps.dataCollection, desc: 'We gather data from multiple sources' },
            { step: 3, title: t.home.steps.aiAnalysis, desc: 'Claude AI analyzes patterns and trends' },
            { step: 4, title: t.home.steps.getReport, desc: 'Receive actionable insights and recommendations' },
          ].map((item) => (
            <div key={item.step} className="text-center">
              <div className="h-10 w-10 bg-primary-600 text-white rounded-full flex items-center justify-center mx-auto mb-3 text-lg font-bold">
                {item.step}
              </div>
              <h4 className="font-semibold text-gray-900 mb-1">{item.title}</h4>
              <p className="text-sm text-gray-600">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}