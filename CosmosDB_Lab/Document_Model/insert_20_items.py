from azure.cosmos import CosmosClient, PartitionKey
import os

# Replace these with your actual values from Portal -> Keys
COSMOS_URI = "<uri here>"
COSMOS_KEY = "<primary_key>"

client = CosmosClient(COSMOS_URI, credential=COSMOS_KEY)

# use existing DB & container or create if not exists
db = client.create_database_if_not_exists(id="Labado")
container = db.create_container_if_not_exists(
    id="Products",
    partition_key=PartitionKey(path="/category"),
    offer_throughput=400
)

categories = ["breakfast","lunch","dinner","sweet","snacks"]

for i in range(1,21):
    item = {
        "id": f"p{i}",
        "name": f"SampleDish{i}",
        "category": categories[i % len(categories)],
        "price": 40 + i,
        "tags": ["veg", "lab"]
    }
    container.upsert_item(item)
    print("Inserted", item["id"])
