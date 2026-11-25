import { useCallback, useEffect, useRef, useState } from 'react'
import {
  Activity,
  AlertTriangle,
  BatteryMedium,
  Camera,
  Check,
  CheckCircle2,
  CircleStop,
  Clock3,
  MapPin,
  Navigation as NavigationIcon,
  Pause,
  Play,
  Radio,
  ScanLine,
  RotateCcw,
  ShieldAlert,
  Signal,
  TriangleAlert,
  Wifi,
  WifiOff,
} from 'lucide-react'

type EventLevel = 'info' | 'warning' | 'critical'
type DashboardEvent = { id: number; time: string; message: string; level: EventLevel }

const routePoints = [
  { x: 73, y: 15 },
  { x: 68, y: 26 },
  { x: 54, y: 44 },
  { x: 42, y: 69 },
]

function getRobotPosition(progress: number) {
  const routePosition = Math.min((progress / 100) * (routePoints.length - 1), routePoints.length - 1)
  const segment = Math.min(Math.floor(routePosition), routePoints.length - 2)
  const fraction = routePosition - segment
  const start = routePoints[segment]
  const end = routePoints[segment + 1]

  return {
    x: start.x + (end.x - start.x) * fraction,
    y: start.y + (end.y - start.y) * fraction,
  }
}

const initialEvents: DashboardEvent[] = [
  { id: 1, time: '14:32:08', message: 'Simulation locale du robot prête.', level: 'info' },
  { id: 2, time: '14:31:54', message: 'Scène restaurant chargée dans le navigateur.', level: 'info' },
  { id: 3, time: '14:31:42', message: 'Configuration conceptuelle Sito-É chargée.', level: 'info' },
]

function OwnerDashboard() {
  const [connected, setConnected] = useState(true)
  const [battery, setBattery] = useState(82)
  const [progress, setProgress] = useState(0)
  const [simulationRunning, setSimulationRunning] = useState(false)
  const [stopRequested, setStopRequested] = useState(false)
  const [confirmStop, setConfirmStop] = useState(false)
  const [events, setEvents] = useState(initialEvents)
  const progressRef = useRef(0)

  const addEvent = useCallback((message: string, level: EventLevel = 'info') => {
    const time = new Intl.DateTimeFormat('fr-FR', { hour: '2-digit', minute: '2-digit', second: '2-digit' }).format(new Date())
    setEvents((currentEvents) => [{ id: Date.now(), time, message, level }, ...currentEvents].slice(0, 6))
  }, [])

  useEffect(() => {
    if (!simulationRunning) return
    const timer = window.setInterval(() => {
      const nextProgress = Math.min(progressRef.current + 1, 100)
      progressRef.current = nextProgress
      setProgress(nextProgress)
      if (nextProgress === 100) {
        window.clearInterval(timer)
        setSimulationRunning(false)
        addEvent('Le robot simulé est arrivé à Table B2.')
      }
    }, 300)
    return () => window.clearInterval(timer)
  }, [addEvent, simulationRunning])

  const toggleConnection = () => {
    const nextConnected = !connected
    setConnected(nextConnected)
    if (!nextConnected) setSimulationRunning(false)
    addEvent(nextConnected ? 'Connexion de supervision rétablie (simulation).' : 'Perte de connexion détectée. Nouveaux appels suspendus (simulation).', nextConnected ? 'info' : 'critical')
  }

  const toggleBattery = () => {
    const nextBattery = battery <= 20 ? 82 : 19
    setBattery(nextBattery)
    addEvent(nextBattery <= 20 ? 'Batterie passée sous le seuil de 20 % (simulation).' : 'Batterie réinitialisée à 82 % (simulation).', nextBattery <= 20 ? 'warning' : 'info')
  }

  const requestStop = () => {
    setSimulationRunning(false)
    setStopRequested(true)
    setConfirmStop(false)
    addEvent('Demande d’arrêt contrôlé envoyée (simulation uniquement).', 'warning')
  }

  const resetDemo = () => {
    setConnected(true)
    setBattery(82)
    progressRef.current = 0
    setProgress(0)
    setSimulationRunning(false)
    setStopRequested(false)
    setConfirmStop(false)
    addEvent('Scénarios de démonstration réinitialisés.', 'info')
  }

  const startSimulation = () => {
    if (!connected || stopRequested) return
    if (progress >= 100) {
      progressRef.current = 0
      setProgress(0)
    }
    setSimulationRunning(true)
    addEvent(progress >= 100 ? 'Nouveau trajet simulé démarré.' : 'Trajet local simulé vers Table B2 démarré.')
  }

  const robotState = !connected ? 'Déconnecté' : stopRequested ? 'Arrêt demandé' : simulationRunning ? 'En déplacement' : progress >= 100 ? 'Arrivé' : 'En attente'
  const missionState = !connected ? 'Suspendue · reconnexion requise' : stopRequested ? 'Arrêt contrôlé demandé' : progress >= 100 ? 'Terminée · Table B2' : simulationRunning ? 'Livraison vers Table B2' : 'Prêt · destination Table B2'
  const robotPosition = getRobotPosition(progress)

  return (
    <main className="owner-workspace">
      <section className="owner-page-heading">
        <div>
          <p className="eyebrow"><span className="eyebrow-line" /> ESPACE PROPRIÉTAIRE · PARC</p>
          <h1>Supervision<span>.</span></h1>
          <p className="intro-copy">État du robot, alertes et commandes de contrôle.</p>
        </div>
        <div className="owner-live-badge"><span className={`status-light ${connected ? '' : 'status-light-offline'}`} /><span><strong>{simulationRunning ? 'Simulation en cours' : connected ? 'Simulation en pause' : 'Liaison simulée coupée'}</strong><small>Données locales · navigateur</small></span><Signal size={17} /></div>
      </section>

      <div className="owner-demo-notice" role="note"><ShieldAlert size={17} /><span><strong>Mode démonstration.</strong> Cette vue n’est pas authentifiée et n’envoie aucune commande à ROS 2 ni au robot.</span></div>

      <section className="owner-metrics" aria-label="Résumé du robot">
        <article className="owner-metric"><span className="metric-icon metric-icon-state"><Radio size={17} /></span><div><small>ÉTAT ROBOT</small><strong>{robotState}</strong><span className="metric-caption">CAYTU Sito-É · simulé</span></div></article>
        <article className="owner-metric"><span className={`metric-icon ${connected ? 'metric-icon-state' : 'metric-icon-alert'}`}>{connected ? <Wifi size={17} /> : <WifiOff size={17} />}</span><div><small>CONNEXION</small><strong>{connected ? 'Connecté' : 'Perdue'}</strong><span className="metric-caption">Signal simulé · 1 Hz</span></div></article>
        <article className="owner-metric"><span className={`metric-icon ${battery <= 20 ? 'metric-icon-alert' : 'metric-icon-battery'}`}><BatteryMedium size={18} /></span><div><small>BATTERIE</small><strong>{battery}%</strong><span className="metric-caption">{battery <= 20 ? 'Seuil d’alerte atteint' : 'Niveau normal'}</span></div><div className="battery-track"><span style={{ width: `${battery}%` }} className={battery <= 20 ? 'battery-low' : ''} /></div></article>
        <article className="owner-metric"><span className="metric-icon metric-icon-mission"><Activity size={17} /></span><div><small>MISSION</small><strong>{!connected || stopRequested ? 'En pause' : 'En cours'}</strong><span className="metric-caption">{missionState}</span></div></article>
      </section>

      <section className="owner-sensors-panel" aria-label="Capteurs documentés du robot">
        <div className="owner-panel-heading"><div><p className="eyebrow map-eyebrow">INTERFACES ROS 2 · DOCUMENTATION PARC</p><h2>Capteurs du Sito-É</h2></div><span className="sensor-connection-badge">Non connectés</span></div>
        <div className="sensor-grid">
          <article className="sensor-card"><span className="sensor-icon sensor-icon-lidar"><ScanLine size={17} /></span><div><strong>RPLIDAR C1</strong><small>LiDAR · mesures de distance</small><code>/scan</code></div></article>
          <article className="sensor-card"><span className="sensor-icon sensor-icon-camera"><Camera size={17} /></span><div><strong>D435i supérieure</strong><small>Image couleur · nuage de points 3D</small><code>/top_camera_color/image_raw</code><code>/top_camera_depth/points</code><code>/top_camera_color/image_raw/compressed</code><code>/top_camera_color/image_raw/theora</code></div></article>
          <article className="sensor-card"><span className="sensor-icon sensor-icon-camera"><Camera size={17} /></span><div><strong>D435i inférieure</strong><small>Image couleur · nuage de points 3D</small><code>/bottom_camera_color/image_raw</code><code>/bottom_camera_depth/points</code><code>/bottom_camera_color/image_raw/compressed</code><code>/bottom_camera_color/image_raw/theora</code></div></article>
          <article className="sensor-card"><span className="sensor-icon sensor-icon-imu"><Activity size={17} /></span><div><strong>IMU</strong><small>Mesures inertielles</small><code>/imu</code></div></article>
        </div>
        <p className="sensor-note">Topics repris de la documentation de la compétition. Les valeurs et flux ne sont pas encore lus par l’application.</p>
      </section>

      <div className="owner-main-grid">
        <section className="owner-map-panel" aria-label="Carte de supervision simulée">
          <div className="owner-panel-heading"><div><p className="eyebrow map-eyebrow">POSITION DU ROBOT · SIMULATION</p><h2>Restaurant PARC</h2></div><span className="map-coordinate"><MapPin size={14} /> Zone nord-est</span></div>
          <div className="map-canvas owner-map-canvas">
            <div className="map-wall wall-top" /><div className="map-wall wall-left" /><div className="map-wall wall-right" />
            <div className="map-zone zone-service"><span>COMPTOIR</span><div className="counter-block" /><div className="counter-block counter-block-small" /></div>
            <div className="map-zone zone-entry"><span>ENTRÉE</span></div><div className="map-corridor"><span>ALLÉE CENTRALE</span></div>
            <svg className="owner-route" viewBox="0 0 1000 500" preserveAspectRatio="none" aria-hidden="true"><path d="M730 95 C690 140 565 150 500 220 S435 290 420 355" /></svg>
            <div className="map-robot" style={{ left: `${robotPosition.x}%`, top: `${robotPosition.y}%` }}><Radio size={17} /><span>ROBOT</span></div>
            <div className="map-destination owner-map-destination" style={{ left: '42%', top: '69%' }}><MapPin size={16} fill="currentColor" /><span>TABLE B2</span></div>
            <div className="owner-table owner-table-a1" /><div className="owner-table owner-table-a2" /><div className="owner-table owner-table-a3" /><div className="owner-table owner-table-b1" /><div className="owner-table owner-table-b3" />
            <div className="map-scale"><span /> PLAN SIMPLIFIÉ</div>
          </div>
          <div className="owner-map-footer"><span><i className="legend-robot"><Radio size={10} /></i> Robot</span><span><i className="legend-selected"><MapPin size={10} /></i> Destination actuelle</span><span className="map-updated"><Clock3 size={13} /> Actualisé à l’instant</span></div>
        </section>

        <section className="owner-control-panel" aria-label="Commandes et mission">
          <div className="owner-panel-heading"><div><p className="eyebrow map-eyebrow">CONTRÔLE AUTORISÉ</p><h2>Mission en cours</h2></div><span className={`mission-pill ${!connected ? 'mission-pill-paused' : ''}`}>{connected && !stopRequested ? 'EN COURS' : 'EN PAUSE'}</span></div>
          <div className="mission-destination"><span className="mission-pin"><MapPin size={17} /></span><div><small>DESTINATION</small><strong>Table B2</strong><span>Restaurant · zone service</span></div></div>
          <div className="mission-progress-label"><span>Progression simulée</span><strong>{connected && !stopRequested ? `${progress}%` : '—'}</strong></div>
          <div className="mission-progress"><span style={{ width: connected && !stopRequested ? `${progress}%` : '0%' }} /></div>
          <div className="mission-meta"><span><Clock3 size={14} /> {simulationRunning ? 'Trajet local · 30 s' : progress >= 100 ? 'Arrivé à destination' : 'Prêt à démarrer'}</span><span><NavigationIcon size={14} /> Environnement navigateur</span></div>
          <div className="local-simulation-controls"><span className="local-simulation-label"><Radio size={14} /> SIMULATION LOCALE · 2D</span><button className="button button-primary simulation-toggle" type="button" disabled={!connected || stopRequested} onClick={simulationRunning ? () => { setSimulationRunning(false); addEvent('Trajet simulé mis en pause.') } : startSimulation}>{simulationRunning ? <><Pause size={15} /> Mettre en pause</> : <><Play size={15} /> {progress >= 100 ? 'Rejouer le trajet' : progress > 0 ? 'Reprendre le trajet' : 'Démarrer le trajet'}</>}</button></div>
          <div className="owner-command-area">
            {confirmStop ? <div className="stop-confirmation" role="group" aria-label="Confirmer la demande d’arrêt"><p>Demander un arrêt contrôlé du robot ?</p><div><button className="button button-danger" type="button" onClick={requestStop}><Check size={15} /> Confirmer</button><button className="button button-neutral" type="button" onClick={() => setConfirmStop(false)}>Annuler</button></div></div> : <button className="button button-danger stop-command" type="button" disabled={!connected || stopRequested} onClick={() => setConfirmStop(true)}><CircleStop size={18} /> {stopRequested ? 'Arrêt demandé' : 'Demander l’arrêt contrôlé'}</button>}
            <p><TriangleAlert size={14} /> Demande simulée ; l’état réel du robot n’est pas modifié.</p>
          </div>
        </section>
      </div>

      <div className="owner-bottom-grid">
        <section className="owner-alerts-panel" aria-label="Alertes du robot">
          <div className="owner-panel-heading"><div><p className="eyebrow map-eyebrow">SURVEILLANCE</p><h2>Alertes</h2></div><span className={`alert-count ${!connected || battery <= 20 ? 'alert-count-active' : ''}`}>{Number(!connected) + Number(battery <= 20)}</span></div>
          <div className={`alert-row ${connected ? 'alert-row-ok' : 'alert-row-critical'}`}><span className="alert-symbol">{connected ? <CheckCircle2 size={17} /> : <WifiOff size={17} />}</span><div><strong>{connected ? 'Connexion établie' : 'Perte de connexion'}</strong><small>{connected ? 'Aucun défaut de liaison simulé' : 'Appels suspendus · vérifier la liaison'}</small></div><span className="alert-time">À L’INSTANT</span></div>
          <div className={`alert-row ${battery <= 20 ? 'alert-row-warning' : 'alert-row-ok'}`}><span className="alert-symbol">{battery <= 20 ? <AlertTriangle size={17} /> : <CheckCircle2 size={17} />}</span><div><strong>{battery <= 20 ? 'Batterie faible' : 'Batterie normale'}</strong><small>{battery}% · seuil défini à 20%</small></div><span className="alert-time">À L’INSTANT</span></div>
          <div className="owner-test-controls"><span>SCÉNARIOS DE TEST</span><button type="button" onClick={toggleConnection}>{connected ? <WifiOff size={14} /> : <RotateCcw size={14} />}{connected ? 'Simuler coupure' : 'Rétablir liaison'}</button><button type="button" onClick={toggleBattery}><BatteryMedium size={14} />{battery <= 20 ? 'Restaurer batterie' : 'Simuler 19 %'}</button><button type="button" onClick={resetDemo}><RotateCcw size={14} />Réinitialiser</button></div>
        </section>

        <section className="owner-events-panel" aria-label="Journal des événements">
          <div className="owner-panel-heading"><div><p className="eyebrow map-eyebrow">TRAÇABILITÉ</p><h2>Journal des événements</h2></div><span className="event-count">{events.length} événements</span></div>
          <ol className="event-list">{events.map((event) => <li className={`event-item event-${event.level}`} key={event.id}><span className="event-dot" /><time>{event.time}</time><span className="event-message">{event.message}</span></li>)}</ol>
        </section>
      </div>
      <footer className="page-footer owner-footer"><span>CAYTU ROBOTICS · VUE PROPRIÉTAIRE</span><span><Signal size={13} /> Données de simulation</span></footer>
    </main>
  )
}

export default OwnerDashboard