#!/bin/bash
# All deletes based on labels used. Must be unique for each kind.
echo "Delete mongo database"

kubectl delete -f ./kubernetes/scaling_mongodb_on_kubernetes/mongo.yaml

echo "Deleting pv and pvc of mongo database"

kubectl delete pv,pvc -l role=mongo

echo "Deleting the flask-api deployment and service..."

kubectl delete service -l service=flask-api
kubectl delete deployment -l name=flask-api

echo "Disabling the ingress..."

kubectl delete ingress -l name=app-ingress
minikube addons disable ingress

echo "Deleting the vue-frontend deployment and service..."

kubectl delete deployment -l name=vue-frontend
kubectl delete service -l service=vue-frontend

echo "Deleting dnsutils"
kubectl delete pod -l name=dnsutils