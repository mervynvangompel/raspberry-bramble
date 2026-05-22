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
- A 3-node Kubernetes cluster is running (all Pis)
- PostgreSQL is deployed with persistent storage on USB
- A simple web app allows entering dog food (cups/day)
- Data is stored in PostgreSQL
- Grafana shows a basic dashboard of daily consumption

## Architecture

### Hardware
| Node | Role | IP |
|------|------|----|
| Desktop (Ubuntu) | Management workstation (kubectl access only) | 192.168.50.10 |
| Raspberry Pi #1 | Control plane | 192.168.50.11 |
| Raspberry Pi #2 | Worker (PostgreSQL on USB stick) | 192.168.50.12 |
| Raspberry Pi #3 | Worker | 192.168.50.13 |

### Network
Network: 192.168.50.0/24 (dedicated homelab subnet)

| Purpose | Range |
|--------|------|
| Management | .10 |
| Nodes | .11–.13 |
| MetalLB | .200–.220 |

### Kubernetes Layer
- Kubernetes distro: k3s
- Control plane: Raspberry Pi #1
- Workers: Raspberry Pi #2, #3
- OS: Raspberry Pi OS Lite (64-bit)

Networking:
- Ingress: Traefik (built into k3s)
- LoadBalancer: MetalLB

### Storage Strategy
Phase 1:
- local-path provisioner (default with k3s)
- PostgreSQL data on USB stick mounted on pi-worker1 (192.168.50.12)

Phase 2 (optional):
- Migrate to external SSD
- Consider NFS if multi-replica databases needed later

### Platform Layer
- PostgreSQL (with USB-backed PersistentVolume)
- Kubernetes Secrets for credentials
- PersistentVolume and PersistentVolumeClaim

### Application Layer
Design:
[Web Form] → [API] → [PostgreSQL]
Data model:
- id (primary key)
- timestamp (datetime)
- cups (decimal)
- notes (text, optional)

Components (already built in POC):
- Frontend: Nginx serving HTML/JS
- API: Python FastAPI
- Database: PostgreSQL

### Observability
- Grafana
- Data source: PostgreSQL
- Prometheus (optional for cluster metrics)

## Execution Plan

### Phase 0 — Prepare hardware
- Flash Raspberry Pi OS Lite (64-bit) to SD cards
- Configure during flash:
  - Enable SSH
  - Set hostnames (pi-control, pi-worker1, pi-worker2)
  - Configure static IPs
- Boot Pis and verify SSH access
- Update packages on all nodes
- Disable swap on all nodes
- Configure /etc/hosts on all nodes (including Ubuntu desktop):
Device	        IP
ubuntu-desktop	192.168.68.55 (already)
pi-control	    192.168.68.60
pi-worker1	    192.168.68.61
pi-worker2	    192.168.68.62

- Prepare USB stick:
  - Format USB stick (ext4)
  - Mount on pi-worker1
  - Add to /etc/fstab for persistence
  - Create directory for PostgreSQL data

### Phase 1 — Cluster setup
- Install k3s on pi-control (control plane)
- Retrieve join token from pi-control
- Join pi-worker1 and pi-worker2 to cluster
- Copy kubeconfig to Ubuntu desktop
- Verify cluster health:
  - `kubectl get nodes` (all Ready?)
  - `kubectl get pods -A` (all system pods running?)
  - `kubectl cluster-info`
- Deploy test workload (nginx) to verify basic functionality

### Phase 2 — Networking
- Install MetalLB
- Configure IP pool (192.168.50.200-220)
- Deploy test service with LoadBalancer type
- Verify external IP assignment
- Test access from Ubuntu desktop

### Phase 3 — Storage and PostgreSQL
- Verify local-path provisioner is working
- Create PersistentVolume pointing to USB mount on pi-worker1
- Create PersistentVolumeClaim
- Create Secret for PostgreSQL credentials
- Deploy PostgreSQL StatefulSet with:
  - Volume mounted from USB
  - Resource limits appropriate for Pi
  - Health checks
- Verify PostgreSQL is running and data persists
- Test database connection

### Phase 4 — Application
- Push existing POC Docker images to registry:
  - dog-feeding-api:latest
  - dog-feeding-frontend:latest
  - (Use Docker Hub or set up local registry)
- Update image references in Kubernetes manifests
- Deploy in order:
  1. PostgreSQL (already done in Phase 3)
  2. API (with ConfigMap and Secret for DB connection)
  3. Frontend (with nginx config for API proxy)
- Test via port-forward first
- Configure Ingress for external access
- Verify end-to-end functionality:
  - Add feeding entry via web UI
  - Check data in PostgreSQL
  - Verify stats endpoint works

### Phase 5 — Observability
- Install Grafana (via Helm or manifest)
- Configure PostgreSQL as data source
- Build dashboard showing:
  - Daily cups consumed
  - Feeding frequency
  - Weekly/monthly trends
  - Last feeding timestamp
- Set up basic alerts (optional)

### Phase 6 — Improvements (optional)
- Add automated backups of PostgreSQL
- Migrate from USB stick to external SSD
- Set up cert-manager for TLS certificates
- Configure Cloudflare Tunnel for public access
- Add authentication (OAuth2 Proxy or basic auth)

### Phase 7 — Infrastructure as Code (optional)
- Convert Kubernetes manifests to Terraform
- Organize:
  - providers.tf
  - variables.tf
  - database.tf
  - api.tf
  - frontend.tf
  - monitoring.tf
- Test `terraform apply` workflow
- Document state management

## Repo Structure
raspberry-bramble/
├── infra/          # Node and networking setup scripts
├── k8s/            # Kubernetes manifests
│   ├── postgres/
│   ├── api/
│   ├── frontend/
│   └── monitoring/
├── app/            # Dog tracker application code
│   ├── api/
│   └── frontend/
├── terraform/      # IaC (Phase 7)
├── docs/           # Documentation and notes
├── images/         # Screenshots for LinkedIn posts
└── scripts/        # Helper scripts
## Mental Model
Network → Nodes → Kubernetes → Platform → App → Observability
## Success Criteria
The project is complete when:
- [ ] 3-node Pi cluster is stable
- [ ] Can add feeding data via web UI
- [ ] Data persists across pod restarts
- [ ] Grafana dashboard shows consumption trends
- [ ] Can access app from Ubuntu desktop
- [ ] Documentation is complete for LinkedIn/GitHub

## Learning Outcomes
- Kubernetes cluster architecture and node management
- Persistent storage in Kubernetes
- Service networking and ingress
- Container image management and registries
- Stateful applications in Kubernetes
- Monitoring and observability
- Infrastructure as Code with Terraform (optional)
