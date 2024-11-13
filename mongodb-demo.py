from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from datetime import datetime
from typing import Optional
import urllib.parse

def initialize_mongodb(
    database_name: str,
    host: str = "localhost",
    port: int = 27017,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> Database:
    """
    Initialize MongoDB connection with optional authentication
    
    Args:
        database_name (str): Name of the MongoDB database
        host (str): MongoDB host address
        port (int): MongoDB port number
        username (str, optional): MongoDB username
        password (str, optional): MongoDB password
        
    Returns:
        Database: MongoDB database instance
    """
    try:
        # Construct connection URI
        if username and password:
            # Escape special characters in username and password
            escaped_username = urllib.parse.quote_plus(username)
            escaped_password = urllib.parse.quote_plus(password)
            uri = f"mongodb+srv://{escaped_username}:{escaped_password}@{host}"
        else:
            uri = f"mongodb+srv://{host}"
            
        # Create MongoDB client
        client = MongoClient(uri)
        
        # Get database instance
        db = client[database_name]
        
        # Test connection
        client.server_info()
        print(f"Successfully connected to MongoDB database: {database_name}")
        
        return db
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
        raise

def write_example_record(db: Database, collection_name: str = "users") -> Optional[str]:
    """
    Write an example record to MongoDB
    
    Args:
        db (Database): MongoDB database instance
        collection_name (str): Name of the collection to write to
        
    Returns:
        Optional[str]: ID of the inserted document if successful, None otherwise
    """
    try:
        # Get collection
        collection: Collection = db[collection_name]
        
        # Create example document
        example_record = {
            'name': 'Jane Doe',
            'email': 'jane.doe@example.com',
            'age': 30,
            'beta': True,
            'created_at': datetime.now(),
            'interests': ['reading', 'hiking', 'photography'],
            'address': {
                'street': '123 Main St',
                'city': 'Example City',
                'country': 'Example Country',
                'postal_code': '12345'
            },
            'metadata': {
                'last_updated': datetime.now(),
                'status': 'active'
            }
        }
        
        # Insert document
        result = collection.insert_one(example_record)
        
        print(f"Document inserted successfully with ID: {result.inserted_id}")
        return str(result.inserted_id)
        
    except Exception as e:
        print(f"Error writing to MongoDB: {str(e)}")
        return None

def read_example_record(db: Database, collection_name: str, document_id: str) -> Optional[dict]:
    """
    Read a record from MongoDB by its ID
    
    Args:
        db (Database): MongoDB database instance
        collection_name (str): Name of the collection to read from
        document_id (str): ID of the document to retrieve
        
    Returns:
        Optional[dict]: Document if found, None otherwise
    """
    try:
        from bson.objectid import ObjectId
        
        collection: Collection = db[collection_name]
        document = collection.find_one({'_id': ObjectId(document_id)})
        
        if document:
            print(f"Successfully retrieved document: {document_id}")
            return document
        else:
            print(f"No document found with ID: {document_id}")
            return None
            
    except Exception as e:
        print(f"Error reading from MongoDB: {str(e)}")
        return None

def main():
    """Main function to demonstrate MongoDB operations"""
    # Configuration
    HOST = "YOUR_HOST"
    DB_NAME = "YOUR_DB"
    COLLECTION_NAME = "users"
    
    # Optional authentication credentials
    USERNAME = "YOUR_USERNAME"  # Set your username if needed
    PASSWORD = "YOUR_PASSWORD"  # Set your password if needed
    
    try:
        # Initialize database connection
        db = initialize_mongodb(
            host=HOST,
            database_name=DB_NAME,
            username=USERNAME,
            password=PASSWORD
        )
        
        # Write example record
        doc_id = write_example_record(db, COLLECTION_NAME)
        
        if doc_id:
            # Read back the record we just wrote
            document = read_example_record(db, COLLECTION_NAME, doc_id)
            if document:
                print("\nRetrieved document contents:")
                print(f"Name: {document.get('name')}")
                print(f"Email: {document.get('email')}")
                print(f"Interests: {', '.join(document.get('interests', []))}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()