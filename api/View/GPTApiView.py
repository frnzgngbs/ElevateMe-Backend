from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
import openai
import os

from ..Serializer.VennSerializer import TwoVennSerializer, ThreeVennSerializer

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

class GPTApiView(ViewSet):
    permission_classes = [AllowAny]
    serializer_class = None

    @action(detail=False, methods=['post', 'get'], serializer_class=TwoVennSerializer)
    def two_venn(self, request):
        field1 = request.data.get('field1')
        field2 = request.data.get('field2')
        field_filter = request.data.get('filter')

        prompt = two_prompt(
            field1=field1,
            field2=field2,
            field_filter=field_filter)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Disregard if the question is out of the context  and seems like a nonsense to you. Also,"
                            "in generating responses, you should give it directly without explanation."
                            "Only generate problem statement."},
                {"role": "user", "content": prompt}]
        )

        problem_statement = response.choices[0].message.content.split('\n')

        return Response({"response": problem_statement}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post', 'get'], serializer_class=ThreeVennSerializer)
    def three_venn(self, request):
        field1 = request.data.get('field1')
        field2 = request.data.get('field2')
        field3 = request.data.get('field3')
        field_filter = request.data.get('filter')

        prompt = three_prompt(
            field1=field1,
            field2=field2,
            field3=field3,
            field_filter=field_filter)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Disregard if the question is out of the context  and seems like a nonsense to you. Also,"
                            "in generating responses, you should give it directly without explanation."
                            "Only generate problem statement."},
                {"role": "user", "content": prompt}]
        )

        problem_statement = response.choices[0].message.content.split('\n')

        return Response({"response": problem_statement}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def five_whys(self, request):
        selected_problem = request.data.get('ranked_problem')

        prompt = (
            f"Generate five whys to uncover the underlying issue behind "
            f"{selected_problem}. Make it relevant to the {selected_problem} and understandable.")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Disregard if the question is out of the context  and seems like a nonsense to you. Also,"
                            "in generating responses, you should give it directly without explanation."
                 },
                {"role": "user", "content": prompt}
            ]
        )

        five_whys = response.choices[0].message.content.split('\n')

        return Response({"response": five_whys}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def potential_root(self, request):
        list_of_whys = request.data.get('list_of_whys')

        joined_whys = ", ".join(list_of_whys)

        prompt = (
            f"Generate potential root problem to uncover the underlying issue behind "
            f"{joined_whys}. Make it relevant to the {joined_whys} and understandable.")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Disregard if the question is out of the context  and seems like a nonsense to you. Also,"
                            "in generating responses, you should give it directly without explanation."
                 },
                {"role": "user", "content": prompt}
            ]
        )

        print(response)

        root_problem = response.choices[0].message.content.split('\n')

        return Response({"response": root_problem}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def five_hmws(self, request):
        root_problem = request.data.get('root_problem')

        prompt = (
            f"Generate five How Might We (HMW) given the root potential problem: {root_problem}."
            f"Make it relevant to the {root_problem} and understandable.")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Disregard if the question is out of the context  and seems like a nonsense to you. Also,"
                            "in generating responses, you should give it directly without explanation."
                 },
                {"role": "user", "content": prompt}
            ]
        )

        five_hmws = response.choices[0].message.content.split('\n')

        return Response({"response": five_hmws}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def elevator_pitch(self, request):
        pass



def three_prompt(**kwargs):
    if kwargs.get('field_filter') is not None:
        return f"Generate 5 problem statement given these 3 fields: {kwargs.get('field1')}, {kwargs.get('field2')}, {kwargs.get('field3')}."
    else:
        return (
            f"Generate 5 problem statement given these 3 fields: {kwargs.get('field1')}, {kwargs.get('field2')}, {kwargs.get('field3')}. "
            f"Apply filter: {kwargs.get('field_filter')}")

def two_prompt(**kwargs):
    if kwargs.get('field_filter') is not None:
        return (
            f"Generate 5 problem statement given these 3 fields: {kwargs.get('field1')}, {kwargs.get('field2')}, {kwargs.get('field3')}."
        )
    else:
        return (
            f"Generate 5 problem statement given these 3 fields: {kwargs.get('field1')}, {kwargs.get('field2')}, {kwargs.get('field3')}. "
            f"Apply filter: {kwargs.get('field_filter')}"
        )