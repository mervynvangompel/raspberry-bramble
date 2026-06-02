# 🫐 The Raspberry Bramble

A Kubernetes homelab project running on Raspberry Pis to track dog feeding habits (and learn a thing or two about Kubernetes, networking, DB's, Terraform and infra as a whole).

## What is this?

A hands-on learning project that combines:
- **Kubernetes** cluster on Raspberry Pi hardware
- **Dog food tracker** web application
- **Real-world DevOps** practices

Because the best way to learn infrastructure is to build something you'll actually use.

## The Stack

- **Infrastructure:** 3x Raspberry Pi nodes running k3s
- **Backend:** Python FastAPI
- **Frontend:** HTML/JS served by Nginx
- **Database:** PostgreSQL with persistent storage
- **Monitoring:** Grafana dashboards
- **Orchestration:** Kubernetes (k3s)

## Why?

This project is overkill for tracking dog food. That's the point.

It's a realistic, production-like environment to learn:
- Kubernetes cluster management
- Container orchestration
- Persistent storage
- Service networking and ingress
- Monitoring and observability
- Infrastructure as code

All while solving a real (well...) problem: keeping track of how much Pippi (our bestest girl) eats every day.

## Project Status

🚧 **Work in Progress**

- [x] POC built and tested locally
- [x] Raspberry Pi hardware prepared
- [ ] Single-node k3s deployment
- [ ] Three-node cluster
- [ ] Grafana dashboards
- [ ] Public access via Cloudflare Tunnel

## Documentation

- [**Architecture & Execution Plan**](docs/architecture.md) - Detailed technical plan
- [**Pi Setup Procedure**](docs/pi-setup.md) - Step-by-step Pi configuration
- [**Troubleshooting**](docs/troubleshooting.md) - Common issues and solutions (unless everything works straight away, right?)

## Quick Start

**For the impatient:**

```bash
# Clone the repo
git clone https://github.com/mervynvangompel/raspberry-bramble.git
cd raspberry-bramble

# See detailed setup instructions
cat docs/pi-setup.md
cat docs/architecture.md
```

## Learning Outcomes

By the end of this project:
- Deploy and manage a multi-node Kubernetes cluster
- Run stateful applications in Kubernetes
- Configure networking, ingress, and load balancing
- Implement persistent storage strategies
- Monitor applications with Grafana
- Apply infrastructure as code practices

## Tech Deep Dive

**Kubernetes (k3s):**
- Lightweight Kubernetes for ARM devices
- Built-in Traefik ingress controller
- 3-node cluster (1 control plane, 2 workers)

**Application:**
- FastAPI backend with PostgreSQL
- Simple web UI for data entry
- REST API for CRUD operations

**Storage:**
- USB-backed persistent volumes
- Local-path provisioner
- Future: Longhorn distributed storage

**Networking:**
- Static IPs for cluster nodes
- Traefik ingress for HTTP routing
- Internal cluster DNS

## The Name

**Bramble** = a prickly shrub (like a raspberry bush) 🫐

Also: a cluster of raspberry plants growing together, which seemed fitting for a Raspberry Pi cluster.

## License

MIT

---

**Note:** This is a learning project. I by no means guarantee this will work for you, or won't need extensive troubleshooting! Use at your own risk, and have fun learning! 🚀
