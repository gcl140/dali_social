import json
from django.core.management.base import BaseCommand
from members.models import Member

class Command(BaseCommand):
    help = 'Import DALI members from list format JSON'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file']
        
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)
            
            members_created = 0
            errors = []
            
            # Process each member in the list
            for index, member_data in enumerate(data):
                try:
                    if isinstance(member_data, list):
                        # Convert the list of key-value pairs to a dictionary
                        member_dict = {}
                        for i in range(0, len(member_data), 2):
                            if i + 1 < len(member_data):
                                key = member_data[i]
                                value = member_data[i + 1]
                                member_dict[key] = value
                        
                        # Create the member
                        if member_dict.get('name'):
                            self.create_member(member_dict)
                            members_created += 1
                            self.stdout.write(f"Created: {member_dict['name']}")
                        else:
                            errors.append(f"Member at index {index} has no name")
                    
                except Exception as e:
                    errors.append(f"Error with member at index {index}: {str(e)}")
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {members_created} members')
            )
            
            if errors:
                self.stdout.write(
                    self.style.ERROR(f'Encountered {len(errors)} errors:')
                )
                for error in errors:
                    self.stdout.write(self.style.ERROR(f'  {error}'))
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error importing members: {str(e)}')
            )

    def create_member(self, data):
        """Create a member with the data"""
        # Clean and prepare the data
        cleaned_data = {
            'name': self.clean_value(data.get('name', '')),
            'year': self.clean_value(data.get('year', '2024')),
            'dev': bool(data.get('dev', False)),
            'des': bool(data.get('des', False)),
            'pm': bool(data.get('pm', False)),
            'core': bool(data.get('core', False)),
            'mentor': bool(data.get('mentor', False)),
            'major': self.clean_value(data.get('major', '')),
            'minor': self.clean_value(data.get('minor', '')),
            'birthday': self.clean_value(data.get('birthday', '')),
            'home': self.clean_value(data.get('home', '')),
            'quote': self.clean_value(data.get('quote', '')),
            'favorite_thing_1': self.clean_value(data.get('favorite thing 1', '')),
            'favorite_thing_2': self.clean_value(data.get('favorite thing 2', '')),
            'favorite_thing_3': self.clean_value(data.get('favorite thing 3', '')),
            'favorite_dartmouth_tradition': self.clean_value(data.get('favorite dartmouth tradition', '')),
            'fun_fact': self.clean_value(data.get('fun fact', '')),
            'picture': self.clean_value(data.get('picture', '')),
        }
        
        # Create the member
        Member.objects.create(**cleaned_data)

    def clean_value(self, value):
        """Clean string values by removing quotes and handling empty values"""
        if isinstance(value, str):
            # Remove surrounding quotes if present
            value = value.strip('"')
            # Remove any other unwanted characters
            value = value.strip()
        return value if value is not None else ''