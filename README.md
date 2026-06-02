# 🫐 The Raspberry Bramble

A concise, visitor-friendly overview of the Raspberry Pi Kubernetes homelab and the dog-food tracker application.

Quick highlights:
- Kubernetes on Raspberry Pi (k3s)
- FastAPI backend, Nginx frontend
- PostgreSQL for persistence, Grafana for observability

Project status:
- Phase 0 complete: Raspberry Pi hardware prepared
- POC built and tested locally
- Next: single-node k3s deployment → expand to 3 nodes → add monitoring

Docs and next steps:
- Phase 0 retrospective: [docs/linkedin/phase0.md](docs/linkedin/phase0.md)
- Architecture & detailed plan: [docs/architecture.md](docs/architecture.md)
- Execution plan: [docs/execution_plan.md](docs/execution_plan.md)
- Pi setup & troubleshooting: [docs/pi_setup.md](docs/pi_setup.md) and [docs/troubleshooting.md](docs/troubleshooting.md)

Quick start:
```bash
git clone https://github.com/mervynvangompel/raspberry-bramble.git
cd raspberry-bramble
cat docs/pi_setup.md
```

This README is intentionally brief — for detailed design, execution steps, and retrospectives, see the `docs/` folder.

---

_This is a learning project. Use at your own risk and enjoy the process!_
