# Phase 1 — Single-Node k3s Deployment
**Goal:** Get the POC application running on ONE Raspberry Pi to prove everything works

**Why start with one node?**
- Simpler troubleshooting (fewer moving parts)
- Faster iteration
- Builds confidence before adding complexity
- Learn k3s basics without cluster coordination issues

## Registry Decision: Public DockerHub
- **Why DockerHub?** Zero setup overhead, simpler k3s config, all Raspi resources for the app
- **Public vs Private?** Starting with public—less config, easier iteration. Can switch to private later.
- **Repo naming:** `mervynvg/bramble-api` and `mervynvg/bramble-frontend`

## Deployment Order (Dependencies Matter)
1. **PostgreSQL** — Database must be ready first (other services depend on it)
2. **API** — Backend service (frontend will call it)
3. **Frontend** — Web UI
4. **Ingress (Traefik)** — Route external traffic to frontend

## Detailed Tasks

### 1. Install k3s on pi-control ✅
k3s was already installed (v1.35.5+k3s1) from a previous experiment.

**Fix kubectl permissions (no sudo required):**
```bash
mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown mervyn:mervyn ~/.kube/config
export KUBECONFIG=~/.kube/config
echo 'export KUBECONFIG=~/.kube/config' >> ~/.bashrc
source ~/.bashrc
```
> **Note:** k3s's kubeconfig at `/etc/rancher/k3s/k3s.yaml` is root-owned by default. If you see `permission denied` without sudo, this is why. If you upgrade or reinstall k3s, repeat the `cp` and `chown` steps.

### 2. Copy kubeconfig to Ubuntu desktop ✅
Run from mervyn-ubuntu:
```bash
mkdir -p ~/.kube
scp mervyn@192.168.68.11:/home/mervyn/.kube/config ~/.kube/config
sed -i 's/127.0.0.1/192.168.68.11/' ~/.kube/config
echo 'export KUBECONFIG=~/.kube/config' >> ~/.bashrc
source ~/.bashrc
```
> **Note:** The kubeconfig defaults to `127.0.0.1` which only works on the Pi itself. The `sed` command updates it to the Pi's network IP so kubectl works from the desktop.

### 3. Verify cluster health ✅
```bash
kubectl get nodes          # pi-control should show Ready
kubectl get pods -A        # all system pods should be Running or Completed
kubectl cluster-info
```

**Expected healthy pods:**
- `coredns` — Running
- `traefik` — Running (ingress controller, bundled with k3s)
- `local-path-provisioner` — Running (handles persistent storage)
- `metrics-server` — Running
- `helm-install-traefik*` — Completed (one-off jobs, correct)
- `svclb-traefik*` — Running

### 4. Deploy test nginx workload ✅
```bash
kubectl create deployment nginx --image=nginx
kubectl expose deployment nginx --port=80 --type=ClusterIP
kubectl get pods -w
kubectl port-forward deployment/nginx 8080:80
# test: http://localhost:8080/
kubectl delete deployment nginx
kubectl delete service nginx
```

### 5. Build and push Docker images to public DockerHub ✅
The PoC was built on an Ubuntu desktop (x86_64) but the Pis are ARM64, so images must be built on the Pi itself.

**Install Docker on pi-control:**
```bash
sudo apt install -y docker.io
sudo usermod -aG docker "$USER"
# log out and back in for group change to take effect
```

**Build and push:**
```bash
cd /home/mervyn/bramble/PoC
docker build -t mervynvg/bramble-api:latest -f Dockerfile .
docker push mervynvg/bramble-api:latest

docker build -t mervynvg/bramble-frontend:latest -f Dockerfile.frontend .
docker push mervynvg/bramble-frontend:latest
```

> **Note:** Images must be separate per component (api and frontend). Each has its own Dockerfile:
> - `Dockerfile` → Python/FastAPI API on port 8000
> - `Dockerfile.frontend` → nginx serving index.html on port 80

### 6. Update image references in k8s manifests ✅
In `api.yaml` and `frontend.yaml`, update image and pull policy:
```yaml
image: mervynvg/bramble-api:latest   # or bramble-frontend
imagePullPolicy: Always               # was: Never
```

### 7. Deploy PostgreSQL, API and Frontend ✅
Apply in dependency order from mervyn-ubuntu:
```bash
kubectl apply -f postgres.yaml
kubectl apply -f api.yaml
kubectl apply -f frontend.yaml
kubectl get pods -w
```
All three pods should reach `Running`. API may restart once or twice while waiting for postgres — this is normal.

### 8. Configure Ingress (Traefik) ✅
Traefik is bundled with k3s and already running. We just need an Ingress resource to route traffic.

**Gotcha: path prefix stripping**
The frontend calls the API at `/api/feedings`, but the API itself only knows about `/feedings`. Traefik must strip the `/api` prefix before forwarding to the API. This requires a Middleware resource.

`infra/ingress.yaml`:
```yaml
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: strip-api-prefix
  namespace: default
spec:
  stripPrefix:
    prefixes:
      - /api
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: dog-feeding-ingress
  namespace: default
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: web
    traefik.ingress.kubernetes.io/router.middlewares: default-strip-api-prefix@kubernetescrd
spec:
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: dog-feeding-frontend
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: dog-feeding-api
            port:
              number: 8000
```

```bash
kubectl apply -f ingress.yaml
```

> **Note:** The middleware annotation follows the pattern `namespace-middlewarename@kubernetescrd`, hence `default-strip-api-prefix@kubernetescrd`. The app is then accessible at `http://192.168.68.11` with no port-forwarding.

### 9. Test end-to-end ✅
Open `http://192.168.68.11` in browser on mervyn-ubuntu — no port-forwarding needed.
- Page loads ✅
- Feeding entry records and persists ✅

See the data in the db:
```bash
kubectl exec -it deployment/postgres -- psql -U postgres -d dogfeeding
SELECT * FROM feedings;
```
> **Note:** If you see the nginx default page, do a hard refresh (Ctrl+Shift+R) — the browser may have cached it.

## Progress Summary

| Task | Status |
|------|--------|
| k3s installed and healthy on pi-control | ✅ |
| kubectl working without sudo | ✅ |
| kubeconfig copied to mervyn-ubuntu | ✅ |
| All system pods healthy | ✅ |
| Test nginx deployment verified | ✅ |
| Docker images built for ARM64 and pushed to DockerHub | ✅ |
| Manifests updated with DockerHub image refs | ✅ |
| PostgreSQL deployed with PVC | ✅ |
| API deployed | ✅ |
| Frontend deployed | ✅ |
| Ingress (Traefik) configured with path prefix stripping | ✅ |
| App accessible without port-forward at http://192.168.68.11 | ✅ |
| End-to-end test passed (feeding entry persists) | ✅ |

## Success Criteria
- ✅ Can access dog feeding tracker from browser on Ubuntu desktop
- ✅ Can add feeding entries and see them persist
- ✅ Understand how Deployments, Services, and Ingress work