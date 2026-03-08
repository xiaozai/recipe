import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AnalysisState {
  currentAnalysis: any | null
  analysisHistory: any[]
  setCurrentAnalysis: (analysis: any) => void
  addToHistory: (analysis: any) => void
  removeFromHistory: (keyword: string) => void
  clearHistory: () => void
}

export const useAnalysisStore = create<AnalysisState>()(
  persist(
    (set, get) => ({
      currentAnalysis: null,
      analysisHistory: [],

      setCurrentAnalysis: (analysis) => {
        set({ currentAnalysis: analysis })
        // Also add to history
        const history = get().analysisHistory
        const exists = history.find((h: any) => h.keyword === analysis.keyword)
        if (!exists) {
          set({
            analysisHistory: [
              { ...analysis, timestamp: new Date().toISOString() },
              ...history.slice(0, 9), // Keep last 10
            ],
          })
        }
      },

      addToHistory: (analysis) => {
        const history = get().analysisHistory
        set({
          analysisHistory: [
            { ...analysis, timestamp: new Date().toISOString() },
            ...history.filter((h: any) => h.keyword !== analysis.keyword).slice(0, 9),
          ],
        })
      },

      removeFromHistory: (keyword) => {
        set({
          analysisHistory: get().analysisHistory.filter((h: any) => h.keyword !== keyword),
        })
      },

      clearHistory: () => {
        set({ analysisHistory: [] })
      },
    }),
    {
      name: 'analysis-storage',
      partialize: (state) => ({
        analysisHistory: state.analysisHistory,
      }),
    }
  )
)