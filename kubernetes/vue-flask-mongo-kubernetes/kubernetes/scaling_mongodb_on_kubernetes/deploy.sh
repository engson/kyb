#!/bin/bash
echo "Deploying Mongo"
kubectl apply -f mongo.yaml

echo "Deploying mongo ingress"
minikube addons enable ingress
kubectl apply -f ingress.yaml

echo "Deploying dnsutils pod"
kubectl apply -f dnsutils.yaml
