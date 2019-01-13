#Declare Environment Variables
export gcpuser=#<GCP user email address you are shelled in with>

export rabbitServer=rabbitmq.default.svc.cluster.local
export rabbitServer_mqadmin=#<select an admin username>
export rabbitServer_mqadminpassword=#<select an admin password>

export stream_url=data.cityofchicago.org
export stream_account=#<Chicago Data Portal account email address>
export stream_password=#<Chicago Data Portal password>
export stream_token=#<Chicago Data Portal app token>

export postgreSQL_user=postgres
export postgreSQL_password=#<Postgre SQL instance password>
export postgreSQL_database=postgres

export postgreSQL_host=#<Postgre SQL instance server IP>
export postgreSQL_pathclientcert=~/git/Credentials/gcppostgresslclient-cert.pem
export postgreSQL_pathclientkey=~/git/Credentials/gcppostgresslclient-key.pem 
export postgreSQL_pathserverca=~/git/Credentials/gcppostgresslserver-ca.pem
export bigquery_pathcreds=~/git/Credentials/bigquerycreds.json

export rabbitmqrbacFile=~/git/rabbitmq-cluster/rabbitmq_rbac.yaml
export rabbitmqssFile=~/git/rabbitmq-cluster/rabbitmq_statefulsets.yaml
export dbpbigqFile=~/git/pythonDBPopulate-bigquery/dep-dbpbigq.yaml
export dbppgsqlFile=~/git/pythonDBPopulate-postgresql/dep-dbppgsql.yaml
export datadistFile=~/git/datadist-postgresql/dep-datadist.yaml
export strconsFile=~/git/pythonStreamConsume/dep-strcons.yaml

export rabbitmqImage=gcr.io/$DEVSHELL_PROJECT_ID/rabbitmq:v1
export bigqueryImage=gcr.io/$DEVSHELL_PROJECT_ID/dbpbigq:v1
export dbppgsqlImage=gcr.io/$DEVSHELL_PROJECT_ID/dbppgsql:v1
export datadistImage=gcr.io/$DEVSHELL_PROJECT_ID/datadist:v1
export strconsImage=gcr.io/$DEVSHELL_PROJECT_ID/strcons:v1

#Move Credentials
cp $postgreSQL_pathclientcert ~/git/pythonDBPopulate-postgresql/gcppostgresslclient-cert.pem
cp $postgreSQL_pathclientkey ~/git/pythonDBPopulate-postgresql/gcppostgresslclient-key.pem
cp $postgreSQL_pathserverca ~/git/pythonDBPopulate-postgresql/gcppostgresslserver-ca.pem

cp $postgreSQL_pathclientcert ~/git/datadist-postgresql/gcppostgresslclient-cert.pem
cp $postgreSQL_pathclientkey ~/git/datadist-postgresql/gcppostgresslclient-key.pem
cp $postgreSQL_pathserverca ~/git/datadist-postgresql/gcppostgresslserver-ca.pem

cp $bigquery_pathcreds ~/git/pythonDBPopulate-bigquery/bigquerycreds.json

#Create role binding to allow rabbit clustering
kubectl create clusterrolebinding myclusteradmin --clusterrole=cluster-admin --user=$gcpuser

#Create images
cd ~/git/rabbitmq-custer
docker rmi $rabbitmqImage -f
docker build -f ./Dockerfile -t $rabbitmqImage .
gcloud docker -- push $rabbitmqImage

cd ~/git/datadist-postgresql
docker rmi $datadistImage -f
docker build -f ./Dockerfile -t $datadistImage .
gcloud docker -- push $datadistImage

cd ~/git/pythonDBPopulate-postgresql
docker rmi $dbppgsqlImage -f
docker build -f ./Dockerfile -t $dbppgsqlImage .
gcloud docker -- push $dbppgsqlImage

cd ~/git/pythonDBPopulate-bigquery
docker rmi $bigqueryImage -f
docker build -f ./Dockerfile -t $bigqueryImage .
gcloud docker -- push $bigqueryImage

cd ~/git/pythonStreamConsume
docker rmi $strconsImage -f
docker build -f ./Dockerfile -t $strconsImage .
gcloud docker -- push $strconsImage

#Build Environment
cd ~
envsubst < $rabbitmqrbacFile | kubectl apply -f -
envsubst < $rabbitmqssFile | kubectl apply -f -
sleep 180
envsubst < $datadistFile | kubectl apply -f -
sleep 60
envsubst < $dbppgsqlFile | kubectl apply -f -
sleep 60
envsubst < $dbpbigqFile | kubectl apply -f -
sleep 60
envsubst < $strconsFile | kubectl apply -f -

#Display environment
kubectl get ConfigMaps
kubectl get HorizontalPodAutoscalers
kubectl get Services
kubectl get Deployments
kubectl get Statefulsets
kubectl get Pods

