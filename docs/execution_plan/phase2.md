# Phase 2 — Expand to Three-Node Cluster
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
