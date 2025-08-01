# Deployment Steps

## Creating Kubernetes Cluster

Cmd
```
k3d cluster create books-cluster --port "8081:80@loadbalancer" --port "8443:443@loadbalancer" --port "30000-30010:30000-30010@server:0"
```
Output
```
INFO[0000] portmapping '8081:80' targets the loadbalancer: defaulting to [servers:*:proxy agents:*:proxy] 
INFO[0000] portmapping '8443:443' targets the loadbalancer: defaulting to [servers:*:proxy agents:*:proxy] 
INFO[0000] Prep: Network                                
INFO[0000] Created network 'k3d-books-cluster'          
INFO[0000] Created image volume k3d-books-cluster-images 
INFO[0000] Starting new tools node...                   
INFO[0000] Starting node 'k3d-books-cluster-tools'      
INFO[0001] Creating node 'k3d-books-cluster-server-0'   
INFO[0001] Creating LoadBalancer 'k3d-books-cluster-serverlb' 
INFO[0001] Using the k3d-tools node to gather environment information 
INFO[0001] Starting new tools node...                   
INFO[0001] Starting node 'k3d-books-cluster-tools'      
INFO[0002] Starting cluster 'books-cluster'             
INFO[0002] Starting servers...                          
INFO[0002] Starting node 'k3d-books-cluster-server-0'   
INFO[0005] All agents already running.                  
INFO[0005] Starting helpers...                          
INFO[0005] Starting node 'k3d-books-cluster-serverlb'   
INFO[0011] Injecting records for hostAliases (incl. host.k3d.internal) and for 3 network members into CoreDNS configmap... 
INFO[0013] Cluster 'books-cluster' created successfully! 
INFO[0013] You can now use it like this:                
kubectl cluster-info
```

## Installing Posgres Helm Chart

```
helm install books-database oci://registry-1.docker.io/bitnamicharts/postgresql -f ./postgres-helm/values.yaml
```

```
kubectl get secrets books-database-postgresql -o yaml
```

Output
```
apiVersion: v1
data:
  password: Ym9va3M=
  postgres-password: ZTViV0h1MTJwWg==
kind: Secret
metadata:
  annotations:
    meta.helm.sh/release-name: books-database
    meta.helm.sh/release-namespace: default
  creationTimestamp: "2025-08-01T12:25:48Z"
  labels:
    app.kubernetes.io/instance: books-database
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: postgresql
    app.kubernetes.io/version: 17.5.0
    helm.sh/chart: postgresql-16.7.21
  name: books-database-postgresql
  namespace: default
  resourceVersion: "816"
  uid: b5dfb85e-32bc-489b-9e40-e941f3af1001
type: Opaque
```