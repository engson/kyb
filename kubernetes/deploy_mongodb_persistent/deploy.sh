#!/bin/bash

echo "Creating the volumes"

kubectl apply -f ./volume_mongo.yaml

echo "Creating the mongo service and statefulset"
# The StatefulSet "mongo" is invalid: spec: Forbidden:
#    updates to statefulset spec for fields other than 'replicas',
#        'template', and 'updateStrategy' are forbidden
kubectl delete -f ./svc_sts_mongo.yaml
kubectl apply -f ./svc_sts_mongo.yaml
