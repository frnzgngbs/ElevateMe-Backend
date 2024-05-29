from rest_framework import serializers

from ..Model.VennDiagramModel import TwoVennDiagram, ThreeVennDiagram

class TwoVennSerializer(serializers.ModelSerializer):
    filter = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = TwoVennDiagram
        fields = ['field1', 'field2', 'filter']
        extra_kwargs = {
            'filter': {'required': False}
    }

    def create(self, validated_data):
        print(validated_data)
        return TwoVennDiagram.objects.create(**validated_data)


class ThreeVennSerializer(serializers.ModelSerializer):
    filter = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = ThreeVennDiagram
        fields = ['field1', 'field2', 'filter', 'field3']



    def create(self, validated_data):
        return ThreeVennDiagram.objects.create(**validated_data)
