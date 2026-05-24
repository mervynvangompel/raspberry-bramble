# The Raspberry Bramble
A Kubernetes Homelab for a Dog Food Tracker

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

This avoids complexity creep and ensures you understand each layer before adding the next.

## MVP Definition
The project is considered successful when:
- A working Kubernetes cluster is running (starting with 1 node, expanding to 3)
- PostgreSQL is deployed with persistent storage
- A simple web app allows entering dog food consumption (cups/day)
- Data is stored in PostgreSQL and persists across restarts
- Grafana shows a basic dashboard of daily consumption

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

## Execution Plan

### Phase 0 — Prepare Hardware ✅ IN PROGRESS
**Goal:** Get all Raspberry Pis flashed and accessible via SSH

Tasks:
- [x] Flash Raspberry Pi OS Lite (64-bit) to SD cards
- [x] Manually enable SSH (create `ssh` file on bootfs)
- [x] Manually create user (create `userconf.txt` on bootfs)
- [x] Boot Pis and verify SSH access
- [x] Set hostnames (pi-control, pi-worker1, pi-worker2)
- [x] Configure static IPs (.11, .12, .13)
- [ ] Update packages on all nodes
- [ ] Disable swap on all nodes
- [ ] Configure /etc/hosts on all nodes for cluster communication

**Current Status:**
- pi-control: Configured, SSH working ✅
- pi-worker1: Pending
- pi-worker2: Pending

**Lessons Learned:**
- Raspberry Pi Imager's customization settings don't apply reliably
- Manual configuration via `ssh` file and `userconf.txt` is more reliable
- See `docs/pi-setup-procedure.md` for detailed steps

---

### Phase 1 — Single-Node k3s Deployment
**Goal:** Get the POC application running on ONE Raspberry Pi to prove everything works

**Why start with one node?**
- Simpler troubleshooting (fewer moving parts)
- Faster iteration
- Builds confidence before adding complexity
- Learn k3s basics without cluster coordination issues

Tasks:
- Install k3s on pi-control (control plane only, no workers yet)
- Copy kubeconfig to Ubuntu desktop
- Verify cluster health:
  - `kubectl get nodes` (pi-control Ready?)
  - `kubectl get pods -A` (all system pods running?)
  - `kubectl cluster-info`
- Deploy test workload (nginx) to verify basic functionality
- Push POC Docker images to registry (Docker Hub or local)
- Deploy PostgreSQL with local-path storage
- Deploy API and Frontend
- Configure Ingress (Traefik)
- Test end-to-end: Can you access the app and add feeding data?

**Success Criteria:**
- Can access dog feeding tracker from browser on Ubuntu desktop
- Can add feeding entries and see them persist
- Understand how Deployments, Services, and Ingress work

**LinkedIn Post:** "Got my dog feeding tracker running on Kubernetes! Single Pi cluster, Traefik ingress, working end-to-end. Next: expanding to 3 nodes."

---

### Phase 2 — Expand to Three-Node Cluster
**Goal:** Add worker nodes and learn cluster behavior

Tasks:
- Prepare USB stick for PostgreSQL:
  - Format USB stick (ext4)
  - Mount on pi-worker1
  - Add to /etc/fstab for persistence
  - Create directory for PostgreSQL data
- Join pi-worker1 to cluster as worker
- Join pi-worker2 to cluster as worker
- Verify all nodes are Ready
- Migrate PostgreSQL to USB-backed storage on pi-worker1
- Deploy remaining workloads (API, Frontend) across workers
- Test pod scheduling and node affinity
- Experiment: Drain a node and watch pods reschedule

**Success Criteria:**
- 3-node cluster with all nodes Ready
- PostgreSQL runs on pi-worker1 with USB storage
- Understand how k8s schedules workloads across nodes
- Can handle node failure gracefully

**LinkedIn Post:** "Expanded to 3-node Raspberry Pi cluster. Learned about pod scheduling, node draining, and persistent storage. The Bramble is growing!"

---

### Phase 3 — Observability
**Goal:** Add monitoring and visualization

Tasks:
- Install Grafana (via Helm or manifest)
- Configure PostgreSQL as data source
- Build dashboard showing:
  - Daily cups consumed
  - Feeding frequency
  - Weekly/monthly trends
  - Last feeding timestamp
- (Optional) Install Prometheus for cluster metrics
- (Optional) Add Loki for log aggregation

**Success Criteria:**
- Can visualize Pippi's feeding trends over time
- Grafana dashboard looks good enough to screenshot for LinkedIn

**LinkedIn Post:** "Added Grafana dashboards to visualize feeding patterns. Now I can see if we're overfeeding on weekends!"

---

### Phase 4 — Polish & Stabilize
**Goal:** Make it production-ready for daily use

Tasks:
- Add authentication (basic auth or OAuth2 Proxy)
- Set up automated PostgreSQL backups
- Add health checks and readiness probes
- Configure resource limits for all workloads
- Test failure scenarios:
  - Node reboot
  - Pod crash
  - Network interruption
- Document recovery procedures

**Success Criteria:**
- System is stable enough for daily family use
- Can recover from common failure scenarios
- Family members can use it without your help

---

### Phase 5 — Advanced Features (Optional)
**Goal:** Level up your homelab

Pick and choose based on interest:

**Infrastructure as Code:**
- Convert Kubernetes manifests to Terraform
- Write Ansible playbooks for Pi provisioning
- Set up GitOps with ArgoCD

**Distributed Storage:**
- Install Longhorn
- Migrate PostgreSQL to replicated storage
- Test node failure with HA storage

**Public Access:**
- Set up Cloudflare Tunnel
- Configure TLS certificates with cert-manager
- Make dashboard publicly accessible (read-only)

**CI/CD:**
- GitHub Actions for building container images
- Automatic deployment on git push

**Advanced Monitoring:**
- Prometheus for cluster metrics
- Alert rules for node failures
- Custom metrics from FastAPI

**Application Features:**
- Mobile PWA (works like an app)
- Notifications if dog not fed by certain time
- Multi-user support with Google login
- Analytics and trends

---

## Repo Structure
```
raspberry-bramble/
├── docs/               # Documentation
│   ├── pi-setup-procedure.md
│   ├── architecture.md
│   └── troubleshooting.md
├── k8s/                # Kubernetes manifests
│   ├── phase1-single-node/
│   ├── phase2-cluster/
│   ├── postgres/
│   ├── api/
│   ├── frontend/
│   └── monitoring/
├── app/                # Application code (from POC)
│   ├── api/
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── frontend/
│       ├── index.html
│       ├── nginx.conf
│       └── Dockerfile.frontend
├── terraform/          # IaC (Phase 5)
├── ansible/            # Provisioning playbooks (Phase 5)
├── images/             # Screenshots for LinkedIn
└── scripts/            # Helper scripts
```

## Mental Model
```
Physical → Network → OS → Container Runtime → Kubernetes → Platform → App → Users
```

Each layer builds on the previous. Understand one before moving to the next.

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

By the end of this project, you will understand:

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

**Phase 5 (Optional):**
- Infrastructure as Code (Terraform)
- GitOps workflows
- Distributed storage systems
- CI/CD pipelines

## Common Pitfalls to Avoid

1. **Complexity creep:** Don't add Istio, service mesh, or 5 monitoring tools before the basic app works
2. **ARM compatibility:** Always check if container images support ARM64
3. **SD card failure:** Plan to migrate to USB/SSD storage early
4. **Power supply issues:** Use official Raspberry Pi power supplies
5. **Skipping basics:** Understand how something works before abstracting it away

## Resources

- [k3s Documentation](https://docs.k3s.io/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [Longhorn Documentation](https://longhorn.io/docs/)

## Next Steps

**Right now:** Complete Phase 0 (flash remaining Pis)

**This week:** Deploy single-node k3s and get POC app running (Phase 1)

**This month:** Expand to 3-node cluster and add Grafana (Phases 2-3)

**Later:** Polish, stabilize, and add advanced features as desired (Phases 4-5)

---

**Remember:** The goal is learning, not perfection. Each phase is a LinkedIn post, a learning milestone, and a stepping stone to the next level. Have fun! 🫐🚀