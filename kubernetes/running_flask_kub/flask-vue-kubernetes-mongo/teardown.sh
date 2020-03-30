#!/bin/bash


echo "Deleting the volume..."

kubectl delete -f ./kubernetes/persistent-volume.yml
kubectl delete -f ./kubernetes/persistent-volume-claim.yml


echo "Deleting the database credentials..."

kubectl delete -f ./kubernetes/secret.yml


echo "Deleting the postgres deployment and service..."

kubectl delete -f ./kubernetes/postgres-deployment.yml
kubectl delete -f ./kubernetes/postgres-service.yml



echo "Deleting the flask deployment and service..."

kubectl delete -f ./kubernetes/flask-deployment.yml
kubectl delete -f ./kubernetes/flask-service.yml


echo "Deleting the ingress..."

kubectl delete -f ./kubernetes/minikube-ingress.yml


echo "Deleting the vue deployment and service..."

kubectl delete -f ./kubernetes/vue-deployment.yml
kubectl delete -f ./kubernetes/vue-service.yml