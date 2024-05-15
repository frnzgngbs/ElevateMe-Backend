from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from ..Model.ProblemStatementModel import  TwoVennProblemStatementModel, ThreeVennProblemStatementModel
from ..Serializer.VennSerializer import TwoVennSerializer, ThreeVennSerializer

class TwoVennProblemStatementSerializer(serializers.ModelSerializer):
    venn = TwoVennSerializer()  # Remove read_only=True

    class Meta:
        model = TwoVennProblemStatementModel
        fields = '__all__'


    def create(self, validated_data):
        venn = validated_data.pop("venn", None)
        if venn:
            two_venn_serializer = TwoVennSerializer(data=venn, **validated_data)
            if two_venn_serializer.is_valid():
                venn = two_venn_serializer.save()
                problem_statement = TwoVennProblemStatementModel.objects.create(venn=venn, **validated_data)
                return problem_statement
        else:
            raise serializers.ValidationError({"error": "Cannot save a problem statement without venn diagram."})

class ThreeProblemStatementSerializer(serializers.ModelSerializer):
    venn = ThreeVennSerializer()  # Remove read_only=True

    class Meta:
        model = ThreeVennProblemStatementModel
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        venn = validated_data.pop("venn", None)
        if venn:
            three_venn_serializer = ThreeVennSerializer(data=venn, **validated_data)
            if three_venn_serializer.is_valid():
                venn = three_venn_serializer.save()
                problem_statement = ThreeVennProblemStatementModel.objects.create(venn=venn, **validated_data)
                return problem_statement
        else:
            raise serializers.ValidationError({"error": "Cannot save a problem statement without venn diagram."})