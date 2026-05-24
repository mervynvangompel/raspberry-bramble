## Architecture

### Hardware
| Node | Role | IP |
|------|------|----|
| Desktop (Ubuntu) | Management workstation (kubectl access only) | 192.168.68.55 |
| Raspberry Pi #1 | Control plane | 192.168.68.11 |
| Raspberry Pi #2 | Worker (PostgreSQL on USB stick) | 192.168.68.12 |
| Raspberry Pi #3 | Worker | 192.168.68.13 |

### Network
Network: 192.168.68.0/22 (existing home network)

| Purpose | IP/Range |
|--------|----------|
| Management | .55 |
| Nodes | .11–.13 |
| Services (DHCP) | Assigned by k3s |

*Note: Starting with existing network for simplicity. Can migrate to dedicated subnet later.*

### Kubernetes Layer
- Kubernetes distro: **k3s** (lightweight, ARM-friendly, homelab standard)
- Initial setup: Single node (pi-control)
- Expanded setup: 1 control plane + 2 workers
- OS: Raspberry Pi OS Lite (64-bit)

Networking:
- Ingress: Traefik (built into k3s)
- DNS: CoreDNS (built into k3s)
- LoadBalancer: ServiceLB (built into k3s, can add MetalLB later)

### Storage Strategy
Phase 1 (Single Node):
- local-path provisioner (default with k3s)
- PostgreSQL on local storage

Phase 2 (Cluster):
- USB stick mounted on pi-worker1 for PostgreSQL
- local-path for other workloads

Phase 3 (Optional - Advanced):
- Migrate to external SSD
- Consider Longhorn for distributed storage

### Platform Layer
- PostgreSQL (single replica initially)
- Kubernetes Secrets for credentials
- PersistentVolume and PersistentVolumeClaim

### Application Layer
Design:
```
[Browser] → [Ingress] → [Frontend] → [API] → [PostgreSQL]
```

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
- Grafana (PostgreSQL as data source)
- Prometheus (optional for cluster metrics)