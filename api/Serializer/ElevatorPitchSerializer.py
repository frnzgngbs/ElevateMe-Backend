from rest_framework import serializers

class ElevatorPitchSerializer(serializers.Serializer):
    list_of_hmws = serializers.ListField(child=serializers.CharField())

