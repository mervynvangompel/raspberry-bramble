# Phase 3 — Observability
**Goal:** Add monitoring and visualization of Pippi's feeding data

## Tasks
- Install Grafana via raw manifests (learning exercise):
  - Deployment running grafana/grafana container
  - PersistentVolume backed by USB stick on pi-worker1 (`/mnt/usb/grafana`)
  - PersistentVolumeClaim bound to that PV
  - Service to expose Grafana internally
  - ConfigMap for PostgreSQL datasource configuration
  - Ingress via Traefik at `192.168.68.11/grafana`
- Configure PostgreSQL as datasource
- Build dashboard showing:
  - Daily cups consumed
  - Feeding frequency
  - Weekly/monthly trends
  - Last feeding timestamp
- Tear down and reinstall via Helm (to understand what Helm abstracts away)

## De-scoped and moved to phase 4
- Prometheus for cluster metrics
- Loki for log aggregation

## Future Enhancements
- Revisit Phase 1 and Phase 2 manifests and install equivalents via Helm

## Success Criteria
- Can visualize Pippi's feeding trends over time
- Grafana dashboard looks good enough to screenshot for LinkedIn
- Understand what Helm does by having done it manually first

## LinkedIn Post
"Added Grafana dashboards to visualize Pippi's feeding patterns. Now I can see if we're overfeeding on weekends (without judgement)!"
