# Phase 1 — Single-Node k3s Deployment
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