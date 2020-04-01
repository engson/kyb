#!/bin/bash

echo "Creating the volume..."

kubectl delete -f ./kubernetes/persistent-volume-claim.yml

echo "Creating the database credentials..."

kubectl delete -f ./kubernetes/secret.yml

echo "Creating the postgres deployment and service..."

kubectl delete -f ./kubernetes/postgres-deployment.yml
kubectl delete -f ./kubernetes/postgres-service.yml

echo "Creating the flask deployment and service..."

kubectl delete -f ./kubernetes/flask-deployment.yml
kubectl delete -f ./kubernetes/flask-service.yml

echo "Adding the ingress..."

kubectl delete -f ./kubernetes/minikube-ingress.yml

echo "Creating the vue deployment and service..."

kubectl delete -f ./kubernetes/vue-deployment.yml
kubectl delete -f ./kubernetes/vue-service.yml
