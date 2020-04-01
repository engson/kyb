# vue-flask-mongo-kubernetes

This is a simple app boilerplate using a Vue.js frontend, Python Flask API, MongoDB database and kubernetes with minikube deployment.

This app is based on https://testdriven.io/blog/running-flask-on-kubernetes/

## Install dependencies

    Dependencies:
    Docker
    Kubernetes
    Minikube

Install docker: https://docs.docker.com/install/

Install kubectl: https://kubernetes.io/docs/tasks/tools/install-kubectl/

Install minikube: https://kubernetes.io/docs/tasks/tools/install-minikube/

## Get started
Clone the repository

    $ git clone https://github.ibm.com/Havard-Thom/vue-flask-mongo-kubernetes
    $ cd vue-flask-mongo-kubernetes

Start the minikube cluster and open minikube dashboard which will be useful later to get a deployment overview

    $ minikube start
    $ minikube dashboard

Before building the docker images for our applications, we want to point our terminal to the minikube docker environment.

    $ minikube docker-env
    $ eval $(minikube -p minikube docker-env)
    $ docker ps (should show minikube containers running)

Build the flask-api docker image

    $ cd flask-api
    $ docker build -t flask-api .
    $ cd ..

Build the vue-frontend docker image

    $ cd vue-frontend
    $ docker build -t vue-frontend .
    $ cd ..

To understand what we are deploying, study the deployment files in `./kubernetes` folder. There is also a more detailed description on https://testdriven.io/blog/running-flask-on-kubernetes/

Run the deploy script to deploy everything on the minikube cluster. It will try to clean up existing deployments so don't worry if there are some errors/warnings.

    $ sh deploy.sh

Check the minikube dashboard to see if everything deployed successfully. There should be three deployments and services (vue-frontend, flask-api and mongodb). There should also be a persistent volume and a persistent volume claim for mongodb storage.

To access our deployed app, we first need to update our `/etc/hosts` file to route requests from the host we have defined in `./kubernetes/minikube-ingress.yml` to the Minikube instance. The host is called `app-boilerplate`.

Add an entry to `/etc/hosts`:

    $ echo "$(minikube ip) app-boilerplate" | sudo tee -a /etc/hosts

We should now be able to open the application at `http://app-boilerplate/`

For more information on Scalability, Helpful Commands etc. see https://testdriven.io/blog/running-flask-on-kubernetes/

NB:

    Boilerplate does not include:
    Proper exception handling
    Authentication and Authorization
    DB scalability

