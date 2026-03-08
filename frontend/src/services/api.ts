import axios from 'axios'

const API_BASE = '/api/v1'

export const analysisApi = {
  async analyze(keyword: string, sources?: string[], limit: number = 50) {
    const response = await axios.post(`${API_BASE}/analyze/sync`, {
      keyword,
      sources,
      limit,
    })
    return response.data
  },

  async startAsyncAnalysis(keyword: string, sources?: string[], limit: number = 50) {
    const response = await axios.post(`${API_BASE}/analyze/`, {
      keyword,
      sources,
      limit,
    })
    return response.data // Returns task_id
  },

  async getAnalysisStatus(taskId: string) {
    const response = await axios.get(`${API_BASE}/analyze/status/${taskId}`)
    return response.data
  },

  async quickAnalyze(keyword: string) {
    const response = await axios.post(`${API_BASE}/analyze/quick`, {
      keyword,
    })
    return response.data
  },

  async search(keyword: string, sources?: string, limit = 50) {
    const params = new URLSearchParams()
    if (sources) params.append('sources', sources)
    params.append('limit', String(limit))
    const response = await axios.get(`${API_BASE}/search/${keyword}?${params}`)
    return response.data
  },

  async analyzeProjects(keyword: string, items: any[]) {
    const response = await axios.post(`${API_BASE}/projects/analyze`, {
      keyword,
      items,
    })
    return response.data
  },

  async quickProjectSummary(keyword: string, items: any[]) {
    const response = await axios.post(`${API_BASE}/projects/quick-summary`, {
      keyword,
      items,
    })
    return response.data
  },

  async generateReport(keyword: string, format = 'markdown') {
    const response = await axios.post(`${API_BASE}/report/generate/${keyword}?format=${format}`)
    return response.data
  },
}

export const sourceApi = {
  async listSources() {
    const response = await axios.get(`${API_BASE}/search/sources/list`)
    return response.data
  },

  async getTrending(source: string, timeframe = 'week') {
    const response = await axios.get(`${API_BASE}/search/${source}/trending?timeframe=${timeframe}`)
    return response.data
  },
}

export const settingsApi = {
  async getSettings() {
    const response = await axios.get(`${API_BASE}/settings`)
    return response.data
  },

  async updateSettings(settings: {
    api_key?: string
    base_url?: string
    model_name?: string
    api_type?: 'anthropic' | 'openai'
    default_sources?: string[]
    default_limit?: number
    language?: string
  }) {
    const response = await axios.put(`${API_BASE}/settings`, settings)
    return response.data
  },

  async resetSettings() {
    const response = await axios.post(`${API_BASE}/settings/reset`)
    return response.data
  },
}