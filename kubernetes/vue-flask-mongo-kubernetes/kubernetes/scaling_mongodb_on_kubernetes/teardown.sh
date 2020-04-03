#!/bin/bash
kubectl delete -f mongo.yaml

echo "Delete ingress"
kubectl delete ingress -l stateful-ingress
minikube addons disable ingress

echo "Deleting dnsutils"
kubectl delete pod -l name=dnsutils

kubectl delete persistentvolumeclaims -l role=mongo
