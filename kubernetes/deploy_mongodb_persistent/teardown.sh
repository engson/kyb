#!/bin/bash

echo "Deleting the mongo service and statefulset"
kubectl delete -f ./svc_sts_mongo.yaml

kubectl delete persistentvolumeclaims -l service=mongo-service