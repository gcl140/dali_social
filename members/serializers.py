from rest_framework import serializers
from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    full_profile_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Member
        fields = [
            'id',
            'name',
            'year',
            'roles',
            'dev',
            'des',
            'pm',
            'core',
            'mentor',
            'major',
            'minor',
            'birthday',
            'home',
            'quote',
            'favorite_thing_1',
            'favorite_thing_2',
            'favorite_thing_3',
            'favorite_dartmouth_tradition',
            'fun_fact',
            'picture',
            'full_profile_url',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_roles(self, obj):
        return obj.get_roles()
    
    def get_full_profile_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(f'/members/{obj.id}/')
        return f'/members/{obj.id}/'

class MemberListSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    
    class Meta:
        model = Member
        fields = [
            'id',
            'name',
            'year',
            'roles',
            'major',
            'picture',
        ]
    
    def get_roles(self, obj):
        return obj.get_roles()

class MemberSearchSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    
    class Meta:
        model = Member
        fields = [
            'id',
            'name',
            'year',
            'roles',
            'major',
            'minor',
            'home',
            'picture',
        ]
    
    def get_roles(self, obj):
        return obj.get_roles()

# Serializer for member statistics
class MemberStatsSerializer(serializers.Serializer):
    total_members = serializers.IntegerField()
    by_year = serializers.DictField()
    by_role = serializers.DictField()
    recent_members = MemberListSerializer(many=True)