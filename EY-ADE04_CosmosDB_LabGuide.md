EY-ADE 04 — Azure Cosmos DB: Practical Lab Guide (Step-by-step for slow learners)
How to use this guide
•	Work slowly, step-by-step. Read one step, do it, then move on. Each lab has a short checklist, expected outputs, quick troubleshooting tips, and an optional challenge.
•	If something fails, read the Troubleshooting box before asking for help.
________________________________________
Prerequisites (before you start)
•	An Azure subscription (free trial is fine). If you don’t have one, create at portal.azure.com.
•	A computer with a modern browser and internet access.
•	Optional: Azure CLI installed (https://learn.microsoft.com/cli/azure/install-azure-cli). If not, you can use the Azure Portal UI.
•	Optional: Python 3.8+ installed and pip available.
•	Install Python SDK (if you will run sample code):
•	pip install azure-cosmos
•	Time needed: 2–3 hours (you can split into shorter sessions).
________________________________________
Lab 1 — Introduction: NoSQL databases (Concept + quick hands-on)
Goal: Understand what NoSQL is and why Cosmos DB is a NoSQL database.
Steps (very slow, one at a time)
1.	Read this short explanation: NoSQL = databases that store non-tabular data (JSON, key-value, graph). They are designed to scale horizontally and handle flexible schemas.
2.	Compare to SQL: SQL uses structured tables, fixed schema. NoSQL stores JSON-like documents that can have different fields per item.
3.	Open Azure Portal and search for Azure Cosmos DB. Just look around — don’t create anything yet.
Quick check (write this down): Name two differences between SQL and NoSQL.
Troubleshooting: If portal.azure.com is slow, refresh or try an incognito window.
________________________________________
Lab 2 — Data models: Document, Key-Value, Graph (Hands-on simple examples)
Goal: See examples of the three major NoSQL models and create sample JSON files.
Parts
•	Document model (Cosmos DB Core/SQL API stores documents)
•	Key-Value model (fast lookups by key)
•	Graph model (useful for relationships—Cosmos DB supports Gremlin API)
Steps
1.	Create three folders on your machine: document-example, keyvalue-example, graph-example.
Document model (Core/SQL)
2.	Create a file product1.json with this content:
{
  "id": "p1",
  "category": "snacks",
  "name": "Masala Peanuts",
  "price": 50,
  "tags": ["snack","maharashtrian"]
}
3.	Create product2.json and make it different (maybe no tags field). This shows flexible schema.
Expected: Two JSON files. Notice product2.json may not have the same fields — that’s okay.
Key-Value model (simple file)
4.	Create kv-store.txt with lines like user:U101=Alice and user:U102=Bob.
Quick check: Explain how you would get Alice if you had key user:U101.
Graph model (conceptual)
5.	Draw on paper: Node Alice —[friend]-> Node Bob. This is a simple graph.
Optional: If curious, open the Cosmos DB Gremlin docs later to see queries for friends.
________________________________________
Lab 3 — Global distribution (concept + portal walkthrough)
Goal: Learn what global distribution is and enable it on a sample account.
Concept (simple):
•	Global distribution lets your database replicate across Azure regions to be nearer to users.
•	Benefits: lower read latency, regional failover, multi-region writes (optional).
Steps (Portal walkthrough)
1.	In the Azure Portal, click Create a resource → Azure Cosmos DB.
2.	Choose the API: Core (SQL) for document-style (recommended for this lab).
3.	Fill Subscription, Resource Group (create new), Account Name (e.g., eyade-cosmoslab-yourname), Location (pick the region closest to you, e.g., Central India or South India).
4.	Leave defaults for now and click Review + Create → Create.
5.	After provisioning, open your Cosmos account and find the Replicate data globally option (or Add region). Click it and add a second region (e.g., West India or Central US) — just add one extra region for learning.
Expected output: The account will show 2 regions. Note: Adding a region may cost more.
Troubleshooting: If you can’t add a region due to subscription limits, skip this step — you can still learn the concept.
________________________________________
Lab 4 — Scaling and performance (Throughput, RU/s, partitioning)
Goal: Understand Request Units (RU/s), provisioned throughput, and partition keys.
Concepts in plain words
•	RU/s = performance cost unit. Every read/write consumes RU. Think of RU as currency for operations.
•	Throughput = how many RU/s you reserve. Higher throughput → more operations per second.
•	Partition key = field used to distribute items across physical partitions. Choose it carefully (high-cardinality preferred, e.g., userId).
Steps (slow)
1.	In your Cosmos DB account, open Data Explorer.
2.	Create a new Database named labdb (click Add Database). For throughput choose Manual and set 400 RU/s (default minimal).
3.	Inside database create a Container named products. Set Partition key to /category for this simple lab. Keep throughput at 400 RU/s.
Why /category? For this lab it’s simple; in real apps you might pick a user id or product id.
Test performance with sample items
4.	Use Data Explorer → products → Items → New Item and paste product1.json from Lab 2. Save.
5.	Add 10 more items (duplicate with different id and category) to see distribution.
Quick experiment: Try querying SELECT * FROM c WHERE c.category='snacks' — note results.
Troubleshooting: If container creation fails with partition error, choose a different partition key or lower RU setting.
________________________________________
Lab 5 — Hands-on: Add sample items using code (Python) and query them
Goal: Write a small Python script to insert items and read them.
Steps (Python method)
1.	Ensure azure-cosmos is installed: pip install azure-cosmos.
2.	In Azure Portal, open your Cosmos DB account → Keys and copy the Primary Connection String or URI and PRIMARY KEY.
3.	Create a file cosmos_insert.py with this content (slowly paste and save):
from azure.cosmos import CosmosClient, PartitionKey

# Replace these with values from your portal
URI = "<YOUR_COSMOS_URI>"
KEY = "<YOUR_PRIMARY_KEY>"
DATABASE_NAME = 'labdb'
CONTAINER_NAME = 'products'

client = CosmosClient(URI, credential=KEY)

# create database (if not exists)
database = client.create_database_if_not_exists(id=DATABASE_NAME)

# create container (if not exists)
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME,
    partition_key=PartitionKey(path='/category'),
    offer_throughput=400
)

# sample items
items = [
    {"id": "p101", "category": "snacks", "name": "Chivda", "price": 60},
    {"id": "p102", "category": "drinks", "name": "Masala Chai", "price": 20}
]

for it in items:
    container.upsert_item(it)
    print('Inserted', it['id'])

# simple query
for row in container.query_items(query='SELECT * FROM c WHERE c.category="snacks"', enable_cross_partition_query=True):
    print('Query result:', row)
4.	Replace URI and KEY with values from portal and run:
python cosmos_insert.py
Expected output: Lines Inserted p101, Inserted p102, then query prints the snacks item.
Troubleshooting:
•	403 error: check the key/URI — maybe pasted wrong.
•	ImportError: ensure azure-cosmos installed.
________________________________________
Lab 6 — Simple queries, update, delete (Data Explorer + Python)
Goal: Learn basic CRUD operations.
Portal (Data Explorer)
1.	Open products → Items. Click any item → Edit → Save to update a field.
2.	To delete, open an item and click Delete.
Python examples (append to cosmos_insert.py or create cosmos_crud.py)
# read by id + partition key
item = container.read_item(item='p101', partition_key='snacks')
print('Read item:', item)

# replace/update
item['price'] = 65
container.replace_item(item=item, body=item)
print('Updated price to', item['price'])

# delete
container.delete_item(item='p102', partition_key='drinks')
print('Deleted p102')
Quick check: After delete, query for drinks should return nothing.
________________________________________
Lab 7 — Best practices checklist (short, cheat-sheet)
•	Choose a high-cardinality partition key (many unique values).
•	Avoid large items (>2 MB).
•	Use RU budgeting: monitor RU/s consumption in Metrics.
•	Use indexing policies for complex queries (later topic).
•	Use SDKs for bulk operations to save RU and time.
________________________________________
Final mini-project (combine everything)
Goal: Build a small product catalog with 20 items, distributed across 3 categories, add them via Python, and run queries:
•	Insert 20 items (mix categories: snacks, drinks, sweets).
•	Query top 5 cheapest snacks.
•	Update one item price & verify.
•	Delete one item & verify.
Assessment: Share a screenshot of the Data Explorer showing your container with items and the terminal output showing inserts & queries.
________________________________________
Extra help & troubleshooting common errors
•	Provisioning failed — check quota or subscription limits. Try a different region.
•	Authentication/403 — re-copy keys, ensure no extra spaces.
•	Module not found — run pip install azure-cosmos and ensure you use the same Python interpreter.
•	Slow portal — try smaller operations, refresh.
________________________________________
Optional extensions (if you finish early)
•	Try the Gremlin (graph) API: create a graph database and add vertices/edges.
•	Explore multi-region writes (careful, this may cost more).
•	Implement pagination in queries.
________________________________________
Lab log template (copy-paste this into a text file and write while you work)
•	Date & time started:
•	Steps completed (tick):
•	Errors encountered:
•	Output screenshots: (file paths)
•	What I learned in 1 sentence:
________________________________________
If you want, I can also:
•	Convert this into a printable PDF or a step-by-step slide deck (one lab per slide).
•	Provide the full Python files ready to download.
Good luck — go step-by-step and tell me which lab you want help with first.

