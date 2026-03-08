import { FileText, Download, Trash2 } from 'lucide-react'
import { useAnalysisStore } from '../stores/analysisStore'
import { useSettingsStore } from '../stores/settingsStore'

export default function Reports() {
  const { t } = useSettingsStore()
  const { analysisHistory, currentAnalysis, clearHistory, removeFromHistory } = useAnalysisStore()

  const downloadReport = (analysis: any) => {
    // Generate markdown report
    const markdown = generateMarkdownReport(analysis, t)
    const blob = new Blob([markdown], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${analysis.keyword}-analysis.md`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">{t.reports.title}</h2>
        {analysisHistory.length > 0 && (
          <button
            onClick={clearHistory}
            className="btn-secondary flex items-center gap-2 text-red-600 hover:bg-red-50"
          >
            <Trash2 className="h-4 w-4" />
            {t.reports.clearHistory}
          </button>
        )}
      </div>

      {/* Current Analysis */}
      {currentAnalysis && (
        <div className="card border-2 border-primary-200">
          <div className="flex items-start justify-between">
            <div>
              <span className="text-xs text-primary-600 font-medium">{t.reports.currentAnalysis}</span>
              <h3 className="text-lg font-semibold text-gray-900 mt-1">
                {currentAnalysis.keyword}
              </h3>
              <p className="text-sm text-gray-600 mt-1">
                {currentAnalysis.analysis?.content_count || 0} {t.analysis.itemsAnalyzed}
              </p>
            </div>
            <button
              onClick={() => downloadReport(currentAnalysis)}
              className="btn-primary flex items-center gap-2"
            >
              <Download className="h-4 w-4" />
              {t.common.download}
            </button>
          </div>
        </div>
      )}

      {/* History */}
      {analysisHistory.length > 0 ? (
        <div className="space-y-3">
          <h3 className="text-lg font-semibold text-gray-900">{t.reports.history}</h3>
          {analysisHistory.map((item: any) => (
            <div key={item.keyword} className="card flex items-center justify-between">
              <div className="flex items-center gap-4">
                <FileText className="h-8 w-8 text-gray-400" />
                <div>
                  <h4 className="font-medium text-gray-900">{item.keyword}</h4>
                  <p className="text-sm text-gray-500">
                    {item.analysis?.content_count || 0} {t.analysis.itemsAnalyzed} • {new Date(item.timestamp).toLocaleDateString()}
                  </p>
                </div>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => downloadReport(item)}
                  className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg"
                  title={t.common.download}
                >
                  <Download className="h-4 w-4" />
                </button>
                <button
                  onClick={() => removeFromHistory(item.keyword)}
                  className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                  title={t.common.delete}
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card text-center py-12">
          <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">{t.reports.noReports}</h3>
          <p className="text-gray-600">
            {t.reports.noReportsDesc}
          </p>
        </div>
      )}
    </div>
  )
}

function generateMarkdownReport(analysis: any, _t: any): string {
  const lines = [
    `# ${analysis.keyword} Technology Trend Analysis Report`,
    '',
    `*Generated at: ${new Date().toISOString()}*`,
    '',
    '## Summary',
    '',
    analysis.analysis?.summary || 'No summary available.',
    '',
  ]

  if (analysis.analysis?.key_insights?.length > 0) {
    lines.push('## Key Insights', '')
    analysis.analysis.key_insights.forEach((insight: string, i: number) => {
      lines.push(`${i + 1}. ${insight}`)
    })
    lines.push('')
  }

  if (analysis.analysis?.use_cases?.length > 0) {
    lines.push('## Popular Use Cases', '')
    lines.push('| Use Case | Description | Heat Level |')
    lines.push('|----------|-------------|------------|')
    analysis.analysis.use_cases.forEach((uc: any) => {
      lines.push(`| ${uc.name} | ${uc.description} | ${uc.heat_level} |`)
    })
    lines.push('')
  }

  if (analysis.analysis?.trends?.length > 0) {
    lines.push('## Trends', '')
    analysis.analysis.trends.forEach((trend: any) => {
      lines.push(`### ${trend.name}`)
      lines.push(`- **Direction**: ${trend.direction}`)
      lines.push(`- **Description**: ${trend.description}`)
      lines.push('')
    })
  }

  if (analysis.analysis?.opportunities?.length > 0) {
    lines.push('## Opportunities', '')
    analysis.analysis.opportunities.forEach((opp: any) => {
      lines.push(`### ${opp.title}`)
      lines.push(`- **Potential**: ${opp.potential}`)
      lines.push(`- **Difficulty**: ${opp.difficulty}`)
      lines.push(`- **Description**: ${opp.description}`)
      lines.push('')
    })
  }

  return lines.join('\n')
}