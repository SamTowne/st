## Kubernetes architecture
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
- to see which node each pod is running on: kubectl get pods -o wide

## Kubernetes Management
- high availability, multiple instances of control plane
  - control plane and worker nodes often use a lb
  - stacked etcd design pattern: control plane nodes run etcd
  - external etcd design pattern: dedicated nodes for etcd 
- management tools
  - kubectl, official cli
  - kubeadm
  - minikube
  - helm, templating (charts) and package mgmt
  - kompose, for transitioning docker compose to kube objs
  - kustomize, configuration management, templated configs for apps
- safely draining a k8s node: kubectl drain <node name>
  - use the --ignore-daemonsets flag if they are in use on the node
  - after maintenence on the node is complete, use uncordon to tell k8s it is ready: kubectl uncordon <node name>
- upgrading kubernetes with kubeadm (one node at a time to keep from downtime when HA is configured)
  - upgrade the control plane nodes
    - drain the node: kubectl drain <node name> --ignore-daemonsets
    - upgrade kubeadm: sudo apt-get update && sudo apt-get install -y --allow-change-held-packages kubeadm=1.22.2-00
    - upgrade internal components using the new kubeadm version
      - use plan to see changes: sudo kubeadm upgrade plan v1.22.2
      - use apply to upgrade: sudo kubeadm upgrade apply v1.22.2
    - upgrade kubelet & kubectl: sudo apt-get update && sudo apt-get install -y --allow-change-held-packages kubelet=1.22.2-00 kubectl=1.22.2-00
      - sudo systemctl daemon-reload
      - sudo systemctl restart kubelet
    - upgrade the kubelet configuration: kubeadm upgrade node
    - uncordon the node
  - upgrade the worker nodes
    - from the control plane node, drain the worker node: kubectl draing <node name> --ignore-daemonsets # --force may be necessary
    - from the worker node, do upgrade steps
    - upgrade kubeadm: sudo apt-get update && sudo apt-get install -y --allow-change-held-packages kubeadm=1.22.2-00
    - sudo kubeadm upgrade node
    - upgrade kubelet & kubectl: sudo apt-get update && sudo apt-get install -y --allow-change-held-packages kubelet=1.22.2-00 kubectl=1.22.2-00
      - sudo systemctl daemon-reload
      - sudo systemctl restart kubelet
    - from the control plane node, uncordon the node: kubectl uncordon <node name>
- backup and restore for etcd cluster data
  - backup etcd using etcdctl: etcdctl --endpoints <endpoint> snapshot save <file name>
  - restore etcd from backup: etcdctl snapshot restore <file name>
  - the restore command spins up a new cluster

## Working with kubectl
- retrieve an obj: kubectl get <object type> <object name> -o <output format> --sort-by <JSON Path>
- obj details: kubectl describe
- creating objects: kubectl create
- create or modify: kubectl apply
- destroy: kubectl delete
- run commands inside containers: kubectl exec <pod name> -c <container name>
- declarative commands: object defined in data structure like yaml or json
- imperative commands: object defined using kubectl commands with a lot of flags for params
  - using imperative command to get boilerplate config for a deployment: kubectl create deployment my-deployment --image=nginx --dry-run -o yaml
  - use the --record flag to add a modification record to an object, the command gets added to the annotation section of the object's metadata as a change-cause record

## Role Based Access Control (RBAC)
- RBAC allows you to control what users are allowed to do and access within the cluster
- RBAC Objects
  - 4 main objects
    - Role: defines permissions within a particular namespace
    - RoleBinding: binds a Role definition to an id or user
    - ClusterRole: defines cluster-wide permissions not specific to a single namespace
    - ClusterRoleBinding: binds a ClusterRole to an id or user
  - permissions are strictly additive (there are no "deny" rules)
  - this role example provides read access to the pods and logs in the default namespace
    ```yaml
    apiVersion: rbac.authorization.k8s.io/vi
    kind: Role
    metadata:
      namespace: default
      name: pod-reader
    rules:
    - apiGroups: [""]
      resources: ["pods", "pods/log"]
      verbs: ["get", "watch", "list"]
    ```
  - the RoleBinding for this role
  - attaches the permission set from the role to the dev User
    ```yaml
    apiVersion: rbac.authorization.k8s.io/vi
    kind: RoleBinding
    metadata:
      name: pod-reader
      namespace: default
    subjects:
    - kind: User
      name: dev
      apiGroup: rbac.authorization.k8s.io
    roleRef:
      kind: Role
      name: pod-reader
      apiGroup: rbac.authorization.k8s.io
    ```
  - this ClusterRole policy grants read access to secrets in any particular namespace
  - this would be an example of something that would most likely need strict binding restrictions
    ```yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRole
    metadata:
      # "namespace" omitted because ClusterRoles are not namespaced
      name: secret-reader
    rules:
    - apiGroups: [""]
      resources: ["secrets"]
      verbs: ["get", "watch", "list"]
    ```
- service accounts
  - service accounts are for the roles that get used by the services within the cluster
  - yaml definition example
    ```yaml
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: my-serviceaccount
    ```
  - access control is handled using the standard RBAC process of defining and binding roles to the ServiceAccount