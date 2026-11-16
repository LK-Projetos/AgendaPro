import { useState } from 'react'
import { ToastProvider } from './components'
import Appointments from './pages/Appointments'
import Clients from './pages/Clients'
import Dashboard from './pages/Dashboard'
import Services from './pages/Services'

const TABS = [
  ['dashboard', 'Dashboard'],
  ['appointments', 'Agendamentos'],
  ['clients', 'Clientes'],
  ['services', 'Serviços'],
] as const
type Tab = (typeof TABS)[number][0]

const initial = (): Tab => {
  const h = window.location.hash.slice(1)
  return TABS.some(([k]) => k === h) ? (h as Tab) : 'dashboard'
}

export default function App() {
  const [tab, setTab] = useState<Tab>(initial)
  const go = (t: Tab) => {
    window.location.hash = t
    setTab(t)
  }
  return (
    <ToastProvider>
      <header className="topbar">
        <span className="brand">AgendaPro</span>
        <nav aria-label="Principal">
          {TABS.map(([k, label]) => (
            <button key={k} className={tab === k ? 'active' : ''} onClick={() => go(k)} aria-current={tab === k ? 'page' : undefined}>
              {label}
            </button>
          ))}
        </nav>
      </header>
      <main>
        {/* key força recarregar os dados ao trocar de aba */}
        {tab === 'dashboard' && <Dashboard key="d" />}
        {tab === 'appointments' && <Appointments key="a" />}
        {tab === 'clients' && <Clients key="c" />}
        {tab === 'services' && <Services key="s" />}
      </main>
      <footer className="foot muted">Ambiente acadêmico de demonstração · dados fictícios</footer>
    </ToastProvider>
  )
}
