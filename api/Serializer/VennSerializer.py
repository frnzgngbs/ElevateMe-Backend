from rest_framework import serializers

from .UserSerializer import UserSerializer
from ..Model.VennDiagramModel import TwoVennDiagram, ThreeVennDiagram

class TwoVennSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwoVennDiagram
        fields = ['field1', 'field2', 'filter']

    def create(self, validated_data):
        print(validated_data)
        return TwoVennDiagram.objects.create(**validated_data)

class ThreeVennSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreeVennDiagram
        fields = ['field1', 'field2', 'filter', 'field3']


    def create(self, validated_data):
        return ThreeVennDiagram.objects.create(**validated_data)
