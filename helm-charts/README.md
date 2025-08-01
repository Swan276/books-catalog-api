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

Output
```
postgres-helm/values.yaml 
Pulled: registry-1.docker.io/bitnamicharts/postgresql:16.7.21
Digest: sha256:877c4002415a7fe8fa280e4361c679534c00a2a7def039d43ff429556780a2c1
NAME: books-database
LAST DEPLOYED: Fri Aug  1 13:25:48 2025
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: postgresql
CHART VERSION: 16.7.21
APP VERSION: 17.5.0

NOTICE: Starting August 28th, 2025, only a limited subset of images/charts will remain available for free. Backup will be available for some time at the 'Bitnami Legacy' repository. More info at https://github.com/bitnami/containers/issues/83267

** Please be patient while the chart is being deployed **

PostgreSQL can be accessed via port 5432 on the following DNS names from within your cluster:

    books-database-postgresql.default.svc.cluster.local - Read/Write connection

To get the password for "postgres" run:

    export POSTGRES_ADMIN_PASSWORD=$(kubectl get secret --namespace default books-database-postgresql -o jsonpath="{.data.postgres-password}" | base64 -d)

To get the password for "books" run:

    export POSTGRES_PASSWORD=$(kubectl get secret --namespace default books-database-postgresql -o jsonpath="{.data.password}" | base64 -d)

To connect to your database run the following command:

    kubectl run books-database-postgresql-client --rm --tty -i --restart='Never' --namespace default --image docker.io/bitnami/postgresql:17.5.0-debian-12-r20 --env="PGPASSWORD=$POSTGRES_PASSWORD" \
      --command -- psql --host books-database-postgresql -U books -d books -p 5432

    > NOTE: If you access the container using bash, make sure that you execute "/opt/bitnami/scripts/postgresql/entrypoint.sh /bin/bash" in order to avoid the error "psql: local user with ID 1001} does not exist"

To connect to your database from outside the cluster execute the following commands:

    kubectl port-forward --namespace default svc/books-database-postgresql 5432:5432 &
    PGPASSWORD="$POSTGRES_PASSWORD" psql --host 127.0.0.1 -U books -d books -p 5432

WARNING: The configured password will be ignored on new installation in case when previous PostgreSQL release was deleted through the helm command. In that case, old PVC will have an old password, and setting it through helm won't take effect. Deleting persistent volumes (PVs) will solve the issue.

WARNING: There are "resources" sections in the chart not set. Using "resourcesPreset" is not recommended for production. For production installations, please set the following values according to your workload needs:
  - primary.resources
  - readReplicas.resources
+info https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
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

Testing postgres
```
kubectl run books-database-postgresql-client --rm --tty -i --restart='Never' --namespace default --image docker.io/bitnami/postgresql:17.5.0-debian-12-r20 --env="PGPASSWORD=books" \
      --command -- psql --host books-database-postgresql -U books -d books -p 5432
```

No tables as migration is not run yet.
```
books=> SELECT *
books-> FROM pg_catalog.pg_tables
books-> WHERE schemaname != 'pg_catalog' AND
books->     schemaname != 'information_schema';
 schemaname | tablename | tableowner | tablespace | hasindexes | hasrules | hastriggers | rowsecurity 
------------+-----------+------------+------------+------------+----------+-------------+-------------
(0 rows)
```
