import json  # For formatting output as JSON
import urllib.request  # To make HTTP requests using standard library
import urllib.error  # To handle HTTP errors
import unittest  # For writing unit tests

import TestMetadataFunctions from unit_tests.py #importing unit test class

# AWS metadata service base URL
#METADATA_BASE_URL = "http://{{instance_url}}/latest/meta-data/"
#METADATA_BASE_URL = "insert_AWS_instance_url"

def get_metadata():
    """
    Gets all the available information about the AWS instance.
    It returns everything as a list of key-value pairs, 
    like a detailed summary of the instance's settings and environment.

    """
    metadata = {}
    try:
        # Get list of metadata keys
        # Sample response from this call:
        # ami-id
        # hostname
        # instance-id
        # instance-type
        # ...
        # Each line is a key that can be queried individually by appending it to METADATA_BASE_URL
        with urllib.request.urlopen(METADATA_BASE_URL, timeout=2) as response:
            keys = response.read().decode().splitlines()

        # Retrieve value for each key
        for key in keys:
            key_url = METADATA_BASE_URL + key
            try:
                with urllib.request.urlopen(key_url, timeout=2) as key_response:
                    metadata[key] = key_response.read().decode()
            except urllib.error.URLError as e:
                print(f"Error retrieving key '{key}': {e}")
    except urllib.error.URLError as e:
        print(f"Error retrieving metadata: {e}")
    return metadata

def get_metadata_key(key):
    """
    Gets the value for a specific piece of information from the AWS instance. 
    User just need to give the name of what you're looking for, 
    and it will return the value if it exists.
    
    """
    try:
        key_url = METADATA_BASE_URL + key
        with urllib.request.urlopen(key_url, timeout=2) as response:
            return response.read().decode()
    except urllib.error.URLError as e:
        print(f"Error retrieving metadata key '{key}': {e}")
        return None

if __name__ == "__main__":
    try:
        # Prompt user to enter a metadata key
        user_key = input("Enter a metadata key to retrieve (leave blank to fetch all): ").strip()

        if user_key:
            # Try to fetch the specific key
            value = get_metadata_key(user_key)
            if value is not None:
                print(json.dumps({user_key: value}, indent=2))
            else:
                # If key is invalid or error occurs, show message and fallback to full metadata
                print("Error: Please recheck key value. Defaulting to fetch all metadata.")
                full_metadata = get_metadata()
                print(json.dumps(full_metadata, indent=2))
        else:
            # If no key is provided, fetch all metadata
            full_metadata = get_metadata()
            print(json.dumps(full_metadata, indent=2))

    except Exception as e:
        # Catch any unexpected errors and fallback to full metadata
        print(f"Unexpected error occurred: {e}")
        print("Defaulting to fetch all metadata.")
        full_metadata = get_metadata()
        print(json.dumps(full_metadata, indent=2))

    # Run unit tests
    unittest.main(argv=[''], exit=False)
