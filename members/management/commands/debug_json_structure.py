import json
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Debug the exact JSON structure'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file']
        
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        print("=== JSON STRUCTURE ANALYSIS ===")
        print(f"Top-level type: {type(data)}")
        print(f"Number of items: {len(data)}")
        
        # Examine first few items in detail
        for i in range(min(3, len(data))):
            print(f"\n--- Item {i} ---")
            item = data[i]
            print(f"Type: {type(item)}")
            print(f"Length: {len(item) if hasattr(item, '__len__') else 'N/A'}")
            print(f"Content: {item}")
            
            if isinstance(item, list):
                print("Key-Value pairs:")
                for j in range(0, len(item), 2):
                    if j + 1 < len(item):
                        print(f"  '{item[j]}': {item[j+1]} (type: {type(item[j+1])})")

        # Check if there are any names in the data
        print(f"\n=== CHECKING FOR NAMES ===")
        names_found = 0
        for i, item in enumerate(data):
            if isinstance(item, list):
                for j in range(0, len(item), 2):
                    if j + 1 < len(item) and item[j] == 'name':
                        names_found += 1
                        print(f"Found name: {item[j+1]}")
                        if names_found >= 5:  # Show first 5 names
                            break
                if names_found >= 5:
                    break
        
        print(f"\nTotal names found: {names_found}")