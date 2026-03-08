import { Translations } from './index'

export const zh: Translations = {
  // Common
  common: {
    search: '搜索',
    analyze: '分析',
    analyzing: '分析中...',
    loading: '加载中',
    save: '保存',
    cancel: '取消',
    delete: '删除',
    clear: '清除',
    download: '下载',
    settings: '设置',
    home: '首页',
    reports: '报告',
    analysis: '分析',
  },
  // Navigation
  nav: {
    home: '首页',
    analysis: '分析',
    reports: '报告',
    settings: '设置',
  },
  // Home page
  home: {
    title: '分析技术趋势',
    subtitle: '搜索和分析 GitHub、Hacker News、Reddit 等平台上技术的使用情况，获取 AI 驱动的洞察和建议。',
    searchPlaceholder: '输入技术或关键词...',
    popularSearches: '热门搜索:',
    features: {
      trendAnalysis: {
        title: '趋势分析',
        description: '发现多个平台上的新兴趋势和模式',
      },
      useCaseDiscovery: {
        title: '用例发现',
        description: '了解其他人如何使用您感兴趣的技术',
      },
      opportunityIdentification: {
        title: '机会识别',
        description: '发现未开发的机会和蓝海领域',
      },
    },
    howItWorks: '工作原理',
    steps: {
      enterKeyword: '输入关键词',
      dataCollection: '数据收集',
      aiAnalysis: 'AI 分析',
      getReport: '获取报告',
    },
  },
  // Analysis page
  analysis: {
    searchPlaceholder: '输入技术或关键词...',
    analysisResults: '分析结果',
    itemsAnalyzed: '项已分析',
    keyInsights: '关键洞察',
    popularUseCases: '热门用例',
    trends: '趋势',
    opportunities: '机会',
    collectedResources: '收集的资源',
    deepAnalysis: '深度项目分析',
    deepAnalysisDesc: '分析项目，了解每个项目在做什么，总结技术趋势',
    analyzeProjects: '分析项目',
    projectReport: '项目分析报告',
    backToOriginal: '返回原始结果',
    filters: '过滤条件',
    dataSources: '数据来源',
    resultCount: '返回数量',
    items: '条',
    heat: '热度',
    useCase: '用例',
    description: '描述',
    confidence: '置信度',
    potential: '潜力',
    difficulty: '难度',
  },
  // Reports page
  reports: {
    title: '报告',
    clearHistory: '清除历史',
    currentAnalysis: '当前分析',
    history: '历史',
    noReports: '暂无报告',
    noReportsDesc: '运行分析以生成报告。报告将在此处显示。',
  },
  // Settings page
  settings: {
    title: '设置',
    llmConfig: 'LLM API 配置',
    apiKey: 'API 密钥',
    baseUrl: 'API 基础 URL',
    modelName: '模型名称',
    apiType: 'API 类型',
    searchConfig: '搜索配置',
    defaultResultCount: '默认返回数量',
    defaultSources: '默认数据源',
    interfaceSettings: '界面设置',
    language: '语言',
    saved: '设置已保存',
    saveError: '保存失败',
    reset: '重置',
    resetConfirm: '确定要重置所有设置吗？',
  },
  // Charts
  charts: {
    sourceDistribution: '来源分布',
    keywordCloud: '关键词云',
    heatDistribution: '热度分布',
  },
  // Project Analysis
  projectAnalysis: {
    totalProjects: '总项目数',
    analyzed: '已分析',
    mainThemes: '主要主题',
    technologies: '技术栈',
    commonPatterns: '常见模式',
    emergingTrends: '新兴趋势',
    marketSentiment: '市场情绪',
    recommendation: '建议',
    projectAnalysis: '项目分析',
    sortByRelevance: '按相关性排序',
    sortAlphabetically: '按字母顺序',
    projectDescription: '项目说明:',
    keyFeatures: '主要功能:',
    sentimentPositive: '积极',
    sentimentNegative: '消极',
    sentimentNeutral: '中性',
  },
  // Footer
  footer: {
    tagline: '技术趋势分析器 - AI 驱动的技术分析',
  },
}