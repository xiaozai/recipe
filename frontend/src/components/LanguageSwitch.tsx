import { useSettingsStore } from '../stores/settingsStore'
import { Languages } from 'lucide-react'

export default function LanguageSwitch() {
  const { language, setLanguage } = useSettingsStore()

  const toggleLanguage = () => {
    setLanguage(language === 'zh' ? 'en' : 'zh')
  }

  return (
    <button
      onClick={toggleLanguage}
      className="flex items-center gap-2 px-3 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
      title={language === 'zh' ? 'Switch to English' : '切换到中文'}
    >
      <Languages className="h-5 w-5" />
      <span className="text-sm font-medium">{language === 'zh' ? 'EN' : '中文'}</span>
    </button>
  )
}