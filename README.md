# kyb
Kybernetes Home office

## Day 1
- [ ] Setup work enviroment
    - [x] Install Centos8 on virtualBox
    - [x] Install TMUX
    - [x] Install minoconda
    - [x] Install Minikube (single-node Kubernetes)
    - [x] Install Kubernetes # https://phoenixnap.com/kb/how-to-install-kubernetes-on-centos
        - [x] Install kubectl
    - [x] Setup SSH key on github
    - [ ] 
- [ ] Setup conda enviroment "ckonda"
    - [ ] Install Python v3.6
    - [ ] Install Flask
    - [ ] Install pymongo
    - [ ] Install pyredis
    - [ ] Install Hamcrest
- [x] Install Vscode
    - [x] Python extension
    - [x] Yaml extension
- [ ] Follow Tutorial to learn basics of Kubernetes



## Day 2


### Backlog

- [ ] Setup Flask Backend
- [ ] Setup Flask Frontend
- [ ] Setup Mongodb client
- [ ] Setup Redis with mongodb
- [ ] Connect Backend with Frontend
- [ ] Setup keycloak
- [ ] Setup feature flags


#### Minikube
`minikube start` : Start cluster  
`minikube dashboard` : Access the Kubernetes Dashboard running within the minikube cluster.  
`minikube stop` : Stop local cluster  
`minikube delete` : Delete local cluster  
`minikube delete --all` : Delete all local clusters and profiles  

Once started: `kubectl`
`kubectl create deployment hello-minikube --image=k8s.gcr.io/echoserver:1.4` : Start server.  
`kubectl expose deployment hello-minikube --type=NodePort --port=8080` : Exposing a service as a NodePort.  
`minikube service hello-minikube` : Open exposed endpoin in your browser. 
`minikube start -p cluster2` : Start second local cluster (only with bare-metal/none driver).  

#### Kubectl - Kubernetes command-line tool.
Allows to run commands against Kubernetes clusters.


