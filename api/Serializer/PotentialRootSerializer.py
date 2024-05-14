from rest_framework import serializers

class PotentialRootSerializer(serializers.Serializer):
    list_of_whys = serializers.ListField(
        child=serializers.CharField()
    )

    def validate(self, data):
        if data.get('list_of_whys') is None:
            return serializers.ValidationError({"error": "Cannot take an empty list of whys."})
        return data