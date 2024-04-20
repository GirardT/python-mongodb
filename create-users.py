# Generate Random Data for MongoDB
# https://sysadmins.co.za/generate-random-data-for-mongodb/

from passwords import MONGODB

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import faker
import time
import bcrypt
import random

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
db = client["ustaa"]
collection = db["users"]

# Constants
NUM_USERS = int(input("Enter number of users: ") or 10)

# Initialize Faker
# https://faker.readthedocs.io/en/master/
fake = faker.Faker()

SERVICE_NAMES = [
    'Accounting Pro', 'Software Solutions', 'Tech Support Hub', 
    'Legal Consultancy', 'Marketing Experts', 'Financial Planning', 
    'Engineering Innovations', 'Creative Design Studio', 
    'IT Network Services', 'Real Estate Advisors', 'Educational Resources', 
    'Medical Health Services', 'Hospitality Management', 'Environmental Services', 
    'Security & Surveillance', 'Construction & Development', 
    'Logistics & Transportation', 'Human Resources Consulting', 
    'Event Planning Professionals', 'Fitness & Wellness Coaching'
]

EDUCATION_COURSES = [
    'Software Engineering', 'Computer Science', 'Information Technology', 
    'Electrical Engineering', 'Business Administration', 'Marketing', 
    'Accounting', 'Law', 'Mechanical Engineering', 'Civil Engineering'
]

UNIVERSITIES = [
    'UNSW', 'University of Sydney', 'Monash University', 
    'University of Melbourne', 'Australian National University', 
    'University of Queensland', 'University of Western Australia', 
    'University of Adelaide', 'University of Technology Sydney', 
    'Macquarie University'
]

STATES = ['act', 'nsw', 'nt', 'qld', 'sa', 'tas', 'vic', 'wa']

# Function to generate a random user with the password 'hello123'
def generate_user():
    password = bcrypt.hashpw(b'hello123', bcrypt.gensalt())
    return {
        'email': fake.email(),
        'password': password.decode(),
        'firstName': fake.first_name(),
        'lastName': fake.last_name(),
        'phone': '0411222333',
        'state': random.choice(STATES),
        'suburb': fake.city(),
        'postcode': fake.zipcode(),
        'facebookName': fake.user_name(),
        'story': fake.sentence(nb_words=random.randint(2, 6)),
        'alumniProfilePicture': fake.image_url(),
        'education': {
            'course': random.choice(EDUCATION_COURSES),
            'college': random.choice(UNIVERSITIES),
            'yearGraduated': fake.date_between(start_date='-20y', end_date='-4y').isoformat(),
        },
        'service': {
            'serviceName': random.choice(SERVICE_NAMES),
            'serviceDescription': fake.sentence(nb_words=random.randint(2, 6)),
            'serviceUrl': fake.url(),
        },
        'isAutomated': True,
        'isOfficer': False,
        'hideProfile': False,
        'isProfileComplete': True
    }

# Function to insert a batch of users into the database
def insert_users(number_of_users):
    try:
        for _ in range(number_of_users):
            user = generate_user()
            collection.insert_one(user)
        
        print(f"{number_of_users} users successfully inserted into the database")
    except Exception as e:
        print(f"Error inserting users: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    insert_users(NUM_USERS)