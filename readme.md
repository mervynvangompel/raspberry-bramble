# The Raspberry Bramble
A Kubernetes Homelab for a Dog Food Tracker

## Goal

Build a small Kubernetes homelab to:

- Learn Kubernetes hands-on (nodes, networking, storage, deployments)
- Run a simple dog food tracking app
- Store data in PostgreSQL
- Visualize consumption trends in Grafana

## MVP Definition

The project is considered successful when:

- A 3-node Kubernetes cluster is running
- PostgreSQL is deployed with persistent storage
- A simple web app allows entering dog food (cups/day)
- Data is stored in PostgreSQL
- Grafana shows a basic dashboard of daily consumption

## Architecture

### Hardware

| Node | Role | IP |
|------|------|----|
| Desktop (Ubuntu) | Control plane + platform services | 192.168.1.10 |
| Raspberry Pi #1 | Worker | 192.168.1.11 |
| Raspberry Pi #2 | Worker | 192.168.1.12 |
| Raspberry Pi #3 | Optional | unused |

### Network

Network: 192.168.1.0/24

| Purpose | Range |
|--------|------|
| Nodes | .10–.20 |
| MetalLB | .200–.220 |

### Kubernetes Layer

- Kubernetes distro: k3s
- Control plane: Desktop
- Workers: Raspberry Pis

Networking:
- Ingress: Traefik
- LoadBalancer: MetalLB

### Storage Strategy

Phase 1:
- Use local-path provisioner

Phase 2:
- Add NFS server on desktop

### Platform Layer

- PostgreSQL
- Kubernetes Secrets
- PersistentVolume

### Application Layer

Design:

[Web Form] → [API] → [PostgreSQL]

Data model:

- date
- cups

### Observability

- Grafana
- Data source: PostgreSQL

## Execution Plan

### Phase 0 — Prepare hardware

- Flash Raspberry Pi OS or Ubuntu Server to SD cards
- Enable SSH
- Boot Pis
- Update packages
- Set hostnames
- Configure static IPs
- Disable swap

### Phase 1 — Cluster setup

- Install k3s on desktop
- Retrieve join token
- Join Raspberry Pis
- Verify nodes

### Phase 2 — Networking

- Install MetalLB
- Configure IP pool
- Deploy test service
- Verify LoadBalancer

### Phase 3 — Storage and PostgreSQL

- Use local-path storage
- Deploy PostgreSQL
- Create Secret
- Verify persistence

### Phase 4 — Application

- Build API
- Containerize app
- Deploy to cluster
- Verify data storage

### Phase 5 — Observability

- Install Grafana
- Connect to PostgreSQL
- Build dashboard

### Phase 6 — Improvements

- Add NFS storage
- Add backups
- Introduce GitOps

## Repo Structure

infra/      node and networking setup
k8s/        manifests
app/        dog tracker code
docs/       notes
scripts/    helpers

## Mental Model

Network → Nodes → Kubernetes → Platform → App → Observability
