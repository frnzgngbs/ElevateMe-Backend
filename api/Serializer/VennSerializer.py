from rest_framework import serializers

from .UserSerializer import UserSerializer
from ..Model.VennDiagramModel import TwoVennDiagram, ThreeVennDiagram

class TwoVennSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = TwoVennDiagram
        fields = '__all__'

    def create(self, validated_data):
        return TwoVennDiagram.objects.create(**validated_data)

class ThreeVennSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = ThreeVennDiagram
        fields = '__all__'


    def create(self, validated_data):
        return ThreeVennDiagram.objects.create(**validated_data)


    def validate(self,data):
        if data['field1'] == data['field2'] or data['field1'] == data['field3'] or data['field2'] == data['field3']:
            raise serializers.ValidationError({"error": "field1, field2, and field3 must all be different."})
        return data