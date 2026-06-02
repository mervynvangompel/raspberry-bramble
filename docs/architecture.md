# The Raspberry Bramble — Architecture & Design Philosophy

## Goal

Build a small Kubernetes homelab to:
- Learn Kubernetes hands-on (nodes, networking, storage, deployments)
- Run a simple dog food tracking app
- Store data in PostgreSQL
- Visualize consumption trends in Grafana

## Philosophy

**Simple app first, homelab platform second.**

This project follows an incremental approach:
1. Get it working on one node first
2. Then expand to a cluster
3. Add features iteratively

This avoids complexity creep and ensures understanding each layer before adding the next.

## MVP Definition

The project is considered successful when:
- A working Kubernetes cluster is running (starting with 1 node, expanding to 3)
- PostgreSQL is deployed with persistent storage
- A simple web app allows entering dog food consumption (cups/day)
- Data is stored in PostgreSQL and persists across restarts
- Grafana shows a basic dashboard of daily consumption

## Mental Model

```
Physical → Network → OS → Container Runtime → Kubernetes → Platform → App → Users
```

Each layer builds on the previous. Understand one before moving to the next.

---

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

---

## Success Criteria Checklist

**Phase 1:**
- [ ] Single-node k3s cluster running
- [ ] POC app deployed and accessible
- [ ] Can add feeding data via web UI
- [ ] Data persists across pod restarts

**Phase 2:**
- [ ] 3-node cluster is stable
- [ ] PostgreSQL on USB storage
- [ ] Understand pod scheduling

**Phase 3:**
- [ ] Grafana dashboard showing trends
- [ ] Screenshots for LinkedIn

**Phase 4:**
- [ ] System stable for daily use
- [ ] Basic auth configured
- [ ] Backups working

**Phase 5:**
- [ ] Pick features based on interest

## Learning Outcomes

By the end of this project, I hope to have a good understanding of:

**Phase 1:**
- How to install and configure k3s
- Kubernetes basics: Pods, Deployments, Services
- How Ingress controllers route traffic
- Container registries and image management
- ConfigMaps and Secrets

**Phase 2:**
- Multi-node cluster architecture
- How k8s schedules workloads
- Persistent storage with PVs and PVCs
- StatefulSets for databases
- Node management and cluster operations

**Phase 3:**
- Monitoring and observability
- Grafana dashboards
- Connecting external data sources

**Phase 4:**
- Production best practices
- Security and authentication
- Backup and disaster recovery
- Resource management

**Phase 5:**
- Infrastructure as Code (Terraform)
- GitOps workflows
- Distributed storage systems
- CI/CD pipelines

## Common Pitfalls to Avoid

1. **Complexity creep:** Don't add Istio, service mesh, or 5 monitoring tools before the basic app works
2. **ARM compatibility:** Always check if container images support ARM64
3. **SD card failure:** Plan to migrate to USB/SSD storage early
4. **Power supply issues:** Use Raspberry Pi power supplies
5. **Skipping basics:** Understand how something works before abstracting it away

## Resources

- [k3s Documentation](https://docs.k3s.io/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [Longhorn Documentation](https://longhorn.io/docs/)

The goal is learning, not perfection! 🫐🚀