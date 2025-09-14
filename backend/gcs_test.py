from google.cloud import storage

# Use your service account JSON file (just filename, since it's in the same folder)
client = storage.Client.from_service_account_json("skillful-air-453214-m7-5fcfdbc81141.json")

# Test: list buckets
for bucket in client.list_buckets():
    print(bucket.name)
