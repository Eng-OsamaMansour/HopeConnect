from rest_framework import serializers
from .models import Matcher

class MatcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matcher
        fields = ['id', 'need_request', 'volunteer_offer', 'created_at']
