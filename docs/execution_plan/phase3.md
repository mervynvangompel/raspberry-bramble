# Phase 3 — Observability
**Status: Complete ✅**
**Goal:** Add monitoring and visualization of Pippi's feeding data

## Tasks

### Grafana via raw manifests (learning exercise) ✅
- Deployment running `grafana/grafana` container
- PersistentVolume backed by USB stick on pi-worker1 (`/mnt/usb/grafana`)
- PersistentVolumeClaim bound to that PV
- Service to expose Grafana internally
- ConfigMap for PostgreSQL datasource configuration (note: env var substitution not supported in ConfigMap provisioning — datasource configured manually via UI and persisted to PVC)
- Ingress via Traefik at `192.168.68.11/grafana`
  - Key learning: Grafana must handle its own `/grafana` subpath prefix internally — stripping the prefix via Traefik Middleware causes redirect loops

### Grafana reinstalled via Helm ✅
- Chart: `grafana/grafana`
- Pinned to v11.4.0 (v12.3.1 has a known PostgreSQL plugin bug)
- Values file: `~/Desktop/bramble/infra/grafana-values.yaml`
- Accessible at `192.168.68.11/grafana` via Traefik IngressRoute

### PostgreSQL datasource configured ✅
- Database: `dogfeeding`
- User: `postgres`
- Host: `postgres:5432`
- SSL: disabled
- Configured manually via UI (not provisioned via ConfigMap)
- Persisted to USB-backed PVC at `/mnt/usb/grafana`

### Dashboard built ✅
- Name: "Pippi's Feeding Tracker"
- Four panels:
  - Daily cups consumed
  - Feeding frequency
  - Last feeding timestamp
  - Weekly average cups
- 157 rows of historical feeding data imported
- Public dashboard URL: `http://192.168.68.11/grafana/public-dashboards/6bfde3cb27134b4183e711ed673efbd4`

### Frontend cleanup ✅
- Removed stale "Feedings Today" counter
- Added embedded Grafana public dashboard
- Kept Pippi's photo and feeding form

## De-scoped and moved to Phase 4
- Prometheus for cluster metrics
- Loki for log aggregation

## Future Enhancements
- Revisit Phase 1 and Phase 2 manifests and install equivalents via Helm
- Automate backup of PostgreSQL database

## Key Learnings
- Grafana subpath routing: strip-prefix middleware causes redirect loops; Grafana must own its prefix internally
- ConfigMap provisioning does not support env var substitution; use UI or a proper secrets approach
- Grafana v12.3.1 has a PostgreSQL plugin bug — pin to v11.4.0

## Success Criteria
- ✅ Can visualize Pippi's feeding trends over time
- ✅ Grafana dashboard looks good enough to screenshot for LinkedIn
- ✅ Understand what Helm does by having done it manually first

## LinkedIn Post
"Added Grafana dashboards to visualize Pippi's feeding patterns. Now I can see if we're overfeeding on weekends (without judgement)!"