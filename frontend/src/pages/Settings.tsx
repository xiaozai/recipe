import { useState, useEffect } from 'react'
import { Save, RotateCcw, CheckCircle, AlertCircle, Key, Search, Languages } from 'lucide-react'
import { useSettingsStore } from '../stores/settingsStore'

const DATA_SOURCES = [
  { id: 'github', label: 'GitHub' },
  { id: 'hackernews', label: 'Hacker News' },
  { id: 'reddit', label: 'Reddit' },
  { id: 'web', label: 'Web' },
]

export default function Settings() {
  const {
    t,
    language,
    setLanguage,
    defaultSources,
    defaultLimit,
    setDefaultSources,
    setDefaultLimit,
    apiKey,
    baseUrl,
    modelName,
    apiType,
    setApiKey,
    setBaseUrl,
    setModelName,
    setApiType,
    resetToDefaults,
  } = useSettingsStore()

  const [localApiKey, setLocalApiKey] = useState(apiKey)
  const [localBaseUrl, setLocalBaseUrl] = useState(baseUrl)
  const [localModelName, setLocalModelName] = useState(modelName)
  const [localApiType, setLocalApiType] = useState(apiType)
  const [localDefaultSources, setLocalDefaultSources] = useState<string[]>(defaultSources)
  const [localDefaultLimit, setLocalDefaultLimit] = useState(defaultLimit)
  const [saveStatus, setSaveStatus] = useState<'idle' | 'success' | 'error'>('idle')

  useEffect(() => {
    setLocalApiKey(apiKey)
    setLocalBaseUrl(baseUrl)
    setLocalModelName(modelName)
    setLocalApiType(apiType)
    setLocalDefaultSources(defaultSources)
    setLocalDefaultLimit(defaultLimit)
  }, [apiKey, baseUrl, modelName, apiType, defaultSources, defaultLimit])

  const handleSave = async () => {
    try {
      // Update local store
      setApiKey(localApiKey)
      setBaseUrl(localBaseUrl)
      setModelName(localModelName)
      setApiType(localApiType)
      setDefaultSources(localDefaultSources)
      setDefaultLimit(localDefaultLimit)

      // Try to sync with backend
      try {
        const response = await fetch('/api/v1/settings', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            api_key: localApiKey,
            base_url: localBaseUrl,
            model_name: localModelName,
            api_type: localApiType,
            default_sources: localDefaultSources,
            default_limit: localDefaultLimit,
          }),
        })

        if (response.ok) {
          setSaveStatus('success')
        } else {
          // Still show success since local settings are saved
          setSaveStatus('success')
        }
      } catch {
        // Backend not available, but local settings are saved
        setSaveStatus('success')
      }

      setTimeout(() => setSaveStatus('idle'), 3000)
    } catch {
      setSaveStatus('error')
      setTimeout(() => setSaveStatus('idle'), 3000)
    }
  }

  const handleReset = () => {
    if (window.confirm(t.settings.resetConfirm)) {
      resetToDefaults()
      setLocalApiKey('')
      setLocalBaseUrl('')
      setLocalModelName('claude-sonnet-4-6')
      setLocalApiType('anthropic')
      setLocalDefaultSources(['github', 'hackernews', 'web'])
      setLocalDefaultLimit(50)
    }
  }

  const toggleSource = (sourceId: string) => {
    setLocalDefaultSources(prev =>
      prev.includes(sourceId)
        ? prev.filter(s => s !== sourceId)
        : [...prev, sourceId]
    )
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">{t.settings.title}</h2>
        {saveStatus === 'success' && (
          <div className="flex items-center gap-2 text-green-600">
            <CheckCircle className="h-5 w-5" />
            <span className="text-sm">{t.settings.saved}</span>
          </div>
        )}
        {saveStatus === 'error' && (
          <div className="flex items-center gap-2 text-red-600">
            <AlertCircle className="h-5 w-5" />
            <span className="text-sm">{t.settings.saveError}</span>
          </div>
        )}
      </div>

      {/* LLM API Configuration */}
      <div className="card">
        <div className="flex items-center gap-2 mb-4">
          <Key className="h-5 w-5 text-primary-600" />
          <h3 className="text-lg font-semibold text-gray-900">{t.settings.llmConfig}</h3>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {t.settings.apiType}
            </label>
            <select
              value={localApiType}
              onChange={(e) => setLocalApiType(e.target.value as 'anthropic' | 'openai')}
              className="input"
            >
              <option value="anthropic">Anthropic</option>
              <option value="openai">OpenAI Compatible</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {t.settings.apiKey}
            </label>
            <input
              type="password"
              value={localApiKey}
              onChange={(e) => setLocalApiKey(e.target.value)}
              className="input"
              placeholder={localApiType === 'anthropic' ? 'sk-ant-...' : 'sk-...'}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {t.settings.baseUrl}
            </label>
            <input
              type="text"
              value={localBaseUrl}
              onChange={(e) => setLocalBaseUrl(e.target.value)}
              className="input"
              placeholder={localApiType === 'anthropic' ? 'https://api.anthropic.com' : 'https://api.openai.com/v1'}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {t.settings.modelName}
            </label>
            <input
              type="text"
              value={localModelName}
              onChange={(e) => setLocalModelName(e.target.value)}
              className="input"
              placeholder="claude-sonnet-4-6"
            />
          </div>
        </div>
      </div>

      {/* Search Configuration */}
      <div className="card">
        <div className="flex items-center gap-2 mb-4">
          <Search className="h-5 w-5 text-primary-600" />
          <h3 className="text-lg font-semibold text-gray-900">{t.settings.searchConfig}</h3>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {t.settings.defaultSources}
            </label>
            <div className="flex flex-wrap gap-2">
              {DATA_SOURCES.map((source) => (
                <label
                  key={source.id}
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer transition-colors ${
                    localDefaultSources.includes(source.id)
                      ? 'bg-primary-100 text-primary-700 border-primary-300'
                      : 'bg-gray-50 text-gray-600 border-gray-200'
                  } border`}
                >
                  <input
                    type="checkbox"
                    checked={localDefaultSources.includes(source.id)}
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
              {t.settings.defaultResultCount}: {localDefaultLimit}
            </label>
            <input
              type="range"
              min="10"
              max="100"
              step="10"
              value={localDefaultLimit}
              onChange={(e) => setLocalDefaultLimit(Number(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>10</span>
              <span>50</span>
              <span>100</span>
            </div>
          </div>
        </div>
      </div>

      {/* Interface Settings */}
      <div className="card">
        <div className="flex items-center gap-2 mb-4">
          <Languages className="h-5 w-5 text-primary-600" />
          <h3 className="text-lg font-semibold text-gray-900">{t.settings.interfaceSettings}</h3>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {t.settings.language}
          </label>
          <div className="flex gap-2">
            <button
              onClick={() => setLanguage('zh')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                language === 'zh'
                  ? 'bg-primary-100 text-primary-700 border-primary-300'
                  : 'bg-gray-50 text-gray-600 border-gray-200'
              } border`}
            >
              中文
            </button>
            <button
              onClick={() => setLanguage('en')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                language === 'en'
                  ? 'bg-primary-100 text-primary-700 border-primary-300'
                  : 'bg-gray-50 text-gray-600 border-gray-200'
              } border`}
            >
              English
            </button>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-3">
        <button
          onClick={handleSave}
          className="btn-primary flex items-center gap-2"
        >
          <Save className="h-4 w-4" />
          {t.common.save}
        </button>
        <button
          onClick={handleReset}
          className="btn-secondary flex items-center gap-2"
        >
          <RotateCcw className="h-4 w-4" />
          {t.settings.reset}
        </button>
      </div>
    </div>
  )
}