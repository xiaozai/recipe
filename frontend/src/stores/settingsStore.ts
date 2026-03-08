import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { Language, getTranslations, Translations } from '../i18n'

interface SettingsState {
  // Language settings
  language: Language
  setLanguage: (lang: Language) => void
  t: Translations

  // Search filter settings
  defaultSources: string[]
  defaultLimit: number
  setDefaultSources: (sources: string[]) => void
  setDefaultLimit: (limit: number) => void

  // LLM API settings (for settings page sync)
  apiKey: string
  baseUrl: string
  modelName: string
  apiType: 'anthropic' | 'openai'
  setApiKey: (key: string) => void
  setBaseUrl: (url: string) => void
  setModelName: (name: string) => void
  setApiType: (type: 'anthropic' | 'openai') => void

  // Reset to defaults
  resetToDefaults: () => void
}

const defaultSettings = {
  language: 'zh' as Language,
  defaultSources: ['github', 'hackernews', 'web'],
  defaultLimit: 50,
  apiKey: '',
  baseUrl: '',
  modelName: 'claude-sonnet-4-6',
  apiType: 'anthropic' as const,
}

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set, _get) => ({
      ...defaultSettings,
      t: getTranslations(defaultSettings.language),

      setLanguage: (language) => {
        set({ language, t: getTranslations(language) })
      },

      setDefaultSources: (sources) => {
        set({ defaultSources: sources })
      },

      setDefaultLimit: (limit) => {
        set({ defaultLimit: limit })
      },

      setApiKey: (key) => {
        set({ apiKey: key })
      },

      setBaseUrl: (url) => {
        set({ baseUrl: url })
      },

      setModelName: (name) => {
        set({ modelName: name })
      },

      setApiType: (type) => {
        set({ apiType: type })
      },

      resetToDefaults: () => {
        set({
          ...defaultSettings,
          t: getTranslations(defaultSettings.language),
        })
      },
    }),
    {
      name: 'settings-storage',
      partialize: (state) => ({
        language: state.language,
        defaultSources: state.defaultSources,
        defaultLimit: state.defaultLimit,
        apiKey: state.apiKey,
        baseUrl: state.baseUrl,
        modelName: state.modelName,
        apiType: state.apiType,
      }),
      onRehydrateStorage: () => (state) => {
        if (state) {
          // Update translations after rehydration
          state.t = getTranslations(state.language)
        }
      },
    }
  )
)