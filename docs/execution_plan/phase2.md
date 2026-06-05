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
- ⬜ Deploy remaining workloads (API, Frontend) across workers
- ⬜ Test pod scheduling and node affinity
- ⬜ Experiment: Drain a node and watch pods reschedule
## Success Criteria
- ✅ 3-node cluster with all nodes Ready
- ✅ PostgreSQL runs on pi-worker1 with USB storage
- ⬜ Understand how k8s schedules workloads across nodes
- ⬜ Can handle node failure gracefully
## LinkedIn Post
"Expanded to 3-node Raspberry Pi cluster. Learned about pod scheduling, node draining, and persistent storage."