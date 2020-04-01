# Mongodb pod

Scalable mongodb with replicasets
One master responsible for all write operations, with slaves copying from master and grandint read access to these copies.

## Setup replicasets

```bash
$ mongo
> rs.initiate({_id: "MainRepSet", version: 1, members: [
       { _id: 0, host : "mongod-0.mongodb-service.default.svc.cluster.local:27017" },
       { _id: 1, host : "mongod-1.mongodb-service.default.svc.cluster.local:27017" },
       { _id: 2, host : "mongod-2.mongodb-service.default.svc.cluster.local:27017" }
 ]});
```

"mongod-2.mongodb-service.default.svc.cluster.local" is Hostname of pods

## Anti affinity

Inter-Pod Anti-Affinity ensures that no 2 Mongo Pods are scheduled on the same worker node, thus, making it resilient to node failures. Also, it is recommended to keep the nodes in different AZs so that the cluster is resilient to Zone failures.

