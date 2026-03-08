export type Language = 'zh' | 'en'

export interface Translations {
  // Common
  common: {
    search: string
    analyze: string
    analyzing: string
    loading: string
    save: string
    cancel: string
    delete: string
    clear: string
    download: string
    settings: string
    home: string
    reports: string
    analysis: string
  }
  // Navigation
  nav: {
    home: string
    analysis: string
    reports: string
    settings: string
  }
  // Home page
  home: {
    title: string
    subtitle: string
    searchPlaceholder: string
    popularSearches: string
    features: {
      trendAnalysis: { title: string; description: string }
      useCaseDiscovery: { title: string; description: string }
      opportunityIdentification: { title: string; description: string }
    }
    howItWorks: string
    steps: {
      enterKeyword: string
      dataCollection: string
      aiAnalysis: string
      getReport: string
    }
  }
  // Analysis page
  analysis: {
    searchPlaceholder: string
    analysisResults: string
    itemsAnalyzed: string
    keyInsights: string
    popularUseCases: string
    trends: string
    opportunities: string
    collectedResources: string
    deepAnalysis: string
    deepAnalysisDesc: string
    analyzeProjects: string
    projectReport: string
    backToOriginal: string
    filters: string
    dataSources: string
    resultCount: string
    items: string
    heat: string
    useCase: string
    description: string
    confidence: string
    potential: string
    difficulty: string
  }
  // Reports page
  reports: {
    title: string
    clearHistory: string
    currentAnalysis: string
    history: string
    noReports: string
    noReportsDesc: string
  }
  // Settings page
  settings: {
    title: string
    llmConfig: string
    apiKey: string
    baseUrl: string
    modelName: string
    apiType: string
    searchConfig: string
    defaultResultCount: string
    defaultSources: string
    interfaceSettings: string
    language: string
    saved: string
    saveError: string
    reset: string
    resetConfirm: string
  }
  // Charts
  charts: {
    sourceDistribution: string
    keywordCloud: string
    heatDistribution: string
  }
  // Project Analysis
  projectAnalysis: {
    totalProjects: string
    analyzed: string
    mainThemes: string
    technologies: string
    commonPatterns: string
    emergingTrends: string
    marketSentiment: string
    recommendation: string
    projectAnalysis: string
    sortByRelevance: string
    sortAlphabetically: string
    projectDescription: string
    keyFeatures: string
    sentimentPositive: string
    sentimentNegative: string
    sentimentNeutral: string
  }
  // Footer
  footer: {
    tagline: string
  }
}

// Import translations
import { zh } from './zh'
import { en } from './en'

const translations: Record<Language, Translations> = {
  zh,
  en,
}

export function getTranslations(lang: Language): Translations {
  return translations[lang]
}

export { translations }