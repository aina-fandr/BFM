import { lazy, Suspense, useState } from 'react'
import { Activity, Cuboid, LayoutDashboard, ListChecks, Radio } from 'lucide-react'
import BankDashboard from './BankDashboard'
import type { BagCategory, BankDestination } from './simulation/world'
import './App.css'

const Simulation3D = lazy(() => import('./Simulation3D'))
type View = 'overview' | 'missions' | 'simulation'

function App() {
  const [view, setView] = useState<View>('overview')
  const [destination, setDestination] = useState<BankDestination>('Dépôt 3')
  const [category, setCategory] = useState<BagCategory>('C1')

  return (
    <div className="app-shell bank-app">
      <header className="topbar bank-topbar">
        <a className="brand bank-brand" href="#top" aria-label="Banka, accueil">
          <span className="brand-mark"><Radio size={18} /></span>
          <span className="brand-name">BANKA<span className="brand-dot">.</span></span>
          <span className="brand-divider" />
          <span className="brand-project">AGV <span>BANCAIRE</span></span>
        </a>
        <nav className="view-switch" aria-label="Navigation principale">
          <button type="button" aria-pressed={view === 'overview'} onClick={() => setView('overview')}><LayoutDashboard size={15} /> Supervision</button>
          <button type="button" aria-pressed={view === 'missions'} onClick={() => setView('missions')}><ListChecks size={15} /> Missions</button>
          <button type="button" aria-pressed={view === 'simulation'} onClick={() => setView('simulation')}><Cuboid size={15} /> Simulation 3D</button>
        </nav>
        <div className="topbar-right">
          <span className="prototype-label"><span /> MODE DÉMO</span>
          <span className="bank-user"><Activity size={15} /> Opérations</span>
        </div>
      </header>

      <div hidden={view === 'simulation'}>
        <BankDashboard
          page={view === 'missions' ? 'missions' : 'overview'}
          onOpenSimulation={() => setView('simulation')}
          onDestinationChange={setDestination}
          onCategoryChange={setCategory}
        />
      </div>
      {view === 'simulation' && <Suspense fallback={<div className="sim-loading">Chargement du bâtiment bancaire…</div>}><Simulation3D destination={destination} category={category} onDestinationChange={setDestination} onBack={() => setView('overview')} /></Suspense>}
    </div>
  )
}

export default App
