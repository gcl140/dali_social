import json
from django.core.management.base import BaseCommand
from members.models import Member

class Command(BaseCommand):
    help = 'Fixed import that handles None values'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file']
        
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        print(f"📊 Found {len(data)} potential members")
        
        members_created = 0
        
        for member_data in data:
            if not isinstance(member_data, dict):
                print(f"❌ Skipping non-dictionary item: {type(member_data)}")
                continue
            
            name = member_data.get('name')
            if not name:
                print("❌ Skipping member with no name")
                continue
            
            print(f"👤 Processing: {name}")
            
            try:
                # Convert None values to empty strings
                cleaned_data = self.clean_member_data(member_data)
                
                # Use get_or_create to avoid duplicates
                member, created = Member.objects.get_or_create(
                    name=cleaned_data['name'],
                    defaults=cleaned_data
                )
                
                if created:
                    members_created += 1
                    print(f"✅ Created: {name}")
                else:
                    print(f"⚠️  Already exists: {name}")
                    
            except Exception as e:
                print(f"❌ Failed to create {name}: {str(e)}")
                import traceback
                traceback.print_exc()
        
        print(f"\n🎉 IMPORT COMPLETE")
        print(f"📈 Members created: {members_created}")
        print(f"💾 Total in database: {Member.objects.count()}")

    def clean_member_data(self, data):
        """Convert None values to appropriate defaults"""
        return {
            'name': data.get('name', ''),
            'year': self.clean_value(data.get('year', '2024')),
            'dev': bool(data.get('dev', False)),
            'des': bool(data.get('des', False)),
            'pm': bool(data.get('pm', False)),
            'core': bool(data.get('core', False)),
            'mentor': bool(data.get('mentor', False)),
            'major': self.clean_value(data.get('major')),
            'minor': self.clean_value(data.get('minor')),
            'birthday': self.clean_value(data.get('birthday')),
            'home': self.clean_value(data.get('home')),
            'quote': self.clean_value(data.get('quote')),
            'favorite_thing_1': self.clean_value(data.get('favorite thing 1')),
            'favorite_thing_2': self.clean_value(data.get('favorite thing 2')),
            'favorite_thing_3': self.clean_value(data.get('favorite thing 3')),
            'favorite_dartmouth_tradition': self.clean_value(data.get('favorite dartmouth tradition')),
            'fun_fact': self.clean_value(data.get('fun fact')),
            'picture': self.clean_value(data.get('picture')),
        }

    def clean_value(self, value):
        """Convert None to empty string, otherwise return the value"""
        if value is None:
            return ''
        return str(value)