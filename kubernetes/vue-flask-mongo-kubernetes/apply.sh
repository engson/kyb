#!/bin/bash

echo "Creating the mongodb deployment and services..."
    
kubectl apply -f ./kubernetes/scaling_mongodb_on_kubernetes/mongo.yaml

echo "Creating the flask-api deployment and service..."

kubectl apply -f ./kubernetes/flask-api.yml

echo "Adding the ingress..."

minikube addons enable ingress
kubectl apply -f ./kubernetes/app-ingress.yml

echo "Creating the vue-frontend deployment and service..."

kubectl apply -f ./kubernetes/vue-frontend.yml

echo "Deploying dnsutils pod"

kubectl apply -f ./kubernetes/scaling_mongodb_on_kubernetes/dnsutils.yaml