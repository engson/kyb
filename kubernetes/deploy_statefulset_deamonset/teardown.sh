#!/bin/sh
##
# Script to remove/undepoy all project resources from the local Minikube environment.
##

# Delete mongod stateful set + mongodb service + secrets + host vm configuer daemonset
kubectl delete -f daemonset.yaml
kubectl delete -f deployment.yaml
kubectl delete -f statefulset.yaml
