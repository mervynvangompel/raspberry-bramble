# ArgoCD — Bootstrap Notes

ArgoCD manages the Bramble workloads (`bramble-app`, `bramble-observability`) declaratively,
but ArgoCD itself can't manage its own installation — this is the one deliberately
imperative piece of the cluster, documented here so a rebuild doesn't lose it.

## Prerequisites

Add the Argo Helm repo (one-time, per management machine):
```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
```

## Install order

1. Create the namespace (declarative, applied like any other manifest):
```bash
   k apply -f namespace.yaml
```

2. Install ArgoCD via Helm (imperative — this command is the source of truth,
   since Helm doesn't record *how* a release was installed anywhere in Git):
```bash
   helm install argocd argo/argo-cd --version 10.1.2 -n argocd -f argocd-values.yaml
```

3. Apply the ingress route:
```bash
   k apply -f ingress-argocd.yaml
```

## Access

UI: `http://192.168.68.11/argocd`

Initial admin password:
```bash
k -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

**Rotate this after first login** — either via the UI (User Info) or:
```bash
argocd account update-password
```

## Notes / gotchas

- `server.insecure: true` is set in `argocd-values.yaml` because Traefik terminates
  on plain HTTP (entrypoint `web`) — without this, ArgoCD's server enforces its own
  TLS redirect and the UI won't load correctly behind the ingress.
- `server.basehref` / `server.rootpath` are set to `/argocd` — same lesson learned
  from Grafana: the app needs to know its own subpath internally. **Do not** add a
  Traefik strip-prefix middleware for this route, it caused redirect loops with
  Grafana and would do the same here.
- `dex` and `notifications` are disabled — unnecessary for a single-user homelab
  setup; re-enable if SSO or alerting integrations are ever needed.
- `applicationSet` is left enabled (resources trimmed) in case an App-of-Apps
  pattern is adopted later.
- Resource requests/limits across all components are trimmed down from chart
  defaults, which assume a larger cluster than 3x Raspberry Pi 5 (8GB).

## Upgrading

Since the install is imperative, upgrades must also be run manually and this file
updated to reflect the new pinned version:
```bash
helm upgrade argocd argo/argo-cd --version <new-version> -n argocd -f argocd-values.yaml
```