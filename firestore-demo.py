from firebase_admin import initialize_app, firestore
import datetime

def initialize_firestore():
    initialize_app()
    return firestore.client(database_id="demonstration")

def write_example_record():
    """Write an example record to Firestore"""
    try:
        # Get Firestore client
        db = initialize_firestore()
        
        # Create example data
        example_record = {
            'name': 'Jane Doe',
            'email': 'jane.doe@example.com',
            'age': 30,
            'beta': True,
            'created_at': datetime.datetime.now(),
            'interests': ['reading', 'hiking', 'photography'],
            'address': {
                'street': '123 Main St',
                'city': 'Example City',
                'country': 'Example Country',
                'postal_code': '12345'
            }
        }
        
        # Add document to 'users' collection with auto-generated ID
        doc_ref = db.collection('users').add(example_record)
        
        print(f"Document added successfully with ID: {doc_ref[1].id}")
        return doc_ref[1].id
        
    except Exception as e:
        print(f"Error writing to Firestore: {str(e)}")
        return None

def main():
    """Main function to demonstrate Firestore operations"""
    print("Initializing Firestore connection...")
    doc_id = write_example_record()
    
    if doc_id:
        print("Example record written successfully!")
        print(f"You can query this record using the document ID: {doc_id}")

if __name__ == "__main__":
    main()