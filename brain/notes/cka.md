## k8s architecture
- control plane
  - the control plane is a collection of components that manage the cluster
  - usually run on a dedicated machine
  - kube-api-server serves the Kubernetes API
  - etcd is the backend data store for the cluster
  - kube-scheduler handles scheduling, assigning containers to nodes
  - kube-controller-manager manages the utilities in a single process
  - cloud-controller-manager provides an interface between K8s and cloud platforms
- nodes
  - kubelet is an agent that runs on each node, also reports container status and info
  - container runtime, not built into k8s, but multiple kinds are supported for use (like docker, containerd)
  - kube proxy is a network proxy, runs on each node and does networking

## Commands
- use -n to return results from a single namespace: kubectl get pods -n example-namespace
- use --all-namespaces to return results from all namespaces: kubectl get pods --all-namespaces