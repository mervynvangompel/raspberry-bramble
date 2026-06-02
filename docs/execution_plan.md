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
- [x] Update packages on all nodes
- [x] Disable swap on all nodes
- [x] Configure /etc/hosts on all nodes for cluster communication

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