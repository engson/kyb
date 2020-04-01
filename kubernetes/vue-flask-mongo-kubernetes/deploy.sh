#!/bin/bash

echo "Creating the persistent volume..."

kubectl apply -f ./kubernetes/persistent-volume.yml
kubectl apply -f ./kubernetes/persistent-volume-claim.yml

echo "Creating the mongodb deployment and service..."

kubectl delete -n default deployment mongodb
kubectl create -f ./kubernetes/mongodb-deployment.yml
kubectl delete -n default service mongodb
kubectl create -f ./kubernetes/mongodb-service.yml

echo "Creating the flask-api deployment and service..."

kubectl delete -n default deployment flask-api
kubectl create -f ./kubernetes/flask-api-deployment.yml
kubectl delete -n default service flask-api
kubectl create -f ./kubernetes/flask-api-service.yml

echo "Adding the ingress..."

minikube addons enable ingress
kubectl apply -f ./kubernetes/minikube-ingress.yml


echo "Creating the vue-frontend deployment and service..."

kubectl delete -n default deployment vue-frontend
kubectl create -f ./kubernetes/vue-frontend-deployment.yml
kubectl delete -n default service vue-frontend
kubectl create -f ./kubernetes/vue-frontend-service.yml