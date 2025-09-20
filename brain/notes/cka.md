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

## Inspecting Pod Resource Usage
- using Kubernetes Metrics Server
  - collects and provides metrics data
  - metric server must be installed on the cluster
  - verify by qerying its api: kubectl get --raw /apis.metrics.k8s.io/
  - this allows use of kubectl top command: kubectl top pod <options>
  - it can take a little bit of time after install of metrics server for data to start getitng returned
  - also, takes a bit for new pods to show in the data results
  - you can also see usage by node: kubectl top node

## Pods and Containers
- managing application configuration
  - application configuration - the dynamic values passed into the containers (apps )at runtime
  - config maps are a primary way to pass data to the containers (map of k:v)
  - secrets are similar, but are treated as sensitive items (map of k:v)
  - environment variables can be used to pass secrets and config maps
    ```yaml
    spec:
      containers:
      ...
      - name: ENVVAR
        valueFrom:
          configMapKeyRef:
            name: my-configmap
            key: mykey
    ```
  - configuration volumes can be used to pass secrets and config maps in the form of mounted volumes
    - this mounts a file system containing the secrets/config maps
  - environment variables example
    ```yaml
    apiVersion: v1
    kind: Pod
    metadtata:
      name: env-pod
    spec:
      containers:
      - name: busybox
        image: busybox
        command: ['sh', 'echo "configmap: $CONFIGMAPVAR secret: $SECRETVAR"']
        env:
        - name: CONFIGMAPVAR
          valueFrom:
            configMapKeyRef:
              name: my-configmap
              key: key1
        - name: SECRETVAR
          valueFrom:
            secretKeyRef:
              name: my-secret
              key: secretkey1
    ```
  - using volumes + volumeMounts for config and secrets
    ```yaml
    ...
    spec:
      containers:
      - name: busybox
        image: busybox
        command: ['sh', '-c', 'echo example']    
        volumeMounts:
        - name: configmap-volume
          mountPath: /etc/config/configmap
        - name: secret-volume
          mountPath: /etc/config/secret
      volumes:
      - name: configmap-volume
        configMap:
          name: my-configmap
      - name: secret-volume
        secret:
          secretName: my-secret
    ```
- managing container resources
  - resource requests: the scheduler investigates the available resources in a node before scheduling a pod
  - resource limits: provide a way to limit the amout of resources containers can use, behavior of how this happens deponds the the container runtime but it may actually kill stuff attemptingt to run in the container
- monitoring container health with probes
  - liveness probes allow you to automatically determine if a container app is in a healthy state
  - startup probes run at container startup and determine once a app is succesffully start
  - readiness probes determine when a container is ready to accept requests
  - exec probe example
    ```yaml
    apiVersion: v1
    kind: Pod
    metadtata:
      name: liveness-pod
    spec:
      containers:
      - name: busybox
        image: busybox
        command: ['sh', '-c', 'while true; do sleep 3600; done']
        livenessProbe:
          exec:
            command: ["echo", "Hello, world"]
          initialDelaySeconds: 5
          periodSeconds: 5
    ```
  - http get probe example
    ```yaml
    apiVersion: v1
    kind: Pod
    metadtata:
      name: liveness-pod
    spec:
      containers:
      - name: busybox
        image: busybox
        command: ['sh', '-c', 'while true; do sleep 3600; done']
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
    ```
  - startup probe example
    ```yaml
    apiVersion: v1
    kind: Pod
    metadtata:
      name: startup-pod
    spec:
      containers:
      - name: nginx
        image: nginx:1.19.1
        command: ['sh', '-c', 'while true; do sleep 3600; done']
        startupProbe:
          httpGet:
            path: /
            port: 80
          failureThreshold: 30
          periodSeconds: 10
    ```
- building self-healing pods with restart policies
  - k8s can automatically restart containers when they failure
  - restart policies allow you to customize this behavior
  - there are 3 types of restart policies: always, OnFailure, and never
    - always is the default value for container spec
- multi-container pods
  - a pod with more than one container is a multi-container pod
  - it is best practice to keep containers in separate pods unless they need to share resources
  - in a multi-container pod, the containers share resources such as network and storage
  - often, secondary containers are used in situations where an app writes to file
  - these are referred to as sidecars, as they help the primary container with something
  - sometimes ssl termination is done using a sidecar
  - example multi-container spec:
    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: multi-container-pod
    spec:
      containers:
      - name: nginx
        image: nginx
      - name: redis
        image: redis
      - name: couchbase
        image: couchbase
    ```
- introducing init containers
  - init containers are containers that run once during the startup process of a pod
  - a pod can have any number of init containers and they each run once, in order, to completion
  - useful in keeping your main containers lighter and more secure by offloading startup tasks to a separate container
  - example use cases
    - cause a pod to wait for another k8s resource to be created before finishing startup
    - perform sensitve startup steps securely outside of app contianers
    - populate data into a shared volume at startup
    - communicate with another service at startup
  - init containers are specified using a config block called initContainers

## Advanced Pod Allocation
- exploring k8s scheduling
  - the kubernetes scheduler selects a suitable node for each pod
  - it considers things like resources requests vs available node resources
  - you can customize scheduling using node labels
  - nodeSelector can be configured to limit which nodes a pod can be scheduled on
  - nodeName can be used to bypass scheduling and assign a pod to a sepcific node
- using DaemonSets
  - a daemonset automatically runs a copy of a pod on each node
  - this applies to new nodes that are created as well
  - daemonsets respect normal scheduling rules such as node labels, taints
  - example
    ```yaml
    apiVersion: apps/v1
    kind: DaemonSet
    metadata:
      name: my-daemonset
    spec:
      selector:
        matchLabels:
          app: my-daemonset
      template:
        metadata:
	  labels:
	    app: my-daemonset
	spec:
	  containers:
	  - name: nginx
	    image: nginx:1.19.1
      
    ```
- using static pods
  - a static pod is managed directly by the kubelet ona node instead of by the K8s API server
  - they get created using yaml definition files that exist on the node directly (so that the api is not needed)
  - for each static pod a mirror pod is created to do the communication with the k8s api (read only, cannot modify the pod viathe k8s api in the standard way)
  - if you attempt to delete the pod using kubectl it will only delete the mirror pod, and then the mirror pod will get recreated again
  - so, static pods are a way to have a pod that runs without a dependency on the k8s api / control plane node

## Deployments
- scaling applications with deployments
  - k8s is great at horizontal scaling (adding/removing total containers)
  - the number of pods is controlled by the Replicas parameter
  - how to scale a deployment
    - update that yaml to change the replicas value
    - kubectl scale command can be used: kubectl scale <deployment> --replicas 3
  - if yaml was updated for scaling, apply to trigger: kubectl apply -f my-deployment.yml
- managing rolling updates with deployments
  - what is a rolling udpate?
    - allow you to make changes to a deployment pods at a controlled rate, gradually replacing old pods with news pods. this allows you to update your pods without incurring downtime
  - what is a rollback?
    - if an update to a deployment causes a problem you can roll back to a previous working state
  - to see state of a deployment: kubectl rollout status deployment/my-deployment
  - you can update the underlying image: kubectl set image deployment/my-deployment nginx:nginx

## Networking
- kubernetes network model
  - a set of standards that defines how networking between pods behaves
  - each pod has its own IP address within the cluster
  - each ip address is unique within the cluster
- cni plugins overview
  - cni plugins are a type of kubernetes network plugin that provide network connectivity between pods according to the standard setby the kubernetes network model
  - the calico network plugin is common
- understanding k8s DNS
  - the kubernetes virtual network includes a dns system to allow pods to locate other pods using domain names instead of by ip
  - the dns components usually exist within the kube-system k8s namespace
  - you can see the core system components by getting pods from the kube-system namespace: kubectl get pods -n kube-system
  - this will likely show the pods running dns if a common setup is in use
  - checking dns records for a specific pod: kubectl exec <name> -- nslookup <host>
- using network policies
  - a network policy is an object that allws you to control the flow of network communication to and from pods
  - podSelectors can be used to determine which pods in a namespace should have a network policy applied
  - podSelectors use labels to select pods
    ```yaml
    podSelector:
      matchLabels:
        role: db
    ```
  - by default, pods are considered non-isolated and are open to all communication
  - if any network policy selects a pod the pod is considered isolated and will only be open to traffic allowed by NetworkPolicies
  - network policies can be applied to ingress, egress, or both directions of traffic
  - from and to selectors
    - from selects ingress traffic (incoming traffic)
    - to selects egress traffic (outgoing traffic)
  - namespaceSelector can be used to apply a rule to all pods in the namespace
    ```yaml
    spec:
      ingress:
        from:
	- namespaceSelector:
	  matchLabels:
	    app: db
    ```

## Services
- a kubernetes service provides a way to expose an application running as a set of pods
- endpoints are the backend entities to which services route traffic
  - one way to determine which pods a service is routing traffic to is to take a look at that service's endpoints
- each service has a type, and each service type determines how and where the service will expose your application
  - clusterIP, NodePort, LoadBalancer, ExternalName
- clusterIP services expose applications inside the cluster network, used when clients will be other pods within the cluster
- nodeport expose applications outside the cluster network, used when the clients/apps/users are outside the cluster
- loadbalancer expose applications outside the cluster network, used when an external load balancer are used
- example yaml for nodeport ServiceType, this exposes the app's 80 listener externally over 30080
  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
   name: svc-nodeport
  spec:
    type: NodePort
    selector:
      app: svc-example
    ports:
      - protocol: TCP
        port: 80
        targetPort: 80
        nodePort: 30080
  ```
- the kubernetes DNS assigns DNS names to services with the following format
- service-name.napespace-name.svc.cluster-domain.example
- a service's fully qualified domain name can be used to reach the service from within any namespace in the cluster
- managing access from outside the cluster
  - ingress is external clients -> ingress -> service
  - an ingress is a kubernetes object that manages external access to services in the cluster
  - ingress relies on installation of an ingress controller
  - ingresses define a set of routing rules, each rule has a set of paths
    ```yaml
    spec:
      rules:
        http:
	  paths:
	  - path: /somepath
	    pathtype: Prefix
	    backend:
	      service:
	        name: my-service
		port:
		number: 80
    ```

## K8s Storage
- the container file system is ephemeral. files on the container's file system exist only as long as the container exists.
- volumes allow you to store data outside the container file system while allowing the container to access the data at runtime
- persistent volumes allow you to treat storage as an abstract resource and consume it using your pods
- volume types: nfs, cloud storage, config maps and secrets, a simple directory on the k8s node
