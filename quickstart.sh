cd ~

#rm -r git
#git clone https://igetit41@github.com/igetit41/gcp-python.git --branch Develop ~/git

docker rm -f $(docker ps -a -q)
docker rmi -f $(docker images -q)

#gcloud container clusters create trafficcollection --num-nodes=3 --machine-type=n1-standard-1 --zone=us-central1-f
gcloud container clusters create trafficcollection --machine-type=n1-standard-1 --zone=us-central1-f --enable-autoscaling --min-nodes=2 --max-nodes=10 --num-nodes=3
#gcloud container clusters delete trafficcollection --zone=us-central1-f

#kubectl create clusterrolebinding myclusteradmin --clusterrole=cluster-admin --user=$USER
#kubectl create clusterrolebinding myclusteradmin --clusterrole=cluster-admin --user=jacob.edward.osterhaus@gmail.com

export rabbitServer=rabbitmq.default.svc.cluster.local
export rabbitServer_mqadmin=mqadmin
export rabbitServer_mqadminpassword=mqadminpassword


export stream_url=data.cityofchicago.org
#export stream_account=igetit41@yahoo.com
#export stream_password=suNder3%clicKed*4
#export stream_token=UOH7ZmZxwekfDYc9Hvqly0yep

export stream_account=d3f1l3@yahoo.com
export stream_password=suNder3%clicKed*4
export stream_token=4sPTvE8j53DI3OfvomPYU4cTv


export postgreSQL_user=postgres
export postgreSQL_password=leNdAnjLOyw0wfJw
export postgreSQL_database=postgres

#export postgreSQL_host=35.226.52.136
#export postgreSQL_host=172.27.176.3
#export postgreSQL_pathclientcert=~/git/Credentials/gcppostgresslclient-cert.pem
#export postgreSQL_pathclientkey=~/git/Credentials/gcppostgresslclient-key.pem 
#export postgreSQL_pathserverca=~/git/Credentials/gcppostgresslserver-ca.pem
#export bigquerycreds=~/git/Credentials/bigquerycreds.json

export postgreSQL_host=35.238.48.234
#export postgreSQL_host=10.4.96.5
export postgreSQL_pathclientcert=~/git/Credentials-np/gcppostgresslclient-cert.pem
export postgreSQL_pathclientkey=~/git/Credentials-np/gcppostgresslclient-key.pem 
export postgreSQL_pathserverca=~/git/Credentials-np/gcppostgresslserver-ca.pem
export bigquery_pathcreds=~/git/Credentials-np/bigquerycreds.json


cp $postgreSQL_pathclientcert ~/git/pythonDBPopulate-postgresql/gcppostgresslclient-cert.pem
cp $postgreSQL_pathclientkey ~/git/pythonDBPopulate-postgresql/gcppostgresslclient-key.pem
cp $postgreSQL_pathserverca ~/git/pythonDBPopulate-postgresql/gcppostgresslserver-ca.pem

cp $postgreSQL_pathclientcert ~/git/datadist-postgresql/gcppostgresslclient-cert.pem
cp $postgreSQL_pathclientkey ~/git/datadist-postgresql/gcppostgresslclient-key.pem
cp $postgreSQL_pathserverca ~/git/datadist-postgresql/gcppostgresslserver-ca.pem

cp $postgreSQL_pathclientcert ~/git/pythonWeb/app/gcppostgresslclient-cert.pem
cp $postgreSQL_pathclientkey ~/git/pythonWeb/app/gcppostgresslclient-key.pem
cp $postgreSQL_pathserverca ~/git/pythonWeb/app/gcppostgresslserver-ca.pem

cp $bigquery_pathcreds ~/git/pythonDBPopulate-bigquery/bigquerycreds.json


cp $postgreSQL_pathclientcert ~/git/pythontest/gcppostgresslclient-cert.pem
cp $postgreSQL_pathclientkey ~/git/pythontest/gcppostgresslclient-key.pem
cp $postgreSQL_pathserverca  ~/git/pythontest/gcppostgresslserver-ca.pem
cp $bigquery_pathcreds ~/git/pythontest/bigquerycreds.json

cp ~/git/pythonDBPopulate-postgresql/pythonDBPopulate-postgresql.py ~/git/pythontest/pythonDBPopulate-postgresql.py
cp ~/git/datadist-postgresql/datadist-postgresql.py ~/git/pythontest/datadist-postgresql.py
cp ~/git/pythonDBPopulate-bigquery/pythonDBPopulate-bigquery.py ~/git/pythontest/pythonDBPopulate-bigquery.py
cp ~/git/pythonStreamConsume/pythonStreamConsume.py ~/git/pythontest/pythonStreamConsume.py
cp ~/git/datalivetrans/datalivetrans.py ~/git/pythontest/datalivetrans.py
cp ~/git/pythonWeb/app/main.py ~/git/pythontest/main.py

cp ~/git/pythontest/postgresql.py ~/git/pythonWeb/app/postgresql.py

cp ~/git/pythontest/looptest.py ~/git/datadist-postgresql/looptest.py
cp ~/git/pythontest/looptest.py ~/git/pythonDBPopulate-postgresql/looptest.py
cp ~/git/pythontest/looptest.py ~/git/pythonDBPopulate-bigquery/looptest.py
cp ~/git/pythontest/looptest.py ~/git/pythonStreamConsume/looptest.py

export rabbitmqrbacFile=~/git/rabbitmq-cluster/rabbitmq_rbac.yaml
export rabbitmqssFile=~/git/rabbitmq-cluster/rabbitmq_statefulsets.yaml
export dbpbigqFile=~/git/pythonDBPopulate-bigquery/dep-dbpbigq.yaml
export dbppgsqlFile=~/git/pythonDBPopulate-postgresql/dep-dbppgsql.yaml
export datadistFile=~/git/datadist-postgresql/dep-datadist.yaml
export strconsFile=~/git/pythonStreamConsume/dep-strcons.yaml
export fullenvFile=~/git/fullenvironment.yaml

export rabbitmqImage=gcr.io/$DEVSHELL_PROJECT_ID/rabbitmq:v2
export bigqueryImage=gcr.io/$DEVSHELL_PROJECT_ID/dbpbigq:v2
export dbppgsqlImage=gcr.io/$DEVSHELL_PROJECT_ID/dbppgsql:v2
export datadistImage=gcr.io/$DEVSHELL_PROJECT_ID/datadist:v6
export strconsImage=gcr.io/$DEVSHELL_PROJECT_ID/strcons:v9


cd ~/git/rabbitmq
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


cd ~
#envsubst < $fullenvFile | kubectl apply -f -
envsubst < $rabbitmqrbacFile | kubectl apply -f -
envsubst < $rabbitmqssFile | kubectl apply -f -
#kubectl delete deployment dep-datadist
envsubst < $datadistFile | kubectl apply -f -
envsubst < $dbppgsqlFile | kubectl apply -f -
envsubst < $dbpbigqFile | kubectl apply -f -
#kubectl delete deployment dep-strcons
envsubst < $strconsFile | kubectl apply -f -

kubectl get pods

