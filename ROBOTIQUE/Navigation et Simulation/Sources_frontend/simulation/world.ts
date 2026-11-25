import scene from './scene_3d.json'

export type BankDestination = 'Dépôt 3' | 'Dépôt 1'
export type BagCategory = 'C1' | 'C2' | 'C3'
export type BankFloor = 'départ' | 'rdc'

export type RoutePoint = {
  x: number
  z: number
  floor: BankFloor
  label: string
  delivery?: boolean
}

export type PlanObject = {
  name: string
  level: string
  kind: string
  center: [number, number, number]
  size: [number, number, number]
  yaw: number
  color: string
  mesh: string
}

export type PlanLabel = {
  level: string
  p: [number, number, number]
  text: string
  color?: string
}

function toVector3(values: number[], name: string): [number, number, number] {
  if (values.length !== 3 || values.some((value) => !Number.isFinite(value))) {
    throw new Error(`Invalid 3D coordinates for ${name}.`)
  }
  return [values[0], values[1], values[2]]
}

export const PLAN_OBJECTS: PlanObject[] = scene.objects.map((object) => ({
  ...object,
  center: toVector3(object.center, object.name),
  size: toVector3(object.size, object.name),
}))
export const PLAN_LABELS: PlanLabel[] = scene.labels.map((label) => ({
  ...label,
  p: toVector3(label.p, label.text),
}))
export const LIFT = { x: -5.12, z: 1, width: 2.2, depth: 2.2 }
export const ROBOT_ENVELOPE = { width: 1.3, depth: 0.9 }
export const ROBOT_TEST_CHASSIS = { width: 1.1, depth: 0.7, margin: 0.1 }
export const CLEAR_TURN = { width: 1.8, depth: 1.8 }
export const DEPARTURE_ALTITUDE = 3

export const DEFAULT_DESTINATION: BankDestination = 'Dépôt 3'

const departureRoute: RoutePoint[] = [
  { x: 5, z: 4.8, floor: 'départ', label: 'Salle de collecte' },
  { x: 5, z: 4.65, floor: 'départ', label: 'Virage dans la collecte' },
  { x: 0.88, z: 4.65, floor: 'départ', label: 'Sortie sud' },
  { x: 0.88, z: -1.2, floor: 'départ', label: 'Passage ouest' },
  { x: -5.12, z: -1.2, floor: 'départ', label: 'Couloir du niveau de départ' },
  { x: LIFT.x, z: LIFT.z, floor: 'départ', label: 'Ascenseur A' },
]

const groundFloorRoute: RoutePoint[] = [
  { x: LIFT.x, z: LIFT.z, floor: 'rdc', label: 'Ascenseur A · RDC' },
  { x: -5.12, z: -1.2, floor: 'rdc', label: 'Sortie de cabine' },
  { x: -3.12, z: -1.2, floor: 'rdc', label: 'Couloir 1' },
  { x: -3.12, z: 4.8, floor: 'rdc', label: 'Virage 5 · couloir 2' },
  { x: 6.88, z: 4.8, floor: 'rdc', label: 'Couloir 2' },
  { x: 8.8, z: 4.8, floor: 'rdc', label: 'Virage 6' },
]

const categoryReceptionX: Record<BagCategory, number> = { C1: 10.85, C2: 12, C3: 13.15 }

export function getRoute(destination: BankDestination, category: BagCategory = 'C1'): RoutePoint[] {
  if (destination === 'Dépôt 1') {
    return [
      ...departureRoute,
      ...groundFloorRoute,
      { x: 12, z: 4.8, floor: 'rdc', label: 'Entrée du dépôt 1' },
      { x: 12, z: 4.8, floor: 'rdc', label: 'Dépôt simulé · zone à confirmer', delivery: true },
    ]
  }
  const receptionX = categoryReceptionX[category]
  return [
    ...departureRoute,
    ...groundFloorRoute,
    { x: 8.8, z: 11.54, floor: 'rdc', label: 'Accès aux dépôts' },
    { x: receptionX, z: 11.54, floor: 'rdc', label: `Accostage réception ${category}` },
    { x: receptionX, z: 11.95, floor: 'rdc', label: `Dépôt simulé ${category}`, delivery: true },
    { x: receptionX, z: 11.54, floor: 'rdc', label: 'Recul après dépôt' },
    { x: 7.8, z: 11.54, floor: 'rdc', label: 'Retour vers attente' },
    { x: 7.8, z: 10.4, floor: 'rdc', label: 'Attente dépôt 3' },
  ]
}

export function getDeliveryProgress(destination: BankDestination, category: BagCategory = 'C1') {
  const route = getRoute(destination, category)
  const deliveryIndex = route.findIndex((point) => point.delivery)
  return deliveryIndex / (route.length - 1) * 100
}

export function getDeliveryPoint(destination: BankDestination, category: BagCategory = 'C1') {
  return getRoute(destination, category).find((point) => point.delivery)
}

export function getRoutePosition(progress: number, destination: BankDestination, category: BagCategory = 'C1') {
  const route = getRoute(destination, category)
  const routePosition = Math.max(0, Math.min(progress, 100)) / 100 * (route.length - 1)
  const segment = Math.min(Math.floor(routePosition), route.length - 2)
  const fraction = routePosition - segment
  const start = route[segment]
  const end = route[segment + 1]
  const startY = start.floor === 'départ' ? DEPARTURE_ALTITUDE : 0
  const endY = end.floor === 'départ' ? DEPARTURE_ALTITUDE : 0

  return {
    x: start.x + (end.x - start.x) * fraction,
    y: startY + (endY - startY) * fraction,
    z: start.z + (end.z - start.z) * fraction,
    yaw: Math.atan2(-(end.x - start.x), -(end.z - start.z)),
    label: progress >= 100 ? route[route.length - 1].label : start.label,
    route,
  }
}

export function getRouteSamples(destination: BankDestination, stepsPerSegment = 8, category: BagCategory = 'C1') {
  const route = getRoute(destination, category)
  return route.flatMap((point, index) => {
    if (index === route.length - 1) return []
    const next = route[index + 1]
    const startY = point.floor === 'départ' ? DEPARTURE_ALTITUDE : 0
    const nextY = next.floor === 'départ' ? DEPARTURE_ALTITUDE : 0
    return Array.from({ length: stepsPerSegment }, (_, step) => {
      const fraction = step / stepsPerSegment
      return {
        x: point.x + (next.x - point.x) * fraction,
        y: startY + (nextY - startY) * fraction,
        z: point.z + (next.z - point.z) * fraction,
      }
    })
  })
}

export function getCurrentStop(progress: number, destination: BankDestination, category: BagCategory = 'C1') {
  const route = getRoute(destination, category)
  const index = Math.min(Math.floor(Math.max(0, Math.min(progress, 100)) / 100 * (route.length - 1)), route.length - 1)
  return route[index].label
}
