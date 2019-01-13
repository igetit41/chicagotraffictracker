1. Log into GCP and set up your free trial.
2. Bring up the Cloud Shell and run the following command to build your cluster:
    gcloud container clusters create trafficcollection --machine-type=n1-standard-1 --zone=us-central1-f --enable-autoscaling --min-nodes=2 --max-nodes=10 --num-nodes=3
3. Once it is finished building take down the public IPs on each of the cluster nodes.
4. Build your PostgreSQL Cloud SQL server.
5. Create a client SSL account for it.
6. Download each file and name them as such:
    gcppostgresslclient-cert.pem
    gcppostgresslclient-key.pem
    gcppostgresslserver-ca.pem
7. Under Connections in your Cloud SQL instance add each cluster IP into authorized network lists as /32s
8. Under APIs & Services -> Credentials create a service account key.
9. Name it "bigquerycreds", give it the BigQuery Admin role.
10 Download the json file and name it as such:
    bigquerycreds.json
11. Via the Cloud shell download this repository with the following command:
    git clone https://igetit41@github.com/igetit41/chicagotraffictracker.git --branch master ~/git
12. Upload the three .pem SSL cert files for your PostgreSQL server and the .json file for your BigQuery account into the following folder:
    /git/Credentials
13. Replace the following values in the quickstart.sh file with your relevant info:
    <GCP user email address>
    export rabbitServer_mqadmin=<admin username>
    export rabbitServer_mqadminpassword=<admin password>


    export stream_url=data.cityofchicago.org
    export stream_account=<account>
    export stream_password=<password>
    export stream_token=<token>


    export postgreSQL_user=<username>
    export postgreSQL_password=<password>
    export postgreSQL_database=<database name>

    export postgreSQL_host=<server IP>
14. Execute the following command:
    /git/quickstart.sh