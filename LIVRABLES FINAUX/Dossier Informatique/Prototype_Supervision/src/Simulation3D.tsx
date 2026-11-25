import { useEffect, useMemo, useRef, useState } from 'react'
import { Canvas, useFrame, useThree } from '@react-three/fiber'
import {
  Activity,
  AlertTriangle,
  ArrowLeft,
  BatteryMedium,
  Camera,
  Check,
  CirclePause,
  CirclePlay,
  Crosshair,
  Grid2X2,
  MapPin,
  RotateCcw,
  ScanLine,
  ShieldCheck,
  Warehouse,
  Wifi,
} from 'lucide-react'
import * as THREE from 'three'
import {
  CLEAR_TURN,
  DEFAULT_DESTINATION,
  getCurrentStop,
  getDeliveryPoint,
  getDeliveryProgress,
  getRoute,
  getRoutePosition,
  getRouteSamples,
  LIFT,
  PLAN_LABELS,
  PLAN_OBJECTS,
  ROBOT_ENVELOPE,
  ROBOT_TEST_CHASSIS,
  type BagCategory,
  type BankDestination,
} from './simulation/world'
import './Simulation3D.css'

type SimStatus = 'ready' | 'running' | 'paused' | 'unloading' | 'arrived'
type SceneMode = 'orbit' | 'top' | 'bottom'
type CompartmentId = 'S1' | 'S2' | 'S3' | 'S4'

const COMPARTMENTS: { id: CompartmentId; x: number; y: number; position: string }[] = [
  { id: 'S1', x: -0.25, y: 0.8775, position: 'Haut gauche' },
  { id: 'S2', x: 0.25, y: 0.8775, position: 'Haut droit' },
  { id: 'S3', x: -0.25, y: 0.5125, position: 'Bas gauche' },
  { id: 'S4', x: 0.25, y: 0.5125, position: 'Bas droit' },
]

const MECHANISM_STEPS = [
  { title: 'Arrivée et immobilisation', detail: 'Position de dépôt simulée ; traction inhibée et interface d’accostage vérifiée.', durationMs: 1200 },
  { title: 'Mise à hauteur de la réception', detail: 'Le plateau élévateur rejoint la hauteur du compartiment sélectionné.', durationMs: 1800 },
  { title: 'Extraction du tiroir', detail: 'Déverrouillage du seul casier sélectionné puis sortie guidée sur 0,35 m.', durationMs: 2000 },
  { title: 'Transfert horizontal et tri', detail: 'Le sac reste soutenu, rejoint le plateau, descend puis est orienté vers sa zone de catégorie.', durationMs: 3400 },
  { title: 'Rentrée et reverrouillage', detail: 'Le tiroir vide rentre en butée ; le verrou est confirmé avant le prochain déplacement.', durationMs: 1800 },
]

const RECEIVER_BASE_HEIGHT = 0.39
const DRAWER_STROKE = 0.35

function getStationPlatformHeight(step: number, progress: number, compartmentHeight: number) {
  const alignedHeight = compartmentHeight - 0.12
  const t = THREE.MathUtils.clamp(progress, 0, 1)
  if (step === 1) return THREE.MathUtils.lerp(RECEIVER_BASE_HEIGHT, alignedHeight, t)
  if (step === 2) return alignedHeight
  if (step === 3) return THREE.MathUtils.lerp(alignedHeight, RECEIVER_BASE_HEIGHT, THREE.MathUtils.clamp((t - 0.58) / 0.22, 0, 1))
  return RECEIVER_BASE_HEIGHT
}

function RoomLabel({ name, detail, position, width }: { name: string; detail: string; position: [number, number, number]; width: number }) {
  const texture = useMemo(() => {
    const canvas = document.createElement('canvas')
    canvas.width = 640
    canvas.height = 180
    const context = canvas.getContext('2d')
    if (!context) throw new Error('Impossible de créer le libellé 3D.')
    context.fillStyle = 'rgba(255,255,255,0.92)'
    context.fillRect(0, 0, canvas.width, canvas.height)
    context.fillStyle = '#263d31'
    context.font = '700 30px Segoe UI, sans-serif'
    context.textAlign = 'center'
    context.fillText(name, 320, 72, 600)
    context.fillStyle = '#77877a'
    context.font = '24px Segoe UI, sans-serif'
    context.fillText(detail, 320, 125, 600)
    const labelTexture = new THREE.CanvasTexture(canvas)
    labelTexture.colorSpace = THREE.SRGBColorSpace
    return labelTexture
  }, [detail, name])

  useEffect(() => () => texture.dispose(), [texture])

  return <sprite position={position} scale={[width, width * 0.28, 1]}>
    <spriteMaterial map={texture} transparent depthWrite={false} />
  </sprite>
}

function PlanGeometry() {
  const buildings = PLAN_OBJECTS.filter((object) => object.level !== 'ROBOT' && object.kind !== 'route')
  return <group>
    {buildings.map((object) => <mesh
      key={object.name}
      position={[object.center[0], object.center[2], object.center[1]]}
      rotation={[0, -object.yaw, 0]}
      castShadow={object.kind !== 'floor'}
      receiveShadow={object.kind === 'floor'}
    >
      <boxGeometry args={[object.size[0], object.size[2], object.size[1]]} />
      <meshStandardMaterial color={object.color} roughness={object.kind === 'floor' ? 0.9 : 0.72} />
    </mesh>)}
    {PLAN_LABELS.map((label, index) => <RoomLabel
      key={`${label.level}-${label.text}-${index}`}
      name={label.text}
      detail=""
      position={[label.p[0], label.p[2] + 0.08, label.p[1]]}
      width={3}
    />)}
    <TurnClearanceZone position={[-3.12, 0, 4.8]} label="VIRAGE 5" />
    <TurnClearanceZone position={[8.8, 0, 4.8]} label="VIRAGE 6" />
  </group>
}

function TurnClearanceZone({ position, label }: { position: [number, number, number]; label: string }) {
  return <group position={position}>
    <mesh position={[0, 0.035, 0]}>
      <boxGeometry args={[CLEAR_TURN.width, 0.025, CLEAR_TURN.depth]} />
      <meshBasicMaterial color="#87b5a5" transparent opacity={0.18} />
    </mesh>
    <mesh position={[0, 0.055, 0]}>
      <boxGeometry args={[CLEAR_TURN.width, 0.02, CLEAR_TURN.depth]} />
      <meshBasicMaterial color="#4b8f7c" wireframe transparent opacity={0.7} />
    </mesh>
    <RoomLabel name={label} detail="1,80 × 1,80 m · H" position={[0, 0.14, 0]} width={1.7} />
  </group>
}

function RobotModel({ position, yaw, showSensors, selectedCompartment = 'S1', drawerExtension = 0, emptyCompartments = [] }: {
  position: [number, number, number]
  yaw: number
  showSensors: boolean
  selectedCompartment?: CompartmentId
  drawerExtension?: number
  emptyCompartments?: CompartmentId[]
}) {
  const wheelPositions = [
    { x: 0, z: -0.305 },
    { x: 0, z: 0.305 },
    { x: -0.36, z: 0 },
    { x: 0.36, z: 0 },
  ]
  return <group position={position} rotation={[0, yaw, 0]}>
    <mesh position={[0, 0.015, 0]}>
      <boxGeometry args={[ROBOT_ENVELOPE.width, 0.02, ROBOT_ENVELOPE.depth]} />
      <meshBasicMaterial color="#3684a2" wireframe transparent opacity={0.48} />
    </mesh>
    <mesh position={[0, 0.15, 0]} castShadow><boxGeometry args={[1.1, 0.3, 0.7]} /><meshStandardMaterial color="#26332c" metalness={0.22} roughness={0.52} /></mesh>
    <mesh position={[0, 0.335, 0]}><boxGeometry args={[0.38, 0.07, 0.34]} /><meshStandardMaterial color="#586a7b" metalness={0.35} roughness={0.5} /></mesh>
    <mesh position={[0, 0.695, 0.24]} castShadow><boxGeometry args={[1, 0.75, 0.02]} /><meshStandardMaterial color="#26332c" metalness={0.16} roughness={0.55} /></mesh>
    <mesh position={[0, 1.07, 0]} castShadow><boxGeometry args={[1, 0.02, 0.5]} /><meshStandardMaterial color="#26332c" metalness={0.16} roughness={0.55} /></mesh>
    <mesh position={[-0.49, 0.695, 0]} castShadow><boxGeometry args={[0.02, 0.75, 0.5]} /><meshStandardMaterial color="#26332c" metalness={0.16} roughness={0.55} /></mesh>
    <mesh position={[0.49, 0.695, 0]} castShadow><boxGeometry args={[0.02, 0.75, 0.5]} /><meshStandardMaterial color="#26332c" metalness={0.16} roughness={0.55} /></mesh>
    <mesh position={[0, 0.33, 0]}><boxGeometry args={[0.98, 0.02, 0.48]} /><meshStandardMaterial color="#586a7b" metalness={0.28} roughness={0.52} /></mesh>
    <mesh position={[0, 0.695, 0]}><boxGeometry args={[0.98, 0.02, 0.48]} /><meshStandardMaterial color="#586a7b" metalness={0.28} roughness={0.52} /></mesh>
    <mesh position={[0, 0.695, 0]}><boxGeometry args={[0.02, 0.73, 0.48]} /><meshStandardMaterial color="#586a7b" metalness={0.28} roughness={0.52} /></mesh>
    {COMPARTMENTS.map(({ id, x, y }) => {
      const selected = id === selectedCompartment
      const empty = emptyCompartments.includes(id)
      const extension = selected ? drawerExtension : 0
      return <group key={id} position={[x, y, -extension]}>
        <mesh position={[0, -0.14, 0]} castShadow>
          <boxGeometry args={[0.43, 0.018, 0.43]} />
          <meshStandardMaterial color="#566879" metalness={0.32} roughness={0.48} />
        </mesh>
        {[-0.205, 0.205].map((railX) => <mesh key={railX} position={[railX, -0.095, 0.005]}>
          <boxGeometry args={[0.018, 0.075, 0.4]} />
          <meshStandardMaterial color="#8d9ba4" metalness={0.52} roughness={0.4} />
        </mesh>)}
        <mesh position={[0, 0, -0.22]} castShadow>
          <boxGeometry args={[0.46, 0.325, 0.025]} />
          <meshStandardMaterial color={selected ? '#e5f0f3' : '#dce6ec'} metalness={0.28} roughness={0.5} />
        </mesh>
        <mesh position={[0, 0.035, -0.244]}>
          <boxGeometry args={[0.13, 0.025, 0.018]} />
          <meshStandardMaterial color="#586a7b" metalness={0.45} roughness={0.42} />
        </mesh>
        <mesh position={[0.17, 0.04, -0.244]}>
          <boxGeometry args={[0.035, 0.04, 0.018]} />
          <meshStandardMaterial color={selected ? '#31a4e7' : '#72818b'} metalness={0.25} roughness={0.45} />
        </mesh>
        {!empty && <mesh position={[0, -0.045, 0.005]} castShadow scale={[0.72, 0.74, 0.78]}>
          <sphereGeometry args={[0.15, 18, 12]} />
          <meshStandardMaterial color="#89957f" roughness={0.92} />
        </mesh>}
        {!empty && <mesh position={[0, 0.015, -0.13]}>
          <boxGeometry args={[0.07, 0.035, 0.012]} />
          <meshStandardMaterial color="#ece9d8" roughness={0.8} />
        </mesh>}
        <mesh position={[0.235, 0, -0.18]}>
          <boxGeometry args={[0.018, 0.055, 0.025]} />
          <meshStandardMaterial color={selected && drawerExtension > 0.01 ? '#43aa70' : '#a9b5b9'} emissive={selected && drawerExtension > 0.01 ? '#1b5934' : '#000000'} />
        </mesh>
      </group>
    })}
    <mesh position={[0.48, 0.92, 0]}><boxGeometry args={[0.04, 0.18, 0.25]} /><meshStandardMaterial color="#31a4e7" /></mesh>
    <mesh position={[0.43, 1.105, 0.08]}><cylinderGeometry args={[0.035, 0.035, 0.025, 16]} /><meshStandardMaterial color="#cc4f4f" /></mesh>
    {wheelPositions.map(({ x, z }, index) => <mesh key={index} position={[x, 0.11, z]} rotation={[Math.PI / 2, 0, 0]} castShadow><cylinderGeometry args={[0.11, 0.11, 0.09, 16]} /><meshStandardMaterial color="#222923" /></mesh>)}
    <mesh position={[0, 0.34, -0.34]}><boxGeometry args={[0.36, 0.08, 0.04]} /><meshStandardMaterial color="#7dd0ac" emissive="#388b68" emissiveIntensity={0.6} /></mesh>
    <mesh position={[0, 0.57, 0.29]}><boxGeometry args={[0.21, 0.1, 0.04]} /><meshStandardMaterial color="#cde4d5" emissive="#496d54" emissiveIntensity={0.4} /></mesh>
    {showSensors && <>
      <mesh position={[0, 0.34, -0.56]} rotation={[-Math.PI / 2, 0, 0]}><coneGeometry args={[0.42, 1.5, 24, 1, true]} /><meshBasicMaterial color="#5bbf94" transparent opacity={0.11} side={THREE.DoubleSide} depthWrite={false} /></mesh>
      <mesh position={[0, 0.57, -0.36]} rotation={[-Math.PI / 2, 0, 0]}><coneGeometry args={[0.3, 1.2, 24, 1, true]} /><meshBasicMaterial color="#e4aa63" transparent opacity={0.12} side={THREE.DoubleSide} depthWrite={false} /></mesh>
    </>}
  </group>
}

function ReceivingStation({ platformHeight, category, step }: {
  platformHeight: number
  category: BagCategory
  step: number
}) {
  const stationX = 0.9
  const stationZ = -1.38
  const categorySlots: Record<BagCategory, number> = { C1: -0.58, C2: 0, C3: 0.58 }
  const colors: Record<BagCategory, string> = { C1: '#57b88f', C2: '#5c91de', C3: '#ac80ca' }
  return <group>
    <mesh position={[0.4, 0.3, -0.94]} rotation={[0, -0.55, 0]} castShadow>
      <boxGeometry args={[0.58, 0.07, 1.05]} />
      <meshStandardMaterial color="#8998a1" metalness={0.35} roughness={0.52} />
    </mesh>
    {Array.from({ length: 7 }, (_, index) => {
      const rollerOffset = -0.46 + index * 0.15
      return <mesh key={index}
        position={[0.4 + Math.sin(-0.55) * rollerOffset, 0.355, -0.94 + Math.cos(-0.55) * rollerOffset]}
        rotation={[0, 0, Math.PI / 2]}
      >
      <cylinderGeometry args={[0.025, 0.025, 0.48, 10]} />
      <meshStandardMaterial color="#c0cbd0" metalness={0.68} roughness={0.34} />
      </mesh>
    })}
    <group position={[stationX, 0, stationZ]}>
      {[-0.43, 0.43].map((x) => <mesh key={x} position={[x, 0.78, 0]} castShadow>
        <boxGeometry args={[0.07, 1.56, 0.08]} />
        <meshStandardMaterial color="#596d79" metalness={0.5} roughness={0.42} />
      </mesh>)}
      <mesh position={[0, 1.56, 0]}><boxGeometry args={[0.93, 0.07, 0.08]} /><meshStandardMaterial color="#596d79" metalness={0.5} roughness={0.42} /></mesh>
      {[-0.43, 0.43].map((x) => <mesh key={`rail-${x}`} position={[x, 0.78, 0.08]}>
        <boxGeometry args={[0.025, 1.4, 0.025]} />
        <meshStandardMaterial color="#31a4e7" metalness={0.55} roughness={0.36} />
      </mesh>)}
      <mesh position={[0, platformHeight, 0]} castShadow>
        <boxGeometry args={[0.82, 0.08, 0.62]} />
        <meshStandardMaterial color="#8fa3ad" metalness={0.42} roughness={0.42} />
      </mesh>
      {Array.from({ length: 5 }, (_, index) => <mesh key={`platform-roller-${index}`} position={[-0.32 + index * 0.16, platformHeight + 0.055, 0]} rotation={[0, 0, Math.PI / 2]}>
        <cylinderGeometry args={[0.027, 0.027, 0.58, 10]} />
        <meshStandardMaterial color="#d3dde0" metalness={0.72} roughness={0.28} />
      </mesh>)}
      <mesh position={[0, 0.07, 0]}><boxGeometry args={[0.22, 0.14, 0.16]} /><meshStandardMaterial color="#354a55" metalness={0.38} roughness={0.5} /></mesh>
    </group>
    {(['C1', 'C2', 'C3'] as const).map((slot) => {
      const active = category === slot
      return <group key={slot} position={[stationX + categorySlots[slot], 0, -2.18]}>
        <mesh position={[0, 0.35, 0]} castShadow>
          <boxGeometry args={[0.49, 0.12, 0.46]} />
          <meshStandardMaterial color={colors[slot]} metalness={0.12} roughness={0.65} />
        </mesh>
        {[-0.22, 0.22].map((x) => <mesh key={x} position={[x, 0.47, 0]}>
          <boxGeometry args={[0.04, 0.16, 0.46]} />
          <meshStandardMaterial color={colors[slot]} roughness={0.7} transparent opacity={0.86} />
        </mesh>)}
        <mesh position={[0, 0.47, -0.21]}><boxGeometry args={[0.49, 0.16, 0.04]} /><meshStandardMaterial color={colors[slot]} roughness={0.7} transparent opacity={0.86} /></mesh>
        {active && <mesh position={[0, 0.56, 0]}><boxGeometry args={[0.53, 0.025, 0.5]} /><meshBasicMaterial color="#f0bd60" wireframe /></mesh>}
      </group>
    })}
    <mesh position={[stationX, 0.018, stationZ]} rotation={[-Math.PI / 2, 0, 0]}>
      <ringGeometry args={[0.48, 0.52, 24]} />
      <meshBasicMaterial color={step === 0 ? '#85958a' : '#31a4e7'} side={THREE.DoubleSide} />
    </mesh>
  </group>
}

function MechanismCamera() {
  const { camera } = useThree()
  useEffect(() => {
    camera.position.set(3.35, 2.45, -3.65)
    camera.lookAt(0.35, 0.62, -1.12)
  }, [camera])
  return null
}

function MechanismScene({ step, progress, compartment, category, emptyCompartments, deliveredBags }: {
  step: number
  progress: number
  compartment: CompartmentId
  category: BagCategory
  emptyCompartments: CompartmentId[]
  deliveredBags: { compartment: CompartmentId; category: BagCategory }[]
}) {
  const selected = COMPARTMENTS.find((item) => item.id === compartment) ?? COMPARTMENTS[0]
  const t = THREE.MathUtils.clamp(progress, 0, 1)
  const platformHeight = getStationPlatformHeight(step, t, selected.y)
  const drawerExtension = step === 2
    ? DRAWER_STROKE * t
    : step === 3
      ? DRAWER_STROKE * (1 - THREE.MathUtils.clamp((t - 0.58) / 0.42, 0, 1))
      : 0
  const emptyDuringTransfer = emptyCompartments.includes(compartment) || (step === 3 && t > 0.015)
  const movingBag: [number, number, number] | null = step === 3 && t > 0.015 && t < 0.99
    ? t < 0.58
      ? [
          THREE.MathUtils.lerp(selected.x, 0.9, THREE.MathUtils.clamp(t / 0.58, 0, 1)),
          selected.y,
          THREE.MathUtils.lerp(-0.6, -1.38, THREE.MathUtils.clamp(t / 0.58, 0, 1)),
        ]
      : t < 0.8
        ? [0.9, THREE.MathUtils.lerp(selected.y, 0.55, (t - 0.58) / 0.22), -1.38]
        : [
            THREE.MathUtils.lerp(0.9, 0.9 + ({ C1: -0.58, C2: 0, C3: 0.58 }[category]), (t - 0.8) / 0.2),
            0.55,
            THREE.MathUtils.lerp(-1.38, -2.18, (t - 0.8) / 0.2),
          ]
    : null
  const categoryCounts: Record<BagCategory, number> = { C1: 0, C2: 0, C3: 0 }

  return <>
    <color attach="background" args={['#e8eeea']} />
    <hemisphereLight args={['#fffdf5', '#63756b', 1.45]} />
    <directionalLight position={[4, 8, 3]} intensity={2.1} color="#fff4e2" castShadow />
    <ambientLight intensity={0.45} />
    <mesh position={[0.35, -0.055, -1.05]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
      <planeGeometry args={[4.5, 4.3]} />
      <meshStandardMaterial color="#d5ddd7" roughness={0.92} />
    </mesh>
    <gridHelper args={[4.2, 21, '#b8c5bd', '#d2dbd5']} position={[0.35, -0.045, -1.05]} />
    <RobotModel
      position={[0, 0, 0]}
      yaw={0}
      showSensors={false}
      selectedCompartment={compartment}
      drawerExtension={drawerExtension}
      emptyCompartments={emptyDuringTransfer ? [...emptyCompartments, compartment] : emptyCompartments}
    />
    <ReceivingStation platformHeight={platformHeight} category={category} step={step} />
    {movingBag && <mesh position={movingBag} scale={[0.15, 0.12, 0.2]} castShadow>
      <sphereGeometry args={[1, 20, 14]} />
      <meshStandardMaterial color={category === 'C1' ? '#7c9c55' : category === 'C2' ? '#5689a8' : '#b4834d'} roughness={0.94} />
    </mesh>}
    {deliveredBags.map((bag) => {
      const index = categoryCounts[bag.category]
      categoryCounts[bag.category] += 1
      const x = 0.9 + ({ C1: -0.58, C2: 0, C3: 0.58 }[bag.category]) + (index % 2) * 0.12 - 0.06
      const z = -2.18 + Math.floor(index / 2) * 0.13
      const isBeingTransferred = step === 3 && bag.compartment === compartment && t > 0.8
      return !isBeingTransferred && <mesh key={`${bag.compartment}-${bag.category}`} position={[x, 0.55 + Math.floor(index / 2) * 0.18, z]} scale={[0.15, 0.12, 0.2]} castShadow>
        <sphereGeometry args={[1, 20, 14]} />
        <meshStandardMaterial color={bag.category === 'C1' ? '#7c9c55' : bag.category === 'C2' ? '#5689a8' : '#b4834d'} roughness={0.94} />
      </mesh>
    })}
    <MechanismCamera />
  </>
}

function MechanismView({ step, progress, compartment, category, emptyCompartments, deliveredBags }: {
  step: number
  progress: number
  compartment: CompartmentId
  category: BagCategory
  emptyCompartments: CompartmentId[]
  deliveredBags: { compartment: CompartmentId; category: BagCategory }[]
}) {
  return <div className="bank-mechanism-view">
    <Canvas camera={{ position: [3.35, 2.45, -3.65], fov: 43, near: 0.1, far: 30 }} dpr={[1, 1.2]} gl={{ antialias: true, powerPreference: 'low-power' }} shadows>
      <MechanismScene step={step} progress={progress} compartment={compartment} category={category} emptyCompartments={emptyCompartments} deliveredBags={deliveredBags} />
    </Canvas>
    <span className="bank-mechanism-axis-label">VUE DÉTAILLÉE · CASIER {compartment} → ZONE {category}</span>
  </div>
}

function BankWorld({ progress, destination, category, showSensors, mode, unloadingProgress, compartment, emptyCompartments }: {
  progress: number
  destination: BankDestination
  category: BagCategory
  showSensors: boolean
  mode: SceneMode
  unloadingProgress: number | null
  compartment: CompartmentId
  emptyCompartments: CompartmentId[]
}) {
  const robot = getRoutePosition(progress, destination, category)
  const samples = useMemo(() => getRouteSamples(destination, 5, category), [category, destination])
  const routeDots = samples.filter((_, index) => index % 2 === 0)
  const currentStop = getCurrentStop(progress, destination, category)
  const deliveryPoint = getDeliveryPoint(destination, category)
  const selectedCompartment = COMPARTMENTS.find((item) => item.id === compartment) ?? COMPARTMENTS[0]
  const deliveryTarget: [number, number, number] = destination === 'Dépôt 3'
    ? [deliveryPoint?.x ?? 10.85, 0.62, 13.015]
    : [deliveryPoint?.x ?? 12, 0.48, deliveryPoint?.z ?? 4.8]
  const transferProgress = THREE.MathUtils.clamp(unloadingProgress ?? 0, 0, 1)
  const frontX = -Math.sin(robot.yaw)
  const frontZ = -Math.cos(robot.yaw)
  const drawerExit = {
    x: robot.x + Math.cos(robot.yaw) * selectedCompartment.x + frontX * 0.6,
    z: robot.z - Math.sin(robot.yaw) * selectedCompartment.x + frontZ * 0.6,
  }
  const transferHeight = transferProgress < 0.58
    ? robot.y + selectedCompartment.y
    : transferProgress < 0.8
      ? THREE.MathUtils.lerp(robot.y + selectedCompartment.y, deliveryTarget[1], (transferProgress - 0.58) / 0.22)
      : deliveryTarget[1]
  const payloadPosition: [number, number, number] = unloadingProgress === null
    ? deliveryTarget
    : [
        THREE.MathUtils.lerp(drawerExit.x, deliveryTarget[0], transferProgress),
        transferHeight + Math.sin(transferProgress * Math.PI) * 0.08,
        THREE.MathUtils.lerp(drawerExit.z, deliveryTarget[2], transferProgress),
      ]

  return <>
    <color attach="background" args={['#dfe7e1']} />
    <fog attach="fog" args={['#dfe7e1', 25, 48]} />
    <hemisphereLight args={['#fffdf5', '#687b70', 1.4]} />
    <directionalLight position={[8, 18, 8]} intensity={2} color="#fff0d9" />
    <ambientLight intensity={0.45} />
    <PlanGeometry />
    {routeDots.map((point, index) => <mesh key={`route-${index}`} position={[point.x, point.y + 0.1, point.z]}>
      <sphereGeometry args={[0.055, 7, 6]} />
      <meshBasicMaterial color="#2978e6" />
    </mesh>)}
    <mesh position={[deliveryTarget[0], 0.06, deliveryTarget[2]]} rotation={[-Math.PI / 2, 0, 0]}>
      <ringGeometry args={[0.4, 0.48, 32]} />
      <meshBasicMaterial color="#db8250" side={THREE.DoubleSide} />
    </mesh>
    {destination === 'Dépôt 1' && <RoomLabel name="ZONE DE DÉPÔT · H" detail="Réception simulée" position={[deliveryTarget[0], 0.62, deliveryTarget[2]]} width={2.2} />}
    <RobotModel
      position={[robot.x, robot.y, robot.z]}
      yaw={robot.yaw}
      showSensors={showSensors}
      selectedCompartment={compartment}
      emptyCompartments={unloadingProgress !== null && transferProgress > 0.015
        ? [...emptyCompartments, compartment]
        : emptyCompartments}
    />
    {unloadingProgress !== null && <mesh position={payloadPosition} castShadow>
      <capsuleGeometry args={[0.16, 0.2, 5, 8]} />
      <meshStandardMaterial color={category === 'C1' ? '#7c9c55' : category === 'C2' ? '#5689a8' : '#b4834d'} roughness={0.9} />
    </mesh>}
    {mode === 'orbit'
      ? <OrbitCamera />
      : <FollowCamera mode={mode} robot={robot} />}
    <mesh position={[LIFT.x, 0.03, LIFT.z]} rotation={[-Math.PI / 2, 0, 0]}>
      <ringGeometry args={[0.45, 0.52, 24]} />
      <meshBasicMaterial color="#9587bc" side={THREE.DoubleSide} />
    </mesh>
    <RoomMarkerLabel label={currentStop} position={[robot.x, robot.y + 1.35, robot.z]} />
  </>
}

function RoomMarkerLabel({ label, position }: { label: string; position: [number, number, number] }) {
  return <group position={position}>
    <mesh><sphereGeometry args={[0.08, 10, 8]} /><meshBasicMaterial color="#de8751" /></mesh>
    <RoomLabel name={label} detail="POSITION AGV" position={[0, 0.15, 0]} width={1.8} />
  </group>
}

function OrbitCamera() {
  const { camera, gl } = useThree()
  useEffect(() => {
    const target = new THREE.Vector3(3.9, 1.4, 5.5)
    let azimuth = 0.58
    let polar = 0.9
    let distance = 25
    let dragging = false
    let previousX = 0
    let previousY = 0
    const element = gl.domElement
    const update = () => {
      camera.position.set(
        target.x + distance * Math.sin(polar) * Math.sin(azimuth),
        target.y + distance * Math.cos(polar),
        target.z + distance * Math.sin(polar) * Math.cos(azimuth),
      )
      camera.lookAt(target)
    }
    const onDown = (event: PointerEvent) => {
      if (event.button !== 0) return
      dragging = true
      previousX = event.clientX
      previousY = event.clientY
      element.setPointerCapture(event.pointerId)
    }
    const onMove = (event: PointerEvent) => {
      if (!dragging) return
      azimuth -= (event.clientX - previousX) * 0.006
      polar = THREE.MathUtils.clamp(polar + (event.clientY - previousY) * 0.004, 0.2, 1.4)
      previousX = event.clientX
      previousY = event.clientY
      update()
    }
    const onUp = () => { dragging = false }
    const onWheel = (event: WheelEvent) => {
      distance = THREE.MathUtils.clamp(distance + event.deltaY * 0.015, 15, 39)
      update()
      event.preventDefault()
    }
    update()
    element.addEventListener('pointerdown', onDown)
    element.addEventListener('pointermove', onMove)
    element.addEventListener('pointerup', onUp)
    element.addEventListener('pointercancel', onUp)
    element.addEventListener('wheel', onWheel, { passive: false })
    return () => {
      element.removeEventListener('pointerdown', onDown)
      element.removeEventListener('pointermove', onMove)
      element.removeEventListener('pointerup', onUp)
      element.removeEventListener('pointercancel', onUp)
      element.removeEventListener('wheel', onWheel)
    }
  }, [camera, gl])
  return null
}

function FollowCamera({ mode, robot }: { mode: Exclude<SceneMode, 'orbit'>; robot: ReturnType<typeof getRoutePosition> }) {
  const camera = useThree((state) => state.camera)
  useFrame(() => {
    const sensorHeight = mode === 'top' ? 1.88 : 0.72
    const forwardX = -Math.sin(robot.yaw)
    const forwardZ = -Math.cos(robot.yaw)
    const x = robot.x + forwardX * 0.3
    const z = robot.z + forwardZ * 0.3
    camera.position.set(x, robot.y + sensorHeight, z)
    camera.up.set(0, 1, 0)
    camera.lookAt(x + forwardX * 3.2, robot.y + (mode === 'top' ? 0.1 : 0.05), z + forwardZ * 3.2)
  })
  return null
}

function CameraView({ mode, progress, destination, category, unloadingProgress, compartment, emptyCompartments }: {
  mode: 'top' | 'bottom'
  progress: number
  destination: BankDestination
  category: BagCategory
  unloadingProgress: number | null
  compartment: CompartmentId
  emptyCompartments: CompartmentId[]
}) {
  return <div className="bank-camera-card">
    <div className="bank-camera-heading"><span><Camera size={13} /> {mode === 'top' ? 'D435i supérieure' : 'D435i inférieure'}</span><small>POV SYNTHÉTIQUE</small></div>
    <div className="bank-camera-view">
      <Canvas camera={{ position: [0, 3, 2], fov: 78, near: 0.08, far: 45 }} dpr={[1, 1.1]} gl={{ antialias: false, powerPreference: 'low-power' }}>
        <BankWorld progress={progress} destination={destination} category={category} showSensors={false} mode={mode} unloadingProgress={unloadingProgress} compartment={compartment} emptyCompartments={emptyCompartments} />
      </Canvas>
      <span className="bank-feed-label">{mode === 'top' ? '/top_camera_color/image_raw' : '/bottom_camera_color/image_raw'}</span>
    </div>
  </div>
}

function RouteMiniMap({ destination, category, progress }: { destination: BankDestination; category: BagCategory; progress: number }) {
  const route = getRoute(destination, category)
  const projectPoint = (x: number, z: number, floor: 'départ' | 'rdc') => floor === 'départ'
    ? [70 + (x + 6.37) * 11, 20 + (6.15 - z) * 8] as const
    : [70 + (x + 6.37) * 10, 120 + (13.69 - z) * 4.9] as const
  const mapRoute = route.map((point) => projectPoint(point.x, point.z, point.floor))
  const routePosition = Math.min(progress, 100) / 100 * (mapRoute.length - 1)
  const routeIndex = Math.min(Math.floor(routePosition), mapRoute.length - 2)
  const routeFraction = routePosition - routeIndex
  const mapX = mapRoute[routeIndex][0] + (mapRoute[routeIndex + 1][0] - mapRoute[routeIndex][0]) * routeFraction
  const mapY = mapRoute[routeIndex][1] + (mapRoute[routeIndex + 1][1] - mapRoute[routeIndex][1]) * routeFraction
  const routePoints = mapRoute.map(([x, y]) => `${x},${y}`).join(' ')
  const deliveryPoint = getDeliveryPoint(destination, category)
  const destinationPoint = projectPoint(deliveryPoint?.x ?? 12, deliveryPoint?.z ?? 4.8, 'rdc')
  return <svg className="bank-mini-map" viewBox="0 0 286 208" role="img" aria-label="Plan schématique des deux niveaux et du trajet nominal">
    <rect width="286" height="208" rx="5" fill="#f6f7f4" />
    <text x="12" y="14" className="mini-map-title">NIVEAU DE DÉPART · +3 m*</text>
    <rect x="140" y="21" width="88" height="48" rx="2" fill="#e9eee8" stroke="#53645a" />
    <rect x="72" y="52" width="24" height="20" fill="#efeafa" stroke="#9a8dbd" />
    <rect x="72" y="72" width="87" height="15" fill="#eff1ed" stroke="#87948a" />
    <text x="184" y="43" className="mini-map-room-label">COLLECTE</text>
    <text x="184" y="54" className="mini-map-dim">8 × 6 m · D</text>
    <text x="84" y="65" className="mini-map-lift">A</text>
    <line x1="12" y1="100" x2="274" y2="100" stroke="#d8ded7" />
    <text x="12" y="114" className="mini-map-title">REZ-DE-CHAUSSÉE · 0 m</text>
    <rect x="72" y="177" width="22" height="12" fill="#efeafa" stroke="#9a8dbd" />
    <rect x="94" y="159" width="109" height="9" fill="#eff1ed" stroke="#87948a" />
    <rect x="95" y="168" width="15" height="21" fill="#eff1ed" stroke="#87948a" />
    <rect x="203" y="120" width="30" height="51" fill="#f1f3ef" stroke="#829087" />
    <rect x="233" y="120" width="40" height="20" fill="#eef4e8" stroke="#829087" />
    <rect x="233" y="141" width="40" height="14" fill="#f0f2ef" stroke="#829087" />
    <rect x="233" y="156" width="40" height="15" fill="#f8f1e7" stroke="#829087" />
    <text x="83" y="186" className="mini-map-lift">A</text>
    <text x="218" y="148" className="mini-map-room-label">HALL</text>
    <text x="253" y="132" className="mini-map-room-label">DÉPÔT 3</text>
    <text x="253" y="150" className="mini-map-room-label">DÉPÔT 2</text>
    <text x="253" y="166" className="mini-map-room-label">DÉPÔT 1</text>
    <polyline points={routePoints} fill="none" stroke="#2878e6" strokeWidth="2" strokeDasharray="4 2" />
    <circle cx={destinationPoint[0]} cy={destinationPoint[1]} r="4" fill="#d7834d" stroke="#fff" strokeWidth="1.5" />
    <circle cx={mapX} cy={mapY} r="5" fill="#175747" stroke="#fff" strokeWidth="1.5" />
    <text x="218" y="201" className="mini-map-dim">Robot</text>
    <text x="250" y="201" className="mini-map-dim">{route.length} repères</text>
  </svg>
}

function Simulation3D({ onBack, destination, category, onDestinationChange }: {
  onBack: () => void
  destination: BankDestination
  category: BagCategory
  onDestinationChange: (destination: BankDestination) => void
}) {
  const [progress, setProgress] = useState(0)
  const [status, setStatus] = useState<SimStatus>('ready')
  const [speed, setSpeed] = useState(10)
  const [showSensors, setShowSensors] = useState(true)
  const [unloadingProgress, setUnloadingProgress] = useState<number | null>(null)
  const [selectedCompartment, setSelectedCompartment] = useState<CompartmentId>('S1')
  const [mechanismRunning, setMechanismRunning] = useState(false)
  const [mechanismAutomatic, setMechanismAutomatic] = useState(false)
  const [mechanismStep, setMechanismStep] = useState(0)
  const [mechanismProgress, setMechanismProgress] = useState(0)
  const [emptyCompartments, setEmptyCompartments] = useState<CompartmentId[]>([])
  const [deliveredBags, setDeliveredBags] = useState<{ compartment: CompartmentId; category: BagCategory }[]>([])
  const progressRef = useRef(0)
  const position = getRoutePosition(progress, destination, category)
  const route = getRoute(destination, category)
  const steps = route.map((point) => point.label)
  const currentStep = Math.min(Math.floor(progress / 100 * (steps.length - 1)), steps.length - 1)
  const stateText = mechanismRunning && !mechanismAutomatic
    ? 'Cycle mécanique simulé'
    : status === 'running' ? 'En déplacement' : status === 'unloading' ? `Transfert simulé · ${category}` : status === 'arrived' ? 'Scénario terminé' : status === 'paused' ? 'Mission suspendue' : 'Prêt à démarrer'
  const deliveryProgress = getDeliveryProgress(destination, category)

  useEffect(() => {
    if (status !== 'running') return
    const timer = window.setInterval(() => {
      const next = Math.min(progressRef.current + speed / 30, 100)
      if (progressRef.current < deliveryProgress && next >= deliveryProgress) {
        progressRef.current = deliveryProgress
        setProgress(deliveryProgress)
        setUnloadingProgress(0)
        setMechanismStep(0)
        setMechanismProgress(0)
        setMechanismAutomatic(true)
        setMechanismRunning(true)
        setStatus('unloading')
        window.clearInterval(timer)
        return
      }
      progressRef.current = next
      setProgress(next)
      if (next === 100) {
        window.clearInterval(timer)
        setStatus('arrived')
      }
    }, 150)
    return () => window.clearInterval(timer)
  }, [deliveryProgress, speed, status])

  useEffect(() => {
    if (!mechanismRunning) return
    let phaseProgress = 0
    const duration = MECHANISM_STEPS[mechanismStep].durationMs
    const timer = window.setInterval(() => {
      phaseProgress = Math.min(phaseProgress + 50 / duration, 1)
      setMechanismProgress(phaseProgress)
      setUnloadingProgress(mechanismStep === 3 ? phaseProgress : null)
      if (phaseProgress === 1) {
        window.clearInterval(timer)
        if (mechanismStep < MECHANISM_STEPS.length - 1) {
          setMechanismProgress(0)
          setMechanismStep((step) => step + 1)
          return
        }
        setUnloadingProgress(null)
        setMechanismRunning(false)
        setEmptyCompartments((compartments) => compartments.includes(selectedCompartment)
          ? compartments
          : [...compartments, selectedCompartment])
        setDeliveredBags((bags) => [...bags, { compartment: selectedCompartment, category }])
        if (mechanismAutomatic) setStatus(progressRef.current >= 100 ? 'arrived' : 'running')
        setMechanismAutomatic(false)
      }
    }, 50)
    return () => window.clearInterval(timer)
  }, [category, mechanismAutomatic, mechanismRunning, mechanismStep, selectedCompartment])

  const start = () => {
    if (emptyCompartments.includes(selectedCompartment)) return
    if (progressRef.current >= 100) {
      progressRef.current = 0
      setProgress(0)
    }
    setStatus('running')
  }

  const reset = () => {
    progressRef.current = 0
    setProgress(0)
    setUnloadingProgress(null)
    setSelectedCompartment('S1')
    setMechanismRunning(false)
    setMechanismAutomatic(false)
    setMechanismStep(0)
    setMechanismProgress(0)
    setEmptyCompartments([])
    setDeliveredBags([])
    setStatus('ready')
    onDestinationChange(DEFAULT_DESTINATION)
    setSpeed(10)
    setShowSensors(true)
  }

  const selectDestination = (nextDestination: BankDestination) => {
    progressRef.current = 0
    setProgress(0)
    setUnloadingProgress(null)
    setMechanismRunning(false)
    setMechanismAutomatic(false)
    setMechanismStep(0)
    setMechanismProgress(0)
    setStatus('ready')
    onDestinationChange(nextDestination)
  }

  const startMechanismDemo = () => {
    if (mechanismRunning || status === 'running' || status === 'unloading' || emptyCompartments.includes(selectedCompartment)) return
    setMechanismStep(0)
    setMechanismProgress(0)
    setMechanismAutomatic(false)
    setMechanismRunning(true)
  }

  const resetCompartments = () => {
    if (mechanismRunning || status === 'running' || status === 'unloading') return
    setEmptyCompartments([])
    setDeliveredBags([])
  }

  const selectedCompartmentInfo = COMPARTMENTS.find((item) => item.id === selectedCompartment) ?? COMPARTMENTS[0]
  const currentMechanismStep = MECHANISM_STEPS[mechanismStep]

  return <main className="sim3d-page bank-sim-page">
    <header className="sim3d-header bank-sim-header">
      <div className="sim3d-title-group"><button className="sim-back-button" type="button" onClick={onBack} aria-label="Retour à la supervision"><ArrowLeft size={17} /></button><div><p className="eyebrow">SIMULATEUR LOCAL · BFM V2</p><h1>Transfert mécanique des sacs<span>.</span></h1></div></div>
      <div className="sim3d-live"><span className={`sim-status-dot ${status === 'running' || status === 'unloading' ? 'sim-status-running' : status === 'arrived' ? 'sim-status-arrived' : ''}`} /><span>{stateText}</span><small>Simulation navigateur</small></div>
    </header>

    <div className="sim3d-disclaimer bank-sim-disclaimer"><AlertTriangle size={15} /><span><strong>Cycle automatique illustratif — non validé pour un équipement réel.</strong> L’animation montre l’architecture proposée : tiroir motorisé, transfert guidé et station élévatrice. Actionneurs, charges, dimensions des sacs, synchronisation, anti-pincement et sécurités restent à calculer et tester. Les volumes du bâtiment et les dégagements sont aussi provisoires.</span></div>

    <section className="bank-sim-toolbar" aria-label="Commandes de simulation">
      <div className="sim3d-transport">
        {mechanismRunning && !mechanismAutomatic
          ? <span className="sim-action-button sim-action-unloading" role="status"><Activity size={16} /> Cycle mécanique…</span>
          : status === 'running'
          ? <button className="sim-action-button sim-action-pause" type="button" onClick={() => setStatus('paused')}><CirclePause size={16} /> Pause</button>
          : status === 'unloading'
            ? <span className="sim-action-button sim-action-unloading" role="status"><Activity size={16} /> Cycle de dépôt…</span>
            : <button className="sim-action-button sim-action-play" type="button" onClick={start} disabled={mechanismRunning || emptyCompartments.includes(selectedCompartment)} title={emptyCompartments.includes(selectedCompartment) ? 'Choisir un compartiment chargé ou réinitialiser les casiers.' : undefined}><CirclePlay size={16} /> {status === 'arrived' ? 'Rejouer' : status === 'paused' ? 'Reprendre' : 'Démarrer le trajet'}</button>}
        <button className="sim-icon-button" type="button" onClick={reset} aria-label="Réinitialiser la simulation" title="Réinitialiser"><RotateCcw size={15} /></button>
      </div>
      <div className="bank-sim-destinations" role="group" aria-label="Destination du transfert">
        <span>DESTINATION</span>
        <button type="button" disabled={mechanismRunning || status === 'running' || status === 'unloading'} className={destination === 'Dépôt 3' ? 'destination-active' : ''} onClick={() => selectDestination('Dépôt 3')}><Warehouse size={13} /> Dépôt 3 · prioritaire</button>
        <button type="button" disabled={mechanismRunning || status === 'running' || status === 'unloading'} className={destination === 'Dépôt 1' ? 'destination-active destination-fallback' : ''} onClick={() => selectDestination('Dépôt 1')}><MapPin size={13} /> Dépôt 1 · repli</button>
      </div>
      <label className="bank-sim-speed"><span>VITESSE</span><input aria-label="Vitesse de démonstration en centimètres par seconde" type="range" min="10" max="30" step="10" value={speed} onChange={(event) => setSpeed(Number(event.target.value))} /><strong>{speed} cm/s</strong></label>
      <button className={`sim-icon-button ${showSensors ? 'sim-tool-active' : ''}`} type="button" onClick={() => setShowSensors((visible) => !visible)} aria-label="Afficher ou masquer les faisceaux simulés" title="Faisceaux capteurs"><ScanLine size={16} /></button>
      <div className="bank-sim-progress"><span>TRAJET</span><strong>{Math.round(progress)}%</strong><div><i style={{ width: `${progress}%` }} /></div></div>
    </section>

    <section className="bank-sim-grid">
      <div className="bank-sim-main">
        <section className="sim3d-viewport-panel bank-scene-panel" aria-label="Scène 3D des locaux bancaires sur deux niveaux">
          <div className="sim-panel-heading"><span><Crosshair size={14} /> VUE 3D · DEUX NIVEAUX</span><small>PLAN V0.1 · GÉOMÉTRIE 3D V0.2</small></div>
          <div className="sim3d-viewport bank-3d-viewport">
            <Canvas camera={{ position: [18, 17, 22], fov: 42, near: 0.1, far: 100 }} dpr={[1, 1.25]} gl={{ antialias: false, powerPreference: 'low-power' }} shadows>
              <BankWorld progress={progress} destination={destination} category={category} showSensors={showSensors} mode="orbit" unloadingProgress={unloadingProgress} compartment={selectedCompartment} emptyCompartments={emptyCompartments} />
            </Canvas>
            <div className="viewport-overlay"><span><span className="viewport-dot" /> {stateText.toUpperCase()}</span><span><Wifi size={13} /> LOCAL · AUCUN ROS</span></div>
            <div className="bank-scene-caption"><span>NIVEAU DÉPART · +3 m*</span><i /><span>RDC · 0 m</span></div>
          </div>
          <div className="bank-scene-legend"><span><i className="bank-legend-route" /> Trajet nominal</span><span><i className="bank-legend-robot" /> AGV · enveloppe d’essai</span><span><i className="bank-legend-lift" /> Ascenseur A · aligné</span><span><i className="bank-legend-category" /> C1 / C2 / C3</span></div>
        </section>

        <section className="bank-route-panel">
          <div className="sim-panel-heading"><span><Grid2X2 size={14} /> PLAN SCHÉMATIQUE · DEUX NIVEAUX</span><small>TRAJET NON À L’ÉCHELLE</small></div>
          <div className="bank-route-map-layout">
            <RouteMiniMap destination={destination} category={category} progress={progress} />
            <div className="bank-step-list">{steps.map((step, index) => <div className={`bank-step ${index < currentStep ? 'step-complete' : index === currentStep ? 'step-current' : ''}`} key={`${step}-${index}`}><span>{index < currentStep ? <Check size={12} /> : index + 1}</span><small>{step}</small></div>)}</div>
          </div>
        </section>
      </div>

      <aside className="bank-sim-side">
        <section className="bank-sim-info-card bank-mechanism-card">
          <div className="sim-panel-heading"><span><Activity size={14} /> ANIMATION DU CYCLE · 5 ÉTAPES</span><small>BFM V2 · CONCEPT</small></div>
          <MechanismView
            step={mechanismStep}
            progress={mechanismProgress}
            compartment={selectedCompartment}
            category={category}
            emptyCompartments={emptyCompartments}
            deliveredBags={deliveredBags}
          />
          <div className="bank-mechanism-controls">
            <span className="bank-mechanism-controls-label">CASIER À DÉCHARGER</span>
            <div className="bank-compartment-grid" role="group" aria-label="Choisir le compartiment du sac">
              {COMPARTMENTS.map((compartment) => {
                const empty = emptyCompartments.includes(compartment.id)
                return <button
                  type="button"
                  key={compartment.id}
                  className={`${selectedCompartment === compartment.id ? 'compartment-selected' : ''}${empty ? ' compartment-empty' : ''}`}
                  onClick={() => setSelectedCompartment(compartment.id)}
                  disabled={mechanismRunning || status === 'running' || status === 'unloading'}
                  aria-pressed={selectedCompartment === compartment.id}
                >
                  <strong>{compartment.id}</strong><small>{empty ? 'VIDE' : '40 kg'}</small>
                </button>
              })}
            </div>
            <div className="bank-mechanism-actions">
              <button
                type="button"
                className="sim-action-button sim-action-play"
                onClick={startMechanismDemo}
                disabled={mechanismRunning || status === 'running' || status === 'unloading' || emptyCompartments.includes(selectedCompartment)}
              >
                <CirclePlay size={14} /> {mechanismRunning ? mechanismAutomatic ? 'Cycle automatique…' : 'Cycle en cours…' : 'Lancer le cycle mécanique'}
              </button>
              <button
                type="button"
                className="sim-icon-button"
                onClick={resetCompartments}
                disabled={mechanismRunning || status === 'running' || status === 'unloading' || emptyCompartments.length === 0}
                aria-label="Recharger les quatre compartiments simulés"
                title="Recharger les quatre compartiments"
              ><RotateCcw size={14} /></button>
            </div>
            <div className="bank-mechanism-stage">
              <div><span>ÉTAPE {mechanismStep + 1} / 5</span><strong>{currentMechanismStep.title}</strong></div>
              <p>{currentMechanismStep.detail}</p>
              <div className="bank-mechanism-progress" aria-label={`Progression de l’étape ${Math.round(mechanismProgress * 100)} %`}><i style={{ width: `${mechanismProgress * 100}%` }} /></div>
            </div>
            <ol className="bank-mechanism-steps">
              {MECHANISM_STEPS.map((step, index) => <li key={step.title} className={index < mechanismStep ? 'mechanism-step-done' : index === mechanismStep ? 'mechanism-step-current' : ''}>
                <span>{index < mechanismStep ? <Check size={10} /> : index + 1}</span><small>{step.title}</small><em>{(step.durationMs / 1000).toFixed(1)} s</em>
              </li>)}
            </ol>
            <dl className="bank-mechanism-readouts">
              <div><dt>Compartiment</dt><dd>{selectedCompartment} · {selectedCompartmentInfo.position}</dd></div>
              <div><dt>Charge nominale affichée</dt><dd>40 kg · à confirmer</dd></div>
              <div><dt>Hauteur de prise</dt><dd>{selectedCompartmentInfo.y.toFixed(3)} m · H</dd></div>
              <div><dt>Course tiroir</dt><dd>{DRAWER_STROKE.toFixed(2)} m · H</dd></div>
              <div><dt>Plateau réception</dt><dd>{getStationPlatformHeight(mechanismStep, mechanismProgress, selectedCompartmentInfo.y).toFixed(3)} m · H</dd></div>
              <div><dt>Zone de réception</dt><dd>{category} · tri par commande</dd></div>
            </dl>
            <div className="bank-interlock-state">
              <span><i className={mechanismRunning || status === 'unloading' ? 'interlock-active' : ''} /> Traction {mechanismRunning || status === 'unloading' ? 'inhibée' : 'autorisée en simulation'}</span>
              <span><i className={mechanismRunning && (mechanismStep === 2 || mechanismStep === 3) ? 'interlock-open' : ''} /> Verrou {mechanismRunning && (mechanismStep === 2 || mechanismStep === 3) ? 'libéré' : 'fermé'}</span>
              <small>Transfert à rouleaux illustratif ; choix poussoir / convoyeur non figé.</small>
            </div>
          </div>
        </section>

        <section className="bank-sim-info-card">
          <div className="sim-panel-heading"><span><Activity size={14} /> ÉTAT DE MISSION</span><small>{Math.round(progress)}%</small></div>
          <div className="bank-current-location"><MapPin size={15} /><span><small>POSITION SIMULÉE</small><strong>{position.label}</strong></span></div>
          <div className="bank-destination-summary"><span>ARRIVÉE</span><strong>{destination}</strong><small>{destination === 'Dépôt 3' ? 'Dépôt prioritaire · 4 × 4 m · H' : 'Dépôt de repli · autorisation à confirmer'}</small></div>
          <div className="bank-capacity-row"><span><BatteryMedium size={14} /> Batterie démo</span><strong>82%</strong></div>
          <div className="bank-capacity-row"><span><PackageCheckIcon /> Charge · {category}</span><strong>{status === 'arrived' ? 'Étape simulée terminée' : status === 'unloading' ? 'Animation de transfert' : progress >= deliveryProgress ? 'AGV en retour · vide' : 'Sac embarqué · simulé'}</strong></div>
        </section>

        <section className="bank-sim-info-card bank-auto-deposit-card">
          <div className="sim-panel-heading"><span><PackageCheckIcon /> CYCLE AUTOMATIQUE SIMULÉ</span><small>{category} · {destination.toUpperCase()}</small></div>
          <div className="bank-auto-deposit-content">
            <strong>{status === 'unloading' ? `Cycle mécanique du casier ${selectedCompartment}` : status === 'arrived' ? `Cycle ${category} terminé` : 'Déchargement automatique — concept'}</strong>
            <p>{status === 'unloading'
              ? `Étape ${mechanismStep + 1}/5 : ${currentMechanismStep.title.toLowerCase()}. Le tiroir sélectionné alimente la station élévatrice ; aucun moteur réel n’est commandé.`
              : status === 'arrived'
                ? `La simulation a dirigé le sac vers ${category}. Courses, efforts, synchronisation et sécurités restent à calculer et à tester.`
                : 'Sélectionnez un compartiment et lancez son cycle détaillé, ou démarrez le trajet pour déclencher le transfert simulé à l’arrivée.'}</p>
            {status === 'unloading' && <div className="bank-auto-deposit-progress" aria-label={`Progression du dépôt ${Math.round((unloadingProgress ?? 0) * 100)} %`}><i style={{ width: `${(unloadingProgress ?? 0) * 100}%` }} /></div>}
          </div>
        </section>

        <section className="bank-sim-info-card bank-geometry-card">
          <div className="sim-panel-heading"><span><ShieldCheck size={14} /> ENVELOPPE DE CONTRÔLE</span><small>PARAMÈTRES FOURNIS</small></div>
          <dl>
            <div><dt>Enveloppe orientée</dt><dd>1,30 × 0,90 m</dd></div>
            <div><dt>Châssis d’essai + marge</dt><dd>{ROBOT_TEST_CHASSIS.width.toFixed(2)} × {ROBOT_TEST_CHASSIS.depth.toFixed(2)} m + {ROBOT_TEST_CHASSIS.margin.toFixed(2)} m/face</dd></div>
            <div><dt>Pas de translation</dt><dd>≤ 0,025 m</dd></div>
            <div><dt>Pas angulaire</dt><dd>≤ 2°</dd></div>
            <div><dt>Virages RDC 5/6</dt><dd>{CLEAR_TURN.width.toFixed(2)} × {CLEAR_TURN.depth.toFixed(2)} m · H</dd></div>
            <div><dt>Portes</dt><dd>Ouvertes pour le contrôle</dd></div>
          </dl>
          <p className="bank-validation-note"><AlertTriangle size={13} /> Les résultats de validation géométrique du JSON ne sont pas importés dans ce prototype.</p>
        </section>

        <section className="bank-sim-info-card">
          <div className="sim-panel-heading"><span><Activity size={14} /> INTERFACES ROS 2 · RÉF. PARC</span><small>À CONFIRMER</small></div>
          <div className="bank-sensor-row"><ScanLine size={14} /><span><strong>RPLIDAR C1</strong><small>/scan</small></span><i /></div>
          <div className="bank-sensor-row"><Camera size={14} /><span><strong>D435i supérieure</strong><small>/top_camera_color · /top_camera_depth</small></span><i /></div>
          <div className="bank-sensor-row"><Camera size={14} /><span><strong>D435i inférieure</strong><small>/bottom_camera_color · /bottom_camera_depth</small></span><i /></div>
          <div className="bank-sensor-row"><Activity size={14} /><span><strong>IMU</strong><small>/imu</small></span><i /></div>
        </section>
      </aside>
    </section>

    <section className="bank-camera-strip" aria-label="Vues de caméra synthétiques">
      <CameraView mode="top" progress={progress} destination={destination} category={category} unloadingProgress={unloadingProgress} compartment={selectedCompartment} emptyCompartments={emptyCompartments} />
      <CameraView mode="bottom" progress={progress} destination={destination} category={category} unloadingProgress={unloadingProgress} compartment={selectedCompartment} emptyCompartments={emptyCompartments} />
      <div className="bank-camera-disclaimer"><Camera size={16} /><span><strong>Vues POV de synthèse.</strong> Images calculées de la scène 3D, pas des flux réels. Topics et capteurs issus de la référence PARC, à confirmer pour l’AGV bancaire ; aucun flux ROS 2 n’est connecté.</span></div>
    </section>

    <footer className="sim3d-footer bank-sim-footer"><span><ShieldCheck size={12} /> Géométrie issue du descriptif utilisateur · D = donnée, H = hypothèse</span><span>AGV BANCAIRE · V0.1 · *Altitude proposée</span></footer>
  </main>
}

function PackageCheckIcon() {
  return <span className="bank-package-glyph">C1–C3</span>
}

export default Simulation3D
