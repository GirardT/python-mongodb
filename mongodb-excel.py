from passwords import MONGODB

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://"+MONGODB[0]+":"+MONGODB[1]+"@cluster0.ixbnes0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Getting a Database and a Collection
# https://pymongo.readthedocs.io/en/stable/tutorial.html#getting-a-database
db = client["sample_mflix"]
collection = db["movies"]

# Convert PyMongo Cursor to Dataframe
# https://www.geeksforgeeks.org/convert-pymongo-cursor-to-dataframe/
import pandas as pd

data = list(collection.find())
df = pd.DataFrame(data)
print(df)

# Export DataFrame to Excel file
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html
excel_file = "mongodb_toexcel.xlsx"
df.to_excel(excel_file, index=False, engine='openpyxl')

print(f"Exported MongoDB documents to {excel_file}")