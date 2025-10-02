from pymongo import MongoClient

# Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017/")

# Create a test database and collection
db = client["test_database"]
collection = db["test_collection"]

# Insert a test document into the collection
result = collection.insert_one({"name": "Vishant", "role": "Developer"})

# Print the ID of the inserted document
print("Data inserted with ID:", result.inserted_id)

# Retrieve and print all documents from the collection
for doc in collection.find():
    print(doc)
