# Notes related to the cluster management

All commands assumes the current directory is `cluster`.

## Creating the cluster

```
kind create cluster --config kind-config.yaml
kubectl cluster-info --context kind-crudite-cluster
```

Some images are stored in a private registry. To access them, generate a secret containing all credentials.
Maybe add Sealed Secrets later to commit the encrypted secret.

```
kubectl create secret docker-registry regcred --docker-server=https://index.docker.io/v1/ --docker-username=[username] --docker-password=[password] --docker-email=axel.delsol.pro@gmail.com
```


## Deploying the crudite application

```
kubectl apply -f crudite-deployment.yaml
kubectl apply -f crudite-service.yaml
```

Checking everything is fine:

```
# Terminal 1
kubectl port-forward svc/crudite-service 8080:8080
# Terminal 2 (powershell)
Invoke-WebRequest -Uri http://127.0.0.1:8080/ding
# Terminal 2 (curl)
curl http://127.0.0.1:8080/ding
```

Alternatively, apply the test-job and test-jobs-dns jobs

```
kubectl apply -f test-job.yaml
kubectl apply -f test-job-dns.yaml
```

## Deleting the cluster

```
kind delete cluster --name crudite-cluster
```