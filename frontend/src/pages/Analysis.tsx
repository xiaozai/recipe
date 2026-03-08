import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate, useSearchParams } from 'react-router-dom'
import { Search, Loader2, AlertCircle, TrendingUp, TrendingDown, Minus, ExternalLink, ChevronDown, ChevronUp, CheckCircle, Radio, BarChart3, Target, Code } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { analysisApi } from '../services/api'
import { useAnalysisStore } from '../stores/analysisStore'
import { useSettingsStore } from '../stores/settingsStore'
import SourceDistributionChart from '../components/Charts/SourceDistributionChart'
import KeywordCloud from '../components/Charts/KeywordCloud'
import HeatDistributionChart from '../components/Charts/HeatDistributionChart'

// Data sources configuration
const DATA_SOURCES = [
  { id: 'github', label: 'GitHub', description: 'Repositories, issues, discussions' },
  { id: 'hackernews', label: 'Hacker News', description: 'Stories and comments' },
  { id: 'reddit', label: 'Reddit', description: 'Posts and discussions' },
  { id: 'web', label: 'Web', description: 'General web search' },
]

export default function Analysis() {
  const { keyword: urlKeyword } = useParams()
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const { t, defaultSources, defaultLimit } = useSettingsStore()

  const [keyword, setKeyword] = useState(urlKeyword || '')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showFilters, setShowFilters] = useState(false)
  const [selectedSources, setSelectedSources] = useState<string[]>([])
  const [resultLimit, setResultLimit] = useState(defaultLimit)

  // Progress tracking
  const [progress, setProgress] = useState(0)
  const [progressMessage, setProgressMessage] = useState('')
  const [_taskId, setTaskId] = useState<string | null>(null)
  const [collectedItems, setCollectedItems] = useState<any[]>([])
  const [showCollectedItems, setShowCollectedItems] = useState(true)

  const pollingRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const { currentAnalysis, setCurrentAnalysis } = useAnalysisStore()

  // Initialize selected sources from URL params or defaults
  useEffect(() => {
    const sourcesParam = searchParams.get('sources')
    const limitParam = searchParams.get('limit')

    if (sourcesParam) {
      setSelectedSources(sourcesParam.split(','))
    } else {
      setSelectedSources(defaultSources)
    }

    if (limitParam) {
      setResultLimit(Number(limitParam))
    } else {
      setResultLimit(defaultLimit)
    }
  }, [searchParams, defaultSources, defaultLimit])

  // Run analysis when URL keyword changes
  useEffect(() => {
    if (urlKeyword) {
      setKeyword(urlKeyword)
      runAnalysis(urlKeyword)
    }

    // Cleanup polling on unmount
    return () => {
      if (pollingRef.current) {
        clearInterval(pollingRef.current)
      }
    }
  }, [urlKeyword])

  const runAnalysis = async (kw: string) => {
    setLoading(true)
    setError(null)
    setProgress(0)
    setProgressMessage(t.home.steps.dataCollection + '...')
    setCollectedItems([])

    try {
      const sources = selectedSources.length < DATA_SOURCES.length ? selectedSources : undefined

      const startResult = await analysisApi.startAsyncAnalysis(kw, sources, resultLimit)
      const newTaskId = startResult.task_id
      setTaskId(newTaskId)

      pollingRef.current = setInterval(async () => {
        try {
          const status = await analysisApi.getAnalysisStatus(newTaskId)

          setProgress(status.progress || 0)
          setProgressMessage(status.progress_message || '')

          if (status.status === 'completed') {
            if (pollingRef.current) {
              clearInterval(pollingRef.current)
              pollingRef.current = null
            }
            setLoading(false)
            setCurrentAnalysis(status.result)
            setCollectedItems(status.result?.items || [])
          } else if (status.status === 'failed') {
            if (pollingRef.current) {
              clearInterval(pollingRef.current)
              pollingRef.current = null
            }
            setLoading(false)
            setError(status.error || 'Analysis failed')
          }
        } catch (err) {
          console.error('Error polling status:', err)
        }
      }, 1000)

    } catch (err) {
      setLoading(false)
      setError(err instanceof Error ? err.message : 'Analysis failed')
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (keyword.trim()) {
      const params = new URLSearchParams()
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

  // Extract keywords from analysis for the cloud
  const getKeywordsForCloud = () => {
    if (!currentAnalysis) return []
    const keywords: string[] = []

    if (currentAnalysis.analysis?.trends) {
      currentAnalysis.analysis.trends.forEach((trend: any) => {
        if (trend.name) keywords.push(trend.name)
      })
    }

    if (currentAnalysis.analysis?.use_cases) {
      currentAnalysis.analysis.use_cases.forEach((uc: any) => {
        if (uc.name) keywords.push(uc.name)
      })
    }

    if (currentAnalysis.analysis?.opportunities) {
      currentAnalysis.analysis.opportunities.forEach((opp: any) => {
        if (opp.title) keywords.push(opp.title)
      })
    }

    return [...new Set(keywords)].slice(0, 15)
  }

  // Prepare use cases for heat chart
  const getUseCasesForHeatChart = () => {
    if (!currentAnalysis?.analysis?.use_cases) return []
    return currentAnalysis.analysis.use_cases.slice(0, 10).map((uc: any) => ({
      name: uc.name,
      heat_level: (uc.heat_level || 'medium') as 'high' | 'medium' | 'low',
    }))
  }

  return (
    <div className="space-y-6">
      {/* Search Bar */}
      <div className="card">
        <form onSubmit={handleSubmit} className="space-y-3">
          <div className="flex gap-2">
            <input
              type="text"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              placeholder={t.analysis.searchPlaceholder}
              className="input flex-1"
              disabled={loading}
            />
            <button type="submit" className="btn-primary flex items-center gap-2" disabled={loading}>
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Search className="h-4 w-4" />
              )}
              {loading ? t.common.analyzing : t.common.analyze}
            </button>
          </div>

          {/* Filter Toggle */}
          <button
            type="button"
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700"
          >
            {t.analysis.filters}
            {showFilters ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
          </button>

          {/* Filter Options */}
          {showFilters && (
            <div className="p-4 bg-gray-50 rounded-lg">
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
      </div>

      {/* Error */}
      {error && (
        <div className="card bg-red-50 border border-red-200">
          <div className="flex items-center gap-2 text-red-700">
            <AlertCircle className="h-5 w-5" />
            <p>{error}</p>
          </div>
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="card">
          <div className="text-center py-8">
            <Loader2 className="h-12 w-12 animate-spin text-primary-600 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              {t.common.analyzing} "{keyword}"
            </h3>
            <p className="text-gray-600 mb-4">{progressMessage}</p>

            <div className="max-w-md mx-auto">
              <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-primary-600 rounded-full transition-all duration-300"
                  style={{ width: `${progress}%` }}
                />
              </div>
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>{progress}%</span>
                <span>{t.home.steps.dataCollection}</span>
              </div>
            </div>

            {collectedItems.length > 0 && (
              <div className="mt-6">
                <button
                  onClick={() => setShowCollectedItems(!showCollectedItems)}
                  className="text-sm text-primary-600 hover:text-primary-700 flex items-center gap-1 mx-auto"
                >
                  <Radio className="h-4 w-4" />
                  {t.analysis.collectedResources} ({collectedItems.length})
                  {showCollectedItems ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                </button>

                {showCollectedItems && (
                  <div className="mt-4 max-h-60 overflow-y-auto text-left bg-gray-50 rounded-lg p-4">
                    <div className="space-y-2">
                      {collectedItems.map((item, i) => (
                        <div key={i} className="flex items-center gap-2 text-sm">
                          <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0" />
                          <span className="text-gray-700 truncate">{item.title}</span>
                          <span className="text-xs text-gray-400 flex-shrink-0">({item.source_type})</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Results */}
      {!loading && currentAnalysis && (
        <div className="space-y-6">
          {/* Overview Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="card text-center">
              <BarChart3 className="h-8 w-8 text-primary-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-900">{currentAnalysis.items?.length || 0}</div>
              <div className="text-sm text-gray-600">{t.projectAnalysis.totalProjects}</div>
            </div>
            <div className="card text-center">
              <Target className="h-8 w-8 text-primary-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-900">{currentAnalysis.analysis?.key_insights?.length || 0}</div>
              <div className="text-sm text-gray-600">{t.analysis.keyInsights}</div>
            </div>
            <div className="card text-center">
              <TrendingUp className="h-8 w-8 text-primary-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-900">{currentAnalysis.analysis?.trends?.length || 0}</div>
              <div className="text-sm text-gray-600">{t.analysis.trends}</div>
            </div>
            <div className="card text-center">
              <Code className="h-8 w-8 text-primary-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-900">{currentAnalysis.analysis?.use_cases?.length || 0}</div>
              <div className="text-sm text-gray-600">{t.analysis.popularUseCases}</div>
            </div>
          </div>

          {/* Charts Section */}
          <div className="grid md:grid-cols-2 gap-6">
            {currentAnalysis.source_counts && Object.keys(currentAnalysis.source_counts).length > 0 && (
              <div className="card">
                <SourceDistributionChart sourceCounts={currentAnalysis.source_counts} />
              </div>
            )}
            <div className="card">
              <KeywordCloud keywords={getKeywordsForCloud()} />
            </div>
          </div>

          {getUseCasesForHeatChart().length > 0 && (
            <div className="card">
              <HeatDistributionChart useCases={getUseCasesForHeatChart()} />
            </div>
          )}

          {/* Summary */}
          <div className="card">
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              {t.analysis.analysisResults} "{currentAnalysis.keyword}"
            </h2>
            <div className="prose max-w-none">
              <ReactMarkdown>{currentAnalysis.analysis?.summary || ''}</ReactMarkdown>
            </div>
            <div className="mt-4 flex gap-4 text-sm text-gray-600">
              <span>📊 {currentAnalysis.analysis?.content_count || currentAnalysis.items?.length || 0} {t.analysis.itemsAnalyzed}</span>
              {currentAnalysis.metadata?.timings && (
                <span>⏱️ {currentAnalysis.metadata.timings.total_seconds?.toFixed(1)}s</span>
              )}
            </div>
          </div>

          {/* Key Insights */}
          {currentAnalysis.analysis?.key_insights?.length > 0 && (
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">{t.analysis.keyInsights}</h3>
              <ul className="space-y-2">
                {currentAnalysis.analysis.key_insights.map((insight: string, i: number) => (
                  <li key={i} className="flex items-start gap-2">
                    <span className="h-6 w-6 bg-primary-100 text-primary-700 rounded-full flex items-center justify-center text-sm font-medium flex-shrink-0">
                      {i + 1}
                    </span>
                    <span className="text-gray-700">{insight}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Use Cases */}
          {currentAnalysis.analysis?.use_cases?.length > 0 && (
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">{t.analysis.popularUseCases}</h3>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead>
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t.analysis.useCase}</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t.analysis.description}</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">{t.analysis.heat}</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {currentAnalysis.analysis.use_cases.map((uc: any, i: number) => (
                      <tr key={i}>
                        <td className="px-4 py-3 text-sm font-medium text-gray-900">{uc.name}</td>
                        <td className="px-4 py-3 text-sm text-gray-600">{uc.description}</td>
                        <td className="px-4 py-3">
                          <span className={`px-2 py-1 text-xs rounded-full ${
                            uc.heat_level === 'high' ? 'bg-red-100 text-red-700' :
                            uc.heat_level === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                            'bg-gray-100 text-gray-700'
                          }`}>
                            {uc.heat_level}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Trends */}
          {currentAnalysis.analysis?.trends?.length > 0 && (
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">{t.analysis.trends}</h3>
              <div className="grid md:grid-cols-2 gap-4">
                {currentAnalysis.analysis.trends.map((trend: any, i: number) => (
                  <div key={i} className="border rounded-lg p-4">
                    <div className="flex items-center gap-2 mb-2">
                      {trend.direction === 'rising' && <TrendingUp className="h-5 w-5 text-green-500" />}
                      {trend.direction === 'declining' && <TrendingDown className="h-5 w-5 text-red-500" />}
                      {trend.direction === 'stable' && <Minus className="h-5 w-5 text-gray-500" />}
                      <h4 className="font-medium text-gray-900">{trend.name}</h4>
                    </div>
                    <p className="text-sm text-gray-600">{trend.description}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Opportunities */}
          {currentAnalysis.analysis?.opportunities?.length > 0 && (
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">{t.analysis.opportunities}</h3>
              <div className="space-y-4">
                {currentAnalysis.analysis.opportunities.map((opp: any, i: number) => (
                  <div key={i} className="border-l-4 border-primary-500 pl-4 py-2">
                    <h4 className="font-medium text-gray-900">{opp.title}</h4>
                    <p className="text-sm text-gray-600 mt-1">{opp.description}</p>
                    <div className="flex gap-3 mt-2 text-xs">
                      <span className={`px-2 py-1 rounded ${
                        opp.potential === 'high' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
                      }`}>
                        {t.analysis.potential}: {opp.potential}
                      </span>
                      <span className="px-2 py-1 rounded bg-gray-100 text-gray-700">
                        {t.analysis.difficulty}: {opp.difficulty}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Items */}
          {currentAnalysis.items?.length > 0 && (
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                {t.analysis.collectedResources} ({currentAnalysis.items.length})
              </h3>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {currentAnalysis.items.slice(0, 50).map((item: any, i: number) => (
                  <div key={i} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                    <div className="flex-1 min-w-0">
                      <a
                        href={item.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm font-medium text-primary-600 hover:underline flex items-center gap-1"
                      >
                        {item.title}
                        <ExternalLink className="h-3 w-3" />
                      </a>
                      <p className="text-xs text-gray-500 mt-1 line-clamp-2">
                        {item.content?.slice(0, 150)}...
                      </p>
                      <div className="flex gap-2 mt-1 text-xs text-gray-400">
                        <span className={`px-1.5 py-0.5 rounded ${
                          item.source_type === 'github_repo' ? 'bg-green-100 text-green-700' :
                          item.source_type === 'hackernews' ? 'bg-orange-100 text-orange-700' :
                          item.source_type === 'reddit_post' ? 'bg-red-100 text-red-700' :
                          'bg-blue-100 text-blue-700'
                        }`}>{item.source_type}</span>
                        {item.author && <span>• {item.author}</span>}
                        {item.score && <span>• ⭐ {item.score}</span>}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}