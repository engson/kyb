#!/bin/bash

echo "Deleting the mongo service and statefulset"
kubectl delete -f ./svc_sts_mongo.yaml

echo "Deleting the volumes"
kubectl delete -f ./volume_mongo.yaml
