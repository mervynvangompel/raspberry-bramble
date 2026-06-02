## Repo Structure
```
raspberry-bramble/
├── README.md           # Project entry (visitor-facing)
├── docs/               # Documentation and design notes
│   ├── architecture.md
│   ├── branchnaming.md
│   ├── execution_plan.md
│   ├── pi_setup.md
│   ├── repo_structure.md
│   └── troubleshooting.md
│   └── linkedin/       # LinkedIn posts + retrospectives
│       ├── phase0.md
│       └── retrospectives/
│           └── phase0.md
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
├── PoC/                # Proof-of-concept artifacts (manifests, Dockerfile, nginx etc.)
├── terraform/          # IaC (future/Phase 5)
├── infra/              # Infra configs
├── images/             # Screenshots for LinkedIn and docs
└── scripts/            # Helper scripts (prepare_pi.sh, etc.)
```