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

**Remember:** The goal is learning, not perfection. 🫐🚀