from rest_framework import serializers
from .models import Orphan, OrphanSponsor, OrphanUpdate

class OrphanSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Orphan
        fields = ("id", "orphanage", "national_id", "name", "gender", "birth_date", 
                 "health_info", "education_status", "photo", "age")
        read_only_fields = ("id","national_id")

class OrphanUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrphanUpdate
        fields = ("id", "orphan", "title", "photo", "note", "created_at")
        read_only_fields = ("id", "created_at")

class OrphanSponsorSerializer(serializers.ModelSerializer):
    orphan_details = OrphanSerializer(source='orphan', read_only=True)
    
    class Meta:
        model = OrphanSponsor
        fields = ['id', 'orphan', 'donor', 'is_active', 'created_at', 'orphan_details']
        read_only_fields = ['donor', 'created_at']
        
    def validate(self, data):
        orphan = data.get('orphan')
        donor = self.context['request'].user
        
        if OrphanSponsor.objects.filter(orphan=orphan, donor=donor).exists():
            raise serializers.ValidationError("You are already sponsoring this orphan")
            
        return data