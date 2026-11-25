import { useEffect, useMemo, useRef, useState } from 'react'
import {
  Activity,
  AlertTriangle,
  ArrowRight,
  BatteryMedium,
  Check,
  CirclePause,
  CirclePlay,
  Clock3,
  Cuboid,
  MapPin,
  PackageCheck,
  Plus,
  Radio,
  RotateCcw,
  ShieldCheck,
  Signal,
  Warehouse,
  Wifi,
  WifiOff,
} from 'lucide-react'
import type { BagCategory, BankDestination } from './simulation/world'
import './BankDashboard.css'

type MissionState = 'En attente' | 'En cours' | 'Terminée' | 'Suspendue'
type Mission = {
  id: string
  category: BagCategory
  destination: BankDestination
  state: MissionState
  createdAt: string
}

const initialMissions: Mission[] = [
  { id: 'AGV-024', category: 'C2', destination: 'Dépôt 3', state: 'En attente', createdAt: '09:42:18' },
  { id: 'AGV-023', category: 'C1', destination: 'Dépôt 3', state: 'En attente', createdAt: '09:39:51' },
  { id: 'AGV-022', category: 'C3', destination: 'Dépôt 1', state: 'Terminée', createdAt: '09:31:06' },
]

function BankDashboard({ page, onOpenSimulation, onDestinationChange, onCategoryChange }: {
  page: 'overview' | 'missions'
  onOpenSimulation: () => void
  onDestinationChange: (destination: BankDestination) => void
  onCategoryChange: (category: BagCategory) => void
}) {
  const [missions, setMissions] = useState(initialMissions)
  const [battery, setBattery] = useState(82)
  const [connected, setConnected] = useState(true)
  const [missionProgress, setMissionProgress] = useState(0)
  const [category, setCategory] = useState<BagCategory>('C1')
  const [destination, setDestination] = useState<BankDestination>('Dépôt 3')
  const [message, setMessage] = useState('Système prêt · les appels de démonstration sont locaux.')
  const progressRef = useRef(0)
  const missionSequence = useRef(25)

  const activeMission = missions.find((mission) => mission.state === 'En cours')
  const queuedMissions = missions.filter((mission) => mission.state === 'En attente')
  const displayMissions = [...missions].sort((first, second) => {
    const priority: Record<MissionState, number> = { 'En cours': 0, 'En attente': 1, Suspendue: 2, Terminée: 3 }
    if (priority[first.state] !== priority[second.state]) return priority[first.state] - priority[second.state]
    if (first.state === 'En attente') return Number(first.id.slice(4)) - Number(second.id.slice(4))
    return second.createdAt.localeCompare(first.createdAt)
  })
  const hasBatteryAlert = battery <= 20
  const statusText = !connected ? 'Déconnecté' : activeMission ? 'En déplacement' : 'En attente'
  const missionRoute = useMemo(() => ['Collecte', 'Virage à droite', 'Passage ouest', 'Ascenseur A', 'Couloir 2', activeMission?.destination ?? 'Dépôt 3', 'Attente'], [activeMission?.destination])

  useEffect(() => {
    if (!activeMission || !connected) return
    const timer = window.setInterval(() => {
      const nextProgress = Math.min(progressRef.current + 2, 100)
      progressRef.current = nextProgress
      setMissionProgress(nextProgress)
      if (nextProgress === 100) {
        window.clearInterval(timer)
        setMissions((current) => current.map((mission) => mission.id === activeMission.id ? { ...mission, state: 'Terminée' } : mission))
        setMessage(`${activeMission.id} est arrivée au ${activeMission.destination}.`)
      }
    }, 450)
    return () => window.clearInterval(timer)
  }, [activeMission, connected])

  const startNextMission = () => {
    if (!connected || hasBatteryAlert || activeMission || queuedMissions.length === 0) return
    const next = queuedMissions[queuedMissions.length - 1]
    onDestinationChange(next.destination)
    onCategoryChange(next.category)
    progressRef.current = 0
    setMissionProgress(0)
    setMissions((current) => current.map((mission) => mission.id === next.id ? { ...mission, state: 'En cours' } : mission))
    setMessage(`${next.id} en route vers le ${next.destination} · ${next.category}.`)
  }

  const pauseMission = () => {
    if (!activeMission) return
    setMissions((current) => current.map((mission) => mission.id === activeMission.id ? { ...mission, state: 'Suspendue' } : mission))
    setMessage(`${activeMission.id} suspendue par l’opérateur.`)
  }

  const resumeMission = (mission: Mission) => {
    if (!connected || hasBatteryAlert) return
    onDestinationChange(mission.destination)
    onCategoryChange(mission.category)
    if (missionProgress >= 100) {
      progressRef.current = 0
      setMissionProgress(0)
    }
    setMissions((current) => current.map((item) => item.id === mission.id ? { ...item, state: 'En cours' } : item))
    setMessage(`${mission.id} reprise par l’opérateur.`)
  }

  const createMission = () => {
    const createdAt = new Intl.DateTimeFormat('fr-FR', { hour: '2-digit', minute: '2-digit', second: '2-digit' }).format(new Date())
    const id = `AGV-${String(missionSequence.current).padStart(3, '0')}`
    missionSequence.current += 1
    onDestinationChange(destination)
    setMissions((current) => [{ id, category, destination, state: 'En attente', createdAt }, ...current])
    setMessage(`Nouvelle mission ${id} ajoutée en fin de file.`)
  }

  const resetDemo = () => {
    setMissions(initialMissions)
    setBattery(82)
    setConnected(true)
    progressRef.current = 0
    setMissionProgress(0)
    setCategory('C1')
    missionSequence.current = 25
    onDestinationChange('Dépôt 3')
    onCategoryChange('C1')
    setMessage('Scénarios de démonstration réinitialisés.')
  }

  const openCurrentMissionSimulation = () => {
    const nextMission = activeMission ?? queuedMissions[queuedMissions.length - 1]
    if (nextMission) {
      onDestinationChange(nextMission.destination)
      onCategoryChange(nextMission.category)
    }
    onOpenSimulation()
  }

  return (
    <main id="top" className="bank-workspace">
      <section className="bank-heading">
        <div>
          <p className="eyebrow"><span className="eyebrow-line" /> EXPLOITATION · AGENCE BANCAIRE</p>
          <h1>{page === 'missions' ? 'Missions de transfert' : 'Supervision AGV'}<span>.</span></h1>
          <p className="intro-copy">Transport interne des sacs · collecte, ascenseur et zones de tri.</p>
        </div>
        <div className="bank-heading-actions">
          <div className="bank-live-badge"><span className={`status-light ${connected ? '' : 'status-light-offline'}`} /><span><strong>{connected ? 'Liaison simulée active' : 'Robot hors ligne'}</strong><small>Dernière mise à jour · à l’instant</small></span><Signal size={17} /></div>
          <button className="bank-button bank-button-primary" type="button" onClick={openCurrentMissionSimulation}><Cuboid size={16} /> Voir la simulation 3D</button>
        </div>
      </section>

      <div className="bank-demo-notice" role="note"><ShieldCheck size={16} /><span><strong>Prototype local.</strong> Aucune commande n’est envoyée à un AGV réel. Les valeurs et missions affichées sont simulées.</span></div>

      {hasBatteryAlert && <div className="bank-alert-banner" role="alert"><AlertTriangle size={18} /><span><strong>Batterie faible · {battery}%.</strong> Les nouvelles missions sont suspendues jusqu’au rétablissement simulé de la batterie.</span></div>}

      <section className="bank-metrics" aria-label="État de l'AGV">
        <article className="bank-metric"><span className="bank-metric-icon"><Radio size={18} /></span><div><small>ÉTAT AGV</small><strong>{statusText}</strong><span>{activeMission ? activeMission.id : 'Unité bancaire · démo'}</span></div></article>
        <article className="bank-metric"><span className={`bank-metric-icon ${hasBatteryAlert ? 'metric-alert' : ''}`}><BatteryMedium size={19} /></span><div><small>BATTERIE</small><strong>{battery}%</strong><span>{hasBatteryAlert ? 'Seuil d’alerte atteint' : 'Niveau nominal simulé'}</span></div><div className="bank-battery-track"><i className={hasBatteryAlert ? 'bank-battery-low' : ''} style={{ width: `${battery}%` }} /></div></article>
        <article className="bank-metric"><span className={`bank-metric-icon ${connected ? '' : 'metric-alert'}`}>{connected ? <Wifi size={18} /> : <WifiOff size={18} />}</span><div><small>CONNEXION</small><strong>{connected ? 'Connecté' : 'Perdue'}</strong><span>Passerelle non connectée</span></div></article>
        <article className="bank-metric"><span className="bank-metric-icon"><PackageCheck size={18} /></span><div><small>FILE D’ATTENTE</small><strong>{queuedMissions.length} mission{queuedMissions.length > 1 ? 's' : ''}</strong><span>Traitement chronologique</span></div></article>
      </section>

      <div className={`bank-content-grid ${page === 'missions' ? 'missions-page' : ''}`}>
        <section className="bank-panel bank-operation-panel">
          <div className="bank-panel-heading">
            <div><p className="eyebrow bank-eyebrow">MISSION EN COURS</p><h2>{activeMission ? `${activeMission.id} · ${activeMission.category}` : 'Prête pour transfert'}</h2></div>
            <span className={`bank-state-pill ${activeMission ? 'state-running' : ''}`}><i /> {activeMission ? 'EN COURS' : 'EN ATTENTE'}</span>
          </div>
          <div className="bank-route-strip" aria-label={`Trajet : ${missionRoute.join(' puis ')}`}>
            {missionRoute.map((stop, index) => <div className="bank-route-stop" key={`${stop}-${index}`}><span className={index < (activeMission ? 3 : 1) ? 'stop-done' : index === 3 && activeMission ? 'stop-current' : ''}>{index < (activeMission ? 3 : 1) ? <Check size={13} /> : index + 1}</span><small>{stop}</small>{index < missionRoute.length - 1 && <i />}</div>)}
          </div>
          <div className="bank-progress-heading"><span>Progression du transfert</span><strong>{activeMission ? `${missionProgress}%` : '—'}</strong></div>
          <div className="bank-progress-track"><i style={{ width: activeMission ? `${missionProgress}%` : '0%' }} /></div>
          <div className="bank-operation-footer"><span><MapPin size={14} /> {activeMission ? `Destination · ${activeMission.destination}` : 'Destination · dépôt prioritaire 3'}</span><span><Clock3 size={14} /> {activeMission ? 'Temps restant estimé · simulé' : 'En attente d’affectation'}</span></div>
          <div className="bank-operator-actions">
            {activeMission
              ? <button className="bank-button bank-button-muted" type="button" onClick={pauseMission}><CirclePause size={16} /> Suspendre la mission</button>
              : <button className="bank-button bank-button-primary" type="button" disabled={!connected || hasBatteryAlert || queuedMissions.length === 0} onClick={startNextMission}><CirclePlay size={16} /> Lancer la prochaine mission</button>}
            <button className="bank-button bank-button-outline" type="button" onClick={() => setBattery((value) => value <= 20 ? 82 : 19)}>{hasBatteryAlert ? <BatteryMedium size={16} /> : <AlertTriangle size={16} />} {hasBatteryAlert ? 'Rétablir batterie (démo)' : 'Tester alerte batterie'}</button>
            <button className="bank-icon-button" type="button" aria-label="Simuler une perte de connexion" title="Simuler une perte de connexion" onClick={() => {
              const nextConnected = !connected
              setConnected(nextConnected)
              if (!nextConnected && activeMission) {
                setMissions((current) => current.map((mission) => mission.id === activeMission.id ? { ...mission, state: 'Suspendue' } : mission))
              }
              setMessage(nextConnected ? 'Connexion de supervision rétablie (simulation).' : 'Perte de connexion simulée · mission suspendue.')
            }}>{connected ? <WifiOff size={16} /> : <Wifi size={16} />}</button>
          </div>
        </section>

        <section className="bank-panel bank-plan-panel">
          <div className="bank-panel-heading"><div><p className="eyebrow bank-eyebrow">PLAN DU SITE</p><h2>Deux niveaux · trajet nominal</h2></div><Warehouse size={19} /></div>
          <div className="bank-site-sketch" aria-label="Schéma simplifié des deux niveaux">
            <div className="site-level site-level-start">
              <strong>NIVEAU DE DÉPART <small>+3 m · hypothèse</small></strong>
              <span className="site-room room-collection">Collecte<small>8 × 6 m · D</small></span>
              <span className="site-room room-a">Pièce A<small>4 × 3 m · D</small></span>
              <span className="site-room room-b">Pièce B<small>2 × 3 m · H</small></span>
              <span className="site-lift">A</span>
              <span className="site-route-line" />
            </div>
            <div className="site-level site-level-ground">
              <strong>REZ-DE-CHAUSSÉE <small>niveau 0 · référence</small></strong>
              <span className="site-room room-depot3">Dépôt 3 · PRIORITAIRE<small>4 × 4 m · H · C1/C2/C3</small></span>
              <span className="site-room room-depot2">Dépôt 2<small>4 × 3 m · H</small></span>
              <span className="site-room room-depot1">Dépôt 1 · REPLI<small>4 × 3 m · H</small></span>
              <span className="site-lift">A</span>
              <span className="site-route-line" />
            </div>
          </div>
          <div className="bank-plan-legend"><span><i className="legend-route" /> Itinéraire nominal</span><span><i className="legend-hypothesis" /> Hypothèse de conception</span><span><i className="legend-lift" /> Ascenseur aligné</span></div>
        </section>

        <section className="bank-panel bank-queue-panel">
          <div className="bank-panel-heading"><div><p className="eyebrow bank-eyebrow">FILE DES TRANSFERTS</p><h2>{page === 'missions' ? 'Gestion des missions' : 'Dernières missions'}</h2></div><button className="bank-link-button" type="button" onClick={openCurrentMissionSimulation}>Simulation <ArrowRight size={14} /></button></div>
          {page === 'missions' && <div className="bank-create-form">
            <label>Catégorie de sacs<select value={category} onChange={(event) => setCategory(event.target.value as BagCategory)}><option>C1</option><option>C2</option><option>C3</option></select></label>
            <label>Destination<select value={destination} onChange={(event) => setDestination(event.target.value as BankDestination)}><option>Dépôt 3</option><option>Dépôt 1</option></select></label>
            <button className="bank-button bank-button-primary" type="button" onClick={createMission}><Plus size={15} /> Créer une mission</button>
          </div>}
          <div className="bank-mission-list">
            {displayMissions.slice(0, page === 'missions' ? 10 : 4).map((mission) => <article className="bank-mission-row" key={mission.id}>
              <span className={`mission-category category-${mission.category.toLowerCase()}`}>{mission.category}</span>
              <div className="bank-mission-details"><strong>{mission.id} <small>· {mission.destination}</small></strong><span>{mission.createdAt} · {mission.state}</span></div>
              {mission.state === 'Suspendue' ? <button className="mission-resume" type="button" disabled={!connected || hasBatteryAlert} onClick={() => resumeMission(mission)} aria-label={`Reprendre ${mission.id}`}><CirclePlay size={16} /></button> : <span className={`mission-state-mark ${mission.state === 'Terminée' ? 'mission-done' : mission.state === 'En cours' ? 'mission-active' : ''}`} title={mission.state}>{mission.state === 'Terminée' ? <Check size={13} /> : mission.state === 'En cours' ? <Activity size={13} /> : <Clock3 size={13} />}</span>}
            </article>)}
          </div>
          <div className="bank-queue-note" role="status"><Activity size={14} /> {message}</div>
        </section>
      </div>

      <section className="bank-assumptions" aria-label="Hypothèses et sécurité">
        <div><ShieldCheck size={16} /><span><strong>Conception préliminaire · plan v0.1.</strong> Cotes « D » issues du descriptif, « H » hypothèses ; à confirmer sur site.</span></div>
        <button type="button" onClick={resetDemo}><RotateCcw size={14} /> Réinitialiser la démo</button>
      </section>
      <footer className="page-footer"><span>AGV BANCAIRE · AVANT-PROJET 2D V0.1</span><span><Signal size={13} /> Démo locale · données simulées</span></footer>
    </main>
  )
}

export default BankDashboard
