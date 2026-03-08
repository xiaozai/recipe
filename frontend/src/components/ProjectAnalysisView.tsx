import { useState } from 'react'
import { TrendingUp, Users, Lightbulb, Target, Code, Zap, BarChart3, ExternalLink, Star } from 'lucide-react'
import { useSettingsStore } from '../stores/settingsStore'
import SourceDistributionChart from './Charts/SourceDistributionChart'
import KeywordCloud from './Charts/KeywordCloud'
import HeatDistributionChart from './Charts/HeatDistributionChart'

interface ProjectAnalysis {
  title: string
  url: string
  source_type: string
  what_it_does: string
  key_features: string[]
  relevance_score: number
}

interface TrendSummary {
  main_themes: string[]
  technology_stack: string[]
  common_patterns: string[]
  emerging_trends: string[]
  market_sentiment: string
  recommendation: string
}

interface ProjectAnalysisResults {
  keyword: string
  total_projects: number
  analyzed_projects: ProjectAnalysis[]
  trend_summary: TrendSummary
  source_counts?: Record<string, number>
}

interface ProjectAnalysisViewProps {
  results: ProjectAnalysisResults
}

export default function ProjectAnalysisView({ results }: ProjectAnalysisViewProps) {
  const { t, language } = useSettingsStore()
  const [sortBy, setSortBy] = useState<'relevance' | 'alphabetical'>('relevance')

  const sortedProjects = [...results.analyzed_projects].sort((a, b) => {
    if (sortBy === 'relevance') {
      return b.relevance_score - a.relevance_score
    }
    return a.title.localeCompare(b.title)
  })

  const getRelevanceColor = (score: number) => {
    if (score >= 80) return 'bg-green-100 text-green-700'
    if (score >= 60) return 'bg-yellow-100 text-yellow-700'
    return 'bg-gray-100 text-gray-700'
  }

  const getSentimentColor = (sentiment: string) => {
    if (sentiment === 'positive') return 'bg-green-100 text-green-700'
    if (sentiment === 'negative') return 'bg-red-100 text-red-700'
    return 'bg-gray-100 text-gray-700'
  }

  const getSentimentLabel = (sentiment: string) => {
    if (sentiment === 'positive') return t.projectAnalysis.sentimentPositive
    if (sentiment === 'negative') return t.projectAnalysis.sentimentNegative
    return t.projectAnalysis.sentimentNeutral
  }

  // Extract all keywords for the cloud
  const allKeywords = [
    ...results.trend_summary.main_themes,
    ...results.trend_summary.technology_stack,
    ...results.trend_summary.emerging_trends.slice(0, 5),
  ]

  // Prepare use cases for heat chart (convert projects to use case format)
  const useCasesForHeatChart = sortedProjects.slice(0, 10).map(project => ({
    name: project.title,
    heat_level: (project.relevance_score >= 80 ? 'high' : project.relevance_score >= 60 ? 'medium' : 'low') as 'high' | 'medium' | 'low',
  }))

  return (
    <div className="space-y-6">
      {/* Overview Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="card text-center">
          <BarChart3 className="h-8 w-8 text-primary-600 mx-auto mb-2" />
          <div className="text-2xl font-bold text-gray-900">{results.total_projects}</div>
          <div className="text-sm text-gray-600">{t.projectAnalysis.totalProjects}</div>
        </div>
        <div className="card text-center">
          <Target className="h-8 w-8 text-primary-600 mx-auto mb-2" />
          <div className="text-2xl font-bold text-gray-900">{results.analyzed_projects.length}</div>
          <div className="text-sm text-gray-600">{t.projectAnalysis.analyzed}</div>
        </div>
        <div className="card text-center">
          <TrendingUp className="h-8 w-8 text-primary-600 mx-auto mb-2" />
          <div className="text-2xl font-bold text-gray-900">{results.trend_summary.main_themes.length}</div>
          <div className="text-sm text-gray-600">{t.projectAnalysis.mainThemes}</div>
        </div>
        <div className="card text-center">
          <Code className="h-8 w-8 text-primary-600 mx-auto mb-2" />
          <div className="text-2xl font-bold text-gray-900">{results.trend_summary.technology_stack.length}</div>
          <div className="text-sm text-gray-600">{t.projectAnalysis.technologies}</div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Source Distribution Chart */}
        {results.source_counts && Object.keys(results.source_counts).length > 0 && (
          <div className="card">
            <SourceDistributionChart sourceCounts={results.source_counts} />
          </div>
        )}

        {/* Keyword Cloud */}
        <div className="card">
          <KeywordCloud keywords={allKeywords} />
        </div>
      </div>

      {/* Heat Distribution Chart */}
      {useCasesForHeatChart.length > 0 && (
        <div className="card">
          <HeatDistributionChart useCases={useCasesForHeatChart} />
        </div>
      )}

      {/* Trend Summary */}
      <div className="card bg-gradient-to-r from-primary-50 to-blue-50">
        <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <TrendingUp className="h-5 w-5" />
          {language === 'zh' ? '技术趋势总结' : 'Technology Trend Summary'}
        </h2>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Main Themes */}
          <div>
            <h3 className="font-semibold text-gray-900 mb-2 flex items-center gap-2">
              <Target className="h-4 w-4" />
              {t.projectAnalysis.mainThemes}
            </h3>
            <div className="flex flex-wrap gap-2">
              {results.trend_summary.main_themes.map((theme: string, i: number) => (
                <span key={i} className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm">
                  {theme}
                </span>
              ))}
            </div>
          </div>

          {/* Technology Stack */}
          <div>
            <h3 className="font-semibold text-gray-900 mb-2 flex items-center gap-2">
              <Code className="h-4 w-4" />
              {t.projectAnalysis.technologies}
            </h3>
            <div className="flex flex-wrap gap-2">
              {results.trend_summary.technology_stack.map((tech: string, i: number) => (
                <span key={i} className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">
                  {tech}
                </span>
              ))}
            </div>
          </div>

          {/* Common Patterns */}
          <div>
            <h3 className="font-semibold text-gray-900 mb-2 flex items-center gap-2">
              <Users className="h-4 w-4" />
              {t.projectAnalysis.commonPatterns}
            </h3>
            <ul className="space-y-1">
              {results.trend_summary.common_patterns.map((pattern: string, i: number) => (
                <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                  <span className="text-primary-500 mt-1">•</span>
                  {pattern}
                </li>
              ))}
            </ul>
          </div>

          {/* Emerging Trends */}
          <div>
            <h3 className="font-semibold text-gray-900 mb-2 flex items-center gap-2">
              <Zap className="h-4 w-4" />
              {t.projectAnalysis.emergingTrends}
            </h3>
            <ul className="space-y-1">
              {results.trend_summary.emerging_trends.map((trend: string, i: number) => (
                <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                  <span className="text-orange-500 mt-1">⚡</span>
                  {trend}
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Market Sentiment & Recommendation */}
        <div className="mt-6 pt-6 border-t border-primary-200">
          <div className="flex items-center gap-3 mb-3">
            <span className="text-sm font-medium text-gray-700">{t.projectAnalysis.marketSentiment}:</span>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getSentimentColor(results.trend_summary.market_sentiment)}`}>
              {getSentimentLabel(results.trend_summary.market_sentiment)}
            </span>
          </div>
          <div>
            <h4 className="font-semibold text-gray-900 mb-1">{t.projectAnalysis.recommendation}:</h4>
            <p className="text-sm text-gray-700">{results.trend_summary.recommendation}</p>
          </div>
        </div>
      </div>

      {/* Projects List */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
            <Lightbulb className="h-5 w-5" />
            {t.projectAnalysis.projectAnalysis}
          </h2>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as 'relevance' | 'alphabetical')}
            className="px-3 py-1 border rounded-lg text-sm"
          >
            <option value="relevance">{t.projectAnalysis.sortByRelevance}</option>
            <option value="alphabetical">{t.projectAnalysis.sortAlphabetically}</option>
          </select>
        </div>

        <div className="space-y-4 max-h-[600px] overflow-y-auto">
          {sortedProjects.map((project: ProjectAnalysis, index: number) => (
            <div
              key={index}
              className="border rounded-lg p-4 hover:border-primary-300 transition-colors"
            >
              <div className="flex items-start justify-between gap-4 mb-3">
                <div className="flex-1 min-w-0">
                  <a
                    href={project.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-lg font-semibold text-primary-600 hover:underline flex items-center gap-2"
                  >
                    {project.title}
                    <ExternalLink className="h-4 w-4" />
                  </a>
                  <div className="flex items-center gap-2 mt-1 text-sm text-gray-500">
                    <span className="px-2 py-0.5 bg-gray-100 rounded text-xs">{project.source_type}</span>
                  </div>
                </div>
                <div className="flex-shrink-0">
                  <div className={`px-3 py-1 rounded-full text-sm font-medium ${getRelevanceColor(project.relevance_score)}`}>
                    <Star className="h-3 w-3 inline mr-1" />
                    {project.relevance_score}
                  </div>
                </div>
              </div>

              <div className="mb-3">
                <h4 className="text-sm font-medium text-gray-700 mb-1">{t.projectAnalysis.projectDescription}</h4>
                <p className="text-sm text-gray-600">{project.what_it_does}</p>
              </div>

              {project.key_features && project.key_features.length > 0 && (
                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-1">{t.projectAnalysis.keyFeatures}</h4>
                  <div className="flex flex-wrap gap-2">
                    {project.key_features.map((feature: string, i: number) => (
                      <span
                        key={i}
                        className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs"
                      >
                        {feature}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}