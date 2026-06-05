# Phase 2 — Expand to Three-Node Cluster
**Goal:** Add worker nodes and learn cluster behavior

## Tasks
- ✅ Prepare USB stick for PostgreSQL:
  - ✅ Format USB stick (ext4) — formatted as `/dev/sda`, no partition table
  - ✅ Mount on pi-worker1 at `/mnt/usb`
  - ✅ Add to /etc/fstab for persistence (UUID=11f581fc-b36c-4540-b064-9d1c6e88f5a8, nofail)
  - ✅ Create directory for PostgreSQL data (`/mnt/usb/postgresql`, chown 999:999)
- ✅ Join pi-worker1 to cluster as worker
  - Note: required adding `cgroup_enable=cpuset cgroup_enable=memory cgroup_memory=1` to `/boot/firmware/cmdline.txt`
- ✅ Join pi-worker2 to cluster as worker
- ✅ Verify all nodes are Ready (pi-control, pi-worker1, pi-worker2 all Ready, k3s v1.35.5)
- ✅ Migrate PostgreSQL to USB-backed storage on pi-worker1
  - PV (`postgres-pv`, 10Gi, local-storage) pointing at `/mnt/usb/postgresql`
  - PVC bound to PV
  - Node affinity pinning postgres pod to pi-worker1
  - 157 rows of historical feeding data imported (2025-12-04 to 2026-05-09)
- ✅ Deploy API and frontend across workers (2 replicas each)
  - podAntiAffinity spreads replicas across pi-worker1 and pi-worker2
  - nodeAffinity prefers workers over control plane
- ✅ Test pod scheduling and node affinity — confirmed pods spread correctly
- ✅ Experiment: Drain pi-worker2 and watched pods reschedule to pi-worker1 and pi-control with zero downtime. Uncordoned and rolled restarts to rebalance.

## Success Criteria
- ✅ 3-node cluster with all nodes Ready
- ✅ PostgreSQL runs on pi-worker1 with USB storage
- ✅ Understand how k8s schedules workloads across nodes
- ✅ Can handle node failure gracefully

## Key Learnings
- cgroups memory controller must be explicitly enabled on Raspberry Pi OS via `cmdline.txt`
- `preferred` scheduling rules are overridden by necessity — pods land on the control plane if workers are not available
- Postgres with node affinity stays put during a drain; stateless pods reschedule freely
- `kubectl drain` + `kubectl uncordon` is the clean way to simulate node failure
- pi-control runs the API server, etcd, scheduler, controller manager, Traefik, and CoreDNS — it's doing critical work even with no app pods