import { Translations } from './index'

export const en: Translations = {
  // Common
  common: {
    search: 'Search',
    analyze: 'Analyze',
    analyzing: 'Analyzing...',
    loading: 'Loading',
    save: 'Save',
    cancel: 'Cancel',
    delete: 'Delete',
    clear: 'Clear',
    download: 'Download',
    settings: 'Settings',
    home: 'Home',
    reports: 'Reports',
    analysis: 'Analysis',
  },
  // Navigation
  nav: {
    home: 'Home',
    analysis: 'Analysis',
    reports: 'Reports',
    settings: 'Settings',
  },
  // Home page
  home: {
    title: 'Analyze Technology Trends',
    subtitle: 'Search and analyze how technologies are being used across GitHub, Hacker News, Reddit, and more. Get AI-powered insights and recommendations.',
    searchPlaceholder: 'Enter a technology or keyword...',
    popularSearches: 'Popular searches:',
    features: {
      trendAnalysis: {
        title: 'Trend Analysis',
        description: 'Discover emerging trends and patterns across multiple platforms',
      },
      useCaseDiscovery: {
        title: 'Use Case Discovery',
        description: 'Learn how others are using technologies you are interested in',
      },
      opportunityIdentification: {
        title: 'Opportunity Identification',
        description: 'Find untapped opportunities and blue ocean areas',
      },
    },
    howItWorks: 'How It Works',
    steps: {
      enterKeyword: 'Enter Keyword',
      dataCollection: 'Data Collection',
      aiAnalysis: 'AI Analysis',
      getReport: 'Get Report',
    },
  },
  // Analysis page
  analysis: {
    searchPlaceholder: 'Enter a technology or keyword...',
    analysisResults: 'Analysis Results',
    itemsAnalyzed: 'items analyzed',
    keyInsights: 'Key Insights',
    popularUseCases: 'Popular Use Cases',
    trends: 'Trends',
    opportunities: 'Opportunities',
    collectedResources: 'Collected Resources',
    deepAnalysis: 'Deep Project Analysis',
    deepAnalysisDesc: 'Analyze projects to understand what each one does and summarize technology trends',
    analyzeProjects: 'Analyze Projects',
    projectReport: 'Project Analysis Report',
    backToOriginal: 'Back to Original Results',
    filters: 'Filters',
    dataSources: 'Data Sources',
    resultCount: 'Result Count',
    items: 'items',
    heat: 'Heat',
    useCase: 'Use Case',
    description: 'Description',
    confidence: 'Confidence',
    potential: 'Potential',
    difficulty: 'Difficulty',
  },
  // Reports page
  reports: {
    title: 'Reports',
    clearHistory: 'Clear History',
    currentAnalysis: 'CURRENT ANALYSIS',
    history: 'History',
    noReports: 'No Reports Yet',
    noReportsDesc: 'Run an analysis to generate reports. They will appear here.',
  },
  // Settings page
  settings: {
    title: 'Settings',
    llmConfig: 'LLM API Configuration',
    apiKey: 'API Key',
    baseUrl: 'Base URL',
    modelName: 'Model Name',
    apiType: 'API Type',
    searchConfig: 'Search Configuration',
    defaultResultCount: 'Default Result Count',
    defaultSources: 'Default Sources',
    interfaceSettings: 'Interface Settings',
    language: 'Language',
    saved: 'Settings saved',
    saveError: 'Failed to save',
    reset: 'Reset',
    resetConfirm: 'Are you sure you want to reset all settings?',
  },
  // Charts
  charts: {
    sourceDistribution: 'Source Distribution',
    keywordCloud: 'Keyword Cloud',
    heatDistribution: 'Heat Distribution',
  },
  // Project Analysis
  projectAnalysis: {
    totalProjects: 'Total Projects',
    analyzed: 'Analyzed',
    mainThemes: 'Main Themes',
    technologies: 'Technologies',
    commonPatterns: 'Common Patterns',
    emergingTrends: 'Emerging Trends',
    marketSentiment: 'Market Sentiment',
    recommendation: 'Recommendation',
    projectAnalysis: 'Project Analysis',
    sortByRelevance: 'Sort by Relevance',
    sortAlphabetically: 'Sort Alphabetically',
    projectDescription: 'Project Description:',
    keyFeatures: 'Key Features:',
    sentimentPositive: 'Positive',
    sentimentNegative: 'Negative',
    sentimentNeutral: 'Neutral',
  },
  // Footer
  footer: {
    tagline: 'Tech Trend Analyzer - AI-powered technology analysis',
  },
}