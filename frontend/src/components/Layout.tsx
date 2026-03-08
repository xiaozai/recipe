import { ReactNode } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { BarChart3, Home, FileText, Search, Settings } from 'lucide-react'
import { useSettingsStore } from '../stores/settingsStore'
import LanguageSwitch from './LanguageSwitch'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()
  const { t } = useSettingsStore()

  const navItems = [
    { path: '/', label: t.nav.home, icon: Home },
    { path: '/analysis', label: t.nav.analysis, icon: Search },
    { path: '/reports', label: t.nav.reports, icon: FileText },
    { path: '/settings', label: t.nav.settings, icon: Settings },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <Link to="/" className="flex items-center gap-2">
              <BarChart3 className="h-8 w-8 text-primary-600" />
              <h1 className="text-xl font-bold text-gray-900">Tech Trend Analyzer</h1>
            </Link>
            <div className="flex items-center gap-2">
              <nav className="flex gap-1">
                {navItems.map((item) => {
                  const Icon = item.icon
                  const isActive = location.pathname === item.path ||
                    (item.path !== '/' && location.pathname.startsWith(item.path))
                  return (
                    <Link
                      key={item.path}
                      to={item.path}
                      className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                        isActive
                          ? 'bg-primary-100 text-primary-700'
                          : 'text-gray-600 hover:bg-gray-100'
                      }`}
                    >
                      <Icon className="h-4 w-4" />
                      <span className="hidden sm:inline">{item.label}</span>
                    </Link>
                  )
                })}
              </nav>
              <LanguageSwitch />
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-auto">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <p className="text-center text-gray-500 text-sm">
            {t.footer.tagline}
          </p>
        </div>
      </footer>
    </div>
  )
}