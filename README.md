# CRUDITE

This is a multi steps project used to learn Go and Kubernetes.
The main goal is to be able to develop a simple CRUD API and deploy it on a Kubernetes cluster using Kind.

Progress:

* [x] Build the API
* [x] Create a kubernetes cluster
* [ ] Add CRUD routes (API update)
* [ ] Deploy the API (cluster update)


## Step 1 - Build the API

* Build an API with Go responding to the route GET /ding and returning "Dong !"
* Add unit tests for the handler
* Setup CI/CD
    * On any push, execute unit tests
    * On release (with tag v*), build and push a docker image on a private dockerhub registry

## Step 2 - Create a kubernetes cluster

* Setup kind to create a cluster and authenticate to the registry
* Deploy the API on the cluster
* Being able to use the /ding route from the browser (using port forwarding)

## Step 3 - Add CRUD routes (API update)

* Save users in a persistent way (probably postgresql)
* Setup migrations
* Update the API to add basic CRUD routes

## Step 4 - Deploy the API (cluster update)

* Add dabatase management inside the cluster
* Deploy the new API on the cluster
