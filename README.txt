Hi there!  This project is to create a datagathering microserviced environment to collect and store the free traffic information provided by the City of Chicago Data Portal API on GCP.  Follow these instructions for an automatic build, learn from the design, and then customize it for your needs.  Keep in mind that this is still in progress and that a db-n1-standard-1 Cloud SQL instance will be sufficent for short-term collections of a month or under.  Any longer and you will need to resize your instance for more CPU.  Within this design though, while the output to BigQuery is optional (but advised for any large queries) the PostgreSQL endpoint is non-optional because it is utilized to verify that only new data is collected from each data pull.

1. Log into GCP and set up your free trial.
2. Bring up the Cloud Shell and run the following command to build your cluster:
    gcloud container clusters create trafficcollection --machine-type=n1-standard-1 --zone=us-central1-f --num-nodes=3
3. Once it is finished building take down the public IPs on each of the cluster nodes.
4. Build your PostgreSQL Cloud SQL server. You do not need to create any databases or tables/schemas on your instance.
5. Create a client SSL account for it.
6. Download each file and name them as such:
    gcppostgresslclient-cert.pem
    gcppostgresslclient-key.pem
    gcppostgresslserver-ca.pem
7. Under Connections in your Cloud SQL instance add each cluster IP into authorized network lists as /32s
8. Under APIs & Services -> Credentials create a service account key.
9. Name it "bigquerycreds", give it the BigQuery Admin role.  You do not need to create any instances, datasets or tables in BigQuery.
10. Download the json file and name it as such:
    bigquerycreds.json
11. Via the Cloud shell download this repository with the following command:
    git clone https://igetit41@github.com/igetit41/chicagotraffictracker.git --branch master ~/git
12. Upload the three .pem SSL cert files for your PostgreSQL server and the .json file for your BigQuery account to your Cloud Shell environment and into the following folder:
    /git/Credentials
13. Sign up for an API token from the City of Chicago here:
    https://data.cityofchicago.org/signup
14. Replace the following indicated values in the quickstart.sh file with your relevant info:
    --->export gcpuser=<GCP user email address you are shelled in with>

        export rabbitServer=rabbitmq.default.svc.cluster.local
    --->export rabbitServer_mqadmin=<select an admin username>
    --->export rabbitServer_mqadminpassword=<select an admin password>

        export stream_url=data.cityofchicago.org
    --->export stream_account=<Chicago Data Portal account email address>
    --->export stream_password=<Chicago Data Portal password>
    --->export stream_token=<Chicago Data Portal app token>

    --->export postgreSQL_user=<Postgre SQL instance username>
    --->export postgreSQL_password=<Postgre SQL instance password>
        export postgreSQL_database=postgres

    --->export postgreSQL_host=<Postgre SQL instance server IP>
        export postgreSQL_pathclientcert=~/git/Credentials/gcppostgresslclient-cert.pem
        export postgreSQL_pathclientkey=~/git/Credentials/gcppostgresslclient-key.pem 
        export postgreSQL_pathserverca=~/git/Credentials/gcppostgresslserver-ca.pem
        export bigquery_pathcreds=~/git/Credentials/bigquerycreds.json
15. Execute the following command:
    /git/quickstart.sh


Useful Links:
    City of Chicago Data Portal - https://data.cityofchicago.org/Transportation/Chicago-Traffic-Tracker-Congestion-Estimates-by-Se/n4j6-wkkf
    Google Cloud Platform - https://cloud.google.com/