# Deployment Steps

## Creating Kubernetes Cluster

```sh
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

```sh
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

```sh
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

### Testing postgres
```sh
kubectl run books-database-postgresql-client --rm --tty -i --restart='Never' --namespace default --image docker.io/bitnami/postgresql:17.5.0-debian-12-r20 --env="PGPASSWORD=books" \
      --command -- psql --host books-database-postgresql -U books -d books -p 5432
```

```sh
books=> SELECT *
books-> FROM pg_catalog.pg_tables
books-> WHERE schemaname != 'pg_catalog' AND
books->     schemaname != 'information_schema';
 schemaname | tablename | tableowner | tablespace | hasindexes | hasrules | hastriggers | rowsecurity 
------------+-----------+------------+------------+------------+----------+-------------+-------------
(0 rows)
```
No tables as migration is not run yet.

## Configuring Image Pull Secret
```sh
kubectl create secret docker-registry ghcr-token \
    --docker-username=<your_github_username> \
    --docker-password=<your_token> \
    --docker-server=ghcr.io
```

### Check secrets
```sh
kubectl get secrets
```
Output
```
NAME                                   TYPE                             DATA   AGE
books-database-postgresql              Opaque                           2      140m
ghcr-token                             kubernetes.io/dockerconfigjson   1      18s
sh.helm.release.v1.books-database.v1   helm.sh/release.v1               1      140m
```

## Install Book Catalog Helm Chart
### Check Chart Template in YAML
```sh
helm template books-api ./book-catalog-chart
```

### Install Chart
```sh
helm install books-api book-catalog-chart/.
```

### See resources
```sh
kubectl get all
```
Output
```
NAME                                               READY   STATUS      RESTARTS   AGE
pod/books-api-book-catalog-chart-dcb559684-9tcxs   1/1     Running     0          4m33s
pod/books-api-book-catalog-chart-dcb559684-gfpc7   1/1     Running     0          4m33s
pod/books-api-book-catalog-chart-dcb559684-jqs4h   1/1     Running     0          4m33s
pod/books-api-migrate-kjd7f                        0/1     Completed   0          4m36s
pod/books-database-postgresql-0                    1/1     Running     0          3h30m

NAME                                   TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
service/books-api-book-catalog-chart   ClusterIP   10.43.93.42    <none>        80/TCP     4m33s
service/books-database-postgresql      ClusterIP   10.43.112.16   <none>        5432/TCP   3h30m
service/books-database-postgresql-hl   ClusterIP   None           <none>        5432/TCP   3h30m
service/kubernetes                     ClusterIP   10.43.0.1      <none>        443/TCP    3h38m

NAME                                           READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/books-api-book-catalog-chart   3/3     3            3           4m33s

NAME                                                     DESIRED   CURRENT   READY   AGE
replicaset.apps/books-api-book-catalog-chart-dcb559684   3         3         3       4m33s

NAME                                         READY   AGE
statefulset.apps/books-database-postgresql   1/1     3h30m

NAME                          STATUS     COMPLETIONS   DURATION   AGE
job.batch/books-api-migrate   Complete   1/1           3s         4m36s
```

### Migration pod logs
```sh
kubectl logs pod/<name of the migration pod>
```
Output
```
Operations to perform:
  Apply all migrations: admin, api, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying api.0001_initial... OK
  Applying api.0002_rename_publisheddate_book_published_date_and_more... OK
  Applying api.0003_book_id_alter_book_isbn... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
```

### Testing Postgres Database after migration
```sh
kubectl run books-database-postgresql-client --rm --tty -i --restart='Never' --namespace default --image docker.io/bitnami/postgresql:17.5.0-debian-12-r20 --env="PGPASSWORD=books" \
      --command -- psql --host books-database-postgresql -U books -d books -p 5432
```

```sh
books=> SELECT *
books-> FROM pg_catalog.pg_tables
books-> WHERE schemaname != 'pg_catalog' AND
books->     schemaname != 'information_schema';
 schemaname |         tablename          | tableowner | tablespace | hasindexes | hasrules | hastriggers | rowsecurity 
------------+----------------------------+------------+------------+------------+----------+-------------+-------------
 public     | django_migrations          | books      |            | t          | f        | f           | f
 public     | django_content_type        | books      |            | t          | f        | t           | f
 public     | auth_permission            | books      |            | t          | f        | t           | f
 public     | auth_group                 | books      |            | t          | f        | t           | f
 public     | auth_group_permissions     | books      |            | t          | f        | t           | f
 public     | auth_user                  | books      |            | t          | f        | t           | f
 public     | auth_user_groups           | books      |            | t          | f        | t           | f
 public     | auth_user_user_permissions | books      |            | t          | f        | t           | f
 public     | django_admin_log           | books      |            | t          | f        | t           | f
 public     | api_book                   | books      |            | t          | f        | f           | f
 public     | django_session             | books      |            | t          | f        | f           | f
(11 rows)
```