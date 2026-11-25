#!/usr/bin/env bash
set -euo pipefail
agv_project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if ! command -v gz >/dev/null 2>&1; then
  printf '%s\n' 'Gazebo est introuvable. Installer Gazebo Harmonic avant de lancer cette maquette.' >&2
  exit 1
fi
case "${1:-depart}" in
  depart) agv_world='niveau_depart_coupe.sdf' ;;
  rdc) agv_world='rez_de_chaussee_coupe.sdf' ;;
  complet) agv_world='batiment_complet.sdf' ;;
  *) printf '%s\n' 'Usage : bash lancer_gazebo.sh depart|rdc|complet' >&2; exit 2 ;;
esac
exec gz sim "$agv_project_dir/modeles/$agv_world"
