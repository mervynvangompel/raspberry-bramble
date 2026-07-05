# The Raspberry Bramble — Phase 3-1: The Day GitOps Ate the Dashboard

## Full writeup (for the repo / phase notes)

Today was meant to be a straightforward step in **The Raspberry Bramble** — my homelab Kubernetes project running Pippi's feeding tracker across three
Raspberry Pi nodes. The goal: add ArgoCD so the cluster manages itself declaratively instead of me typing `kubectl apply` and hoping I remembered everything.

Setting up ArgoCD itself went smoothly — dedicated namespace, trimmed resource requests to fit the Pi's 8GB, exposed at `/argocd` behind Traefik, manual sync policy so I could watch what it wanted to do before it did it.

Then I pointed it at Grafana, and things got interesting.

**The gap ArgoCD exposed:** Grafana had originally been installed via a one-off `helm install` command, months ago, never saved anywhere except my shell history. Only the *values file* was in Git — the actual install command, chart name, and version lived nowhere durable. Classic case of "works until you need to rebuild it", and the whole reason to set up ArgoCD in the first place.

**The near-miss:** An old raw Kubernetes manifest for Grafana — a leftover from before I'd switched to the Helm chart — had originally declared the
PersistentVolume and PersistentVolumeClaim holding the dashboard data. I deleted that stale file from Git during cleanup, not realizing ArgoCD was
still tracking those two storage objects. On the next sync, ArgoCD saw a PV and PVC it no longer had any record of wanting, and correctly did exactly
what I told it to: flagged them for deletion.

After my coffee break, I caught it mid-sync — both objects sitting in `Terminating` for way longer than they should have. Here's the detail that saved the day:

**The reclaim policy was `Retain`.**

In Kubernetes, when you delete a PersistentVolumeClaim, what happens to the actual data depends entirely on the PV's `persistentVolumeReclaimPolicy`.
With `Delete` (a common default for dynamically provisioned storage), the underlying files get wiped along with the Kubernetes object. With `Retain`,
Kubernetes only ever deletes its own bookkeeping — the PV/PVC *records* — and leaves the real data on disk completely alone, orphaned but intact, waiting
for someone to reattach it.

On top of that, there's a second quiet safety net: deleting a PVC's API object doesn't force an already-running pod to unmount it. The kubelet only
detaches a volume when the *pod* restarts or reschedules — not when the PVC record disappears from etcd. So even after the PVC was gone from
`kubectl get`, my Grafana pod kept humming along, still reading and writing to the same files, completely unbothered.

That gave me a safe window to:
1. Clear the stuck deletion finalizers;
2. Recreate the PV and PVC declaratively in Git (this time with an explicit `argocd.argoproj.io/sync-options: Prune=false` annotation, so this can't
   happen again);
3. Sync ArgoCD to recreate them;
4. Only *then* restart the Grafana pod, so it picked up the "new" PVC — which pointed at the exact same directory on disk the whole time.

Dashboard came back untouched. Zero data loss. Zero downtime. But it was a genuinely useful scare — the kind of lesson that's much cheaper to learn on a homelab with a dog-feeding tracker than on, say, your employers production environment.

**Bonus near-incident, same session:** ArgoCD also spun up a *second*, parallel Grafana deployment because I hadn't pinned a Helm release name — it
defaulted to naming things after the Application instead of matching my original manually-installed release. Worth knowing: ArgoCD doesn't actually
use Helm under the hood to install charts — it renders them with `helm template` and applies plain manifests, so there's no real Helm release
to `helm uninstall`, just ordinary `kubectl delete` on the stray objects. Fixed by explicitly setting `helm.releaseName` in the Application spec.

**Takeaways for the repo's learnings file:**
- Never delete a manifest from Git without checking whether ArgoCD is currently tracking the resources it declares
- Always pin `Prune=false` on any storage object ArgoCD manages
- Always pin an explicit Helm `releaseName` when adopting an existing manually-installed release
- `Retain` is not optional for anything you'd be upset (or annoyed) to lose
- Prefer plain "Sync" over "Sync and Replace" — Replace does a delete+recreate under the hood and can trip over immutable fields like `spec.selector`

---