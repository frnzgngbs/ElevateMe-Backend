from rest_framework import serializers

class TwoVennSerializer(serializers.Serializer):
    field1 = serializers.CharField()
    field2 = serializers.CharField()
    filter_field = serializers.CharField(required=False)

    def validate(self, data):
        if data.get('field1') == data.get('field2'):
            raise serializers.ValidationError({"error": "field1 and field2 must be different."})
        return data

class ThreeVennSerializer(serializers.Serializer):
    field1 = serializers.CharField()
    field2 = serializers.CharField()
    field3 = serializers.CharField()
    filter_field = serializers.CharField(required=False)

    def validate(self,data):
        if data['field1'] == data['field2'] or data['field1'] == data['field3'] or data['field2'] == data['field3']:
            raise serializers.ValidationError({"error": "field1, field2, and field3 must all be different."})
        return data