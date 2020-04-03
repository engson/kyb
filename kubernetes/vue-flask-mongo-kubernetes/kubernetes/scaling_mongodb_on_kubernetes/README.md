# scaling mongodb on kubernetes

<https://medium.com/faun/scaling-mongodb-on-kubernetes-32e446c16b82>

_StatefulSets are intended to be used with stateful applications and distributed systems._

One of the best use cases for this is to orchaestrate data-store services such as MongoDB, ElasticSearch, Redis, Zookeeper and so on.

Some of the features that can be ascribed to StatefulSets are:

1. Pods with Ordinal Indexes
2. Stable Network Identities
3. Ordered and Parallel Pod Management
4. Rolling Updates

Details for these can be found here. <https://kubernetes.io/docs/tutorials/stateful-application/basic-stateful-set/>

One very distinct feature of Stateful Sets is to provide Stable
Network Identities which when used with Headless Services , can be even more powerful.

Without spending much time on information readily available in Kubernetes documentation, let us focus on running and scaling a MongoDB cluster.

You need to have a running Kubernetes Cluster with RBAC enabled (recommended). In this tutorial I will be using a GKE cluster, however, AWS EKS or Microsoft’s AKS or a Kops Managed K8’s K8’s are also viable alternatives.

We will deploy the following components for our MongoDB cluster

1. Daemon Set to configure HostVM
2. Service Account and ClusterRole Binding for Mongo Pods
3. Storage Class to provision persistent SSDs for the Pods
4. Headless Service to access to Mongo Containers
5. Mongo Pods Stateful Set
6. GCP Internal LB to access MongoDB from outside the kuberntes cluster (Optional)
7. Access to pods using Ingress (Optional)

It is important to note that each MongoDB Pod will have a sidecar running, in order to configure the replica set, on the fly. The sidecar checks for new members every 5 seconds.

__Important Points:__

1. The Sidecar for Mongo should be configured carefully with proper environment variables, stating the labels given to the pod, namespace for the deployment and service. Details about the sidecar container can be found here <https://github.com/cvallance/mongo-k8s-sidecar>.
2. The guidance around default cache size is: “50% of RAM minus 1 GB, or 256 MB”. Given that the amount of memory requested is 2GB, the WiredTiger cache size here, has been set to 256MB
3. Inter-Pod Anti-Affinity ensures that no 2 Mongo Pods are scheduled on the same worker node, thus, making it resilient to node failures. Also, it is recommended to keep the nodes in different AZs so that the cluster is resilient to Zone failures.
4. The Sevice Account currently deployed has admin priviledges. However, it should be restricted to the DB’s namespace.

## Delpoy steps

```s
kubectl apply -f configure-node.yml
kubectl apply -f mongo.yml
```

The headless service with noCluster-IP and neither an External-IP, is a __headless service.__ svc/mongo will directly resolve to __Pod-IPs__ for our Stateful Sets.

### DNS resolution

To verify DNS resolution. We launch an interactive shell within our cluster.

```s
kubectl apply -f dnslookup.yaml
kubectl exec -it dnsutils -- sh
/# dig mongo.default +search +noall +answer +cmd
; <<>> DiG 9.11.6-P1 <<>> mongo.default +search +noall +answer +cmd                                                                
;; global options: +cmd
<answer>
mongo.default.svc.cluster.local. 30 IN  A       172.17.0.9
mongo.default.svc.cluster.local. 30 IN  A       172.17.0.3
mongo.default.svc.cluster.local. 30 IN  A       172.17.0.4
```

OLD METHOD FROM AUTHOR (dig not included in ubuntu image anymore)

```s
kubectl run my-shell --rm -i --tty --image ubuntu -- bash
root@my-shell-68974bb7f7-cs4l9:/# dig mongo.mongo +search +noall +answer
; <<>> DiG 9.11.3-1ubuntu1.1-Ubuntu <<>> mongo.mongo +search +noall +answer
;; global options: +cmd
mongo.mongo.svc.cluster.local. 30 IN A 10.56.7.10
mongo.mongo.svc.cluster.local. 30 IN A 10.56.8.11
mongo.mongo.svc.cluster.local. 30 IN A 10.56.1.4
```

The DNS for service will be [name of service].[namespace of service]. In our case `mongo.mongo`.

The IPS( 10.56.6.17, 10.56.7.10, 10.56.8.11 ) are our Mongo Stateful Set’s Pod IPs.  
This can be tested by running a nslookup over these, from inside the cluster.

```s
root@my-shell-68974bb7f7-cs4l9:/# nslookup 10.56.6.17

17.6.56.10.in-addr.arpa name = mongo-0.mongo.mongo.svc.cluster.local.
```

Nslookup inside dnsutils pod.

```sh 
/ # nslookup 172.17.0.9
9.0.17.172.in-addr.arpa name = mongo-2.mongo.default.svc.cluster.local.                                                            

/ # nslookup 172.17.0.3
3.0.17.172.in-addr.arpa name = mongo-0.mongo.default.svc.cluster.local.                                                            

/ # nslookup 172.17.0.4
4.0.17.172.in-addr.arpa name = mongo-1.mongo.default.svc.cluster.local.
```

If you app is deployed in the K8’s cluster itself, then it can access the nodes by

```s
Node-0: mongo-0.mongo.mongo.svc.cluster.local:27017
Node-1: mongo-1.mongo.mongo.svc.cluster.local:27017
Node-2: mongo-2.mongo.mongo.svc.cluster.local:27017
```

If you would like to access the mongo nodes from outside the cluster you can deploy internal load balancers for each of these pods or create an internal ingress, using an Ingress Controller such as NGINX or Traefik.

### GCP Internal LB SVC Configuration (Optional)

```yaml
apiVersion: v1
kind: Service
metadata: 
  annotations: 
    cloud.google.com/load-balancer-type: Internal
  name: mongo-0
  namespace: mongo
spec: 
  ports: 
    - 
      port: 27017
      targetPort: 27017
  selector: 
    statefulset.kubernetes.io/pod-name: mongo-0
  type: LoadBalancer
```

Deploy 2 more such services for mongo-1 and mongo-2.
You can provide the IPs of the Internal Load Balancer to the MongoClient URI.

```bash
root$ kubectl -n mongo get svc
NAME      TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)           AGE
mongo     ClusterIP      None            <none>        27017/TCP         15m
mongo-0   LoadBalancer   10.59.252.157   10.20.20.2    27017:30184/TCP   9m
mongo-1   LoadBalancer   10.59.252.235   10.20.20.3    27017:30343/TCP   9m
mongo-2   LoadBalancer   10.59.254.199   10.20.20.4    27017:31298/TCP   9m
```

The external IPs for mongo-0/1/2 are the IPs of the newly created TCP loadbalancers.  
These are local to your Subnetwork or peered networks, if any.

### Access Pods using Ingress (Optional)

Traffic to Mongo Stateful set pods can also be directed using an Ingress Controller such as Nginx.  
Make sure the ingress service is internal and not exposed over public ip. The ingress object will look something like this:

```yaml
spec:
  rules:
  - host: mongo.example.com
    http:
      paths:
      - path: '/'
        backend:
          serviceName: mongo # There is no extra service. This is 
          servicePort: '27017' # the headless service.
```

It is important to note that your application is aware of atleast one mongo node which is currently up so that it can discover all the others.

Author used Robo3T as mongoclient for following step.
Connect to one of the nodes, and running `rs.status()` to see details of replicaset, and check if the other 2 pods were configured and connected to the Replica Set automatically.
A fully qualified domain name should be seen from each member.

Now we scale the Stateful Set for mongo Pods to check if the new mongo containers get added to the ReplicaSet or not.

```s
root$ kubectl -n mongo scale statefulsets mongo --replicas=4
statefulset "mongo" scaled

root$ kubectl -n mongo get pods -o wide
```

The scaling action will also automatically provision a persistent volume, which will act as the data directory for the new pod.
We run `rs.scale()` again to see if another member was added.

## Further Considerations

1. It can be helpful to label the Node Pool which will be used for Mongo Pods and ensure that appropriate Node Affinity is mentioned in the Spec for the Stateful Set and HostVM configurer Daemon Set . This is because the Daemon set will tweak some parameters of the host OS and those settings should be restricted for MongoDB Pods only. Other applications might work better without those settings.

2. Labelling a node pool is extremely easy in GKE, can be directly from the GCP console.
3. Although we have specified CPU and Memory limits in the Pod Spec, we can also consider deploying a VPA (Vertical Pod Autoscaler).
4. Traffic to our DB from inside the cluster can be controlled by implementing network policies or a service mesh such as Istio.
