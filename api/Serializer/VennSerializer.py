from rest_framework import serializers

class TwoVennSerializer(serializers.Serializer):
    field1 = serializers.CharField()
    field2 = serializers.CharField()
    filter_field = serializers.CharField(required=False)

class ThreeVennSerializer(serializers.Serializer):
    field1 = serializers.CharField()
    field2 = serializers.CharField()
    field3 = serializers.CharField()
    filter_field = serializers.CharField(required=False)
