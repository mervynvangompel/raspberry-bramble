# Updating the Bramble Frontend

## 1. Edit the frontend

Make your changes to `~/Desktop/bramble/app/index.html`.

## 2. Build and push the Docker image

```bash
cd ~/Desktop/bramble/app
docker buildx build --platform linux/arm64 -f Dockerfile.frontend -t mervynvg/bramble-frontend:latest --push .
```

> Note: if you get an `exec format error`, QEMU isn't set up. Fix with:
> ```bash
> docker run --privileged --rm tonistiigi/binfmt --install all
> ```
> Then retry the build.

## 3. Restart the deployment

```bash
kubectl rollout restart deployment/dog-feeding-frontend
```

## 4. Watch the rollout

```bash
kubectl rollout status deployment/dog-feeding-frontend
```

Once complete, the new frontend is live at **http://192.168.68.11**.

---

### Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `ImagePullBackOff` | Wrong platform / image not pushed | Check build used `-f Dockerfile.frontend` and `--push` |
| Container crash / `BackOff` | Built API image instead of frontend | Make sure you used `-f Dockerfile.frontend` |
| "No available server" | Pod still restarting | Wait and re-check `kubectl get pods` |