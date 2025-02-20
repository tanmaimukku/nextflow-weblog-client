# nextflow-weblog-client
A lightweight Python HTTP server that captures Nextflow Weblog events and forwards them to Amazon DocumentDB (MongoDB). This enables real-time tracking of Nextflow pipeline execution.

## What is Nextflow Weblog?
Nextflow provides a [Weblog](https://github.com/nextflow-io/weblog) feature that streams pipeline execution events in real-time via HTTP.

## How It Works
1. Nextflow sends Weblog events via HTTP to this client.
2. The client receives and stores the events in MongoDB.
3. Events are logged in the configured database and collection.

## MongoDB Configuration
Update the connection string in the script:
```python
MONGO_URI = "mongodb://<username>:<password>@localhost:27017/?tls=true&tlsCAFile=<path-to-ca-file>&directConnection=true&tlsAllowInvalidHostnames=true"
DB_NAME = "nextflow_pipeline_logs"
COLLECTION_NAME = "weblog_raw"
```

## SSH Tunnel Setup
Since Amazon DocumentDB is not publicly accessible, set up an SSH tunnel:

```sh
ssh -i <your-private-key> -p 22 -L 27017:<documentdb-endpoint>:27017 ec2-user@<jump-host> -N
```

Replace `<your-private-key>` with your SSH key path.  
Replace `<documentdb-endpoint>` with your DocumentDB cluster endpoint.  
Replace `<jump-host>` with your SSH-accessible host.  

## Running the Weblog Client
Ensure Python is installed, then start the client:

```sh
python3 weblog_client.py
```

Then, run your pipeline with:

```sh
nextflow run <pipeline>.nf -with-weblog http://localhost:8080
```
This client captures Nextflow Weblog events and sends them to MongoDB for storage.  

