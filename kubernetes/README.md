## Neo4j Causal Cluster
Create configmaps for read replicas and core pods:
```
kubectl create -f custom-core-configmap.yaml
kubectl create -f custom-replica-configmap.yaml
```
Install helm package with custom values
```
sudo helm --namespace=neo4j install mygraph https://github.com/neo4j-contrib/neo4j-helm/releases/download/4.2.2-1/neo4j-4.2.2-1.tgz --set acceptLicenseAgreement=yes --set neo4jPassword=mySecretPassword -f ./value.yaml
```
Port-forward leader node:
```
kubectl port-forward pod/mygraph-neo4j-core-2 7474:7474 7687:7687
```
Scale read replicas:
```
kubectl scale statefulset mygraph-neo4j-replica  --replicas=3
```

## FastAPI based Metadata Store App
Create Kubernetes deployment and service:
```
kubectl create -f metadata_app.yaml
```

## React.js based Metadata Store Dashboard
Create Kubernetes deployment and service:
```
kubectl create -f metadata_react_app.yaml
```
