import http.server
import json
import pymongo

# MongoDB connection (Same as your existing connection string)
MONGO_URI = "mongodb://integratedOmics:89e9646da70f864c2e9aea4d1edca93b@localhost:27017/?tls=true&tlsCAFile=/home/tmukku/next-flow_test/global-bundle.pem&directConnection=true&tlsAllowInvalidHostnames=true"

# Database and Collection
DB_NAME = "nextflow_pipeline_logs"
COLLECTION_NAME = "weblog_raw"

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI, w="majority", retryWrites=False)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

class WeblogHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            json_data = json.loads(post_data.decode('utf-8'))
            collection.insert_one(json_data)  # Insert raw JSON into MongoDB
            print("Inserted into MongoDB:", json_data["event"])  # Print event type
            self.send_response(200)
        except json.JSONDecodeError:
            print("Invalid JSON received")
            self.send_response(400)

        self.end_headers()

if __name__ == "__main__":
    server_address = ("", 8080)
    httpd = http.server.HTTPServer(server_address, WeblogHandler)
    print("Listening for Weblog data on port 8080...")
    httpd.serve_forever()
